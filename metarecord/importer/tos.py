import re

from openpyxl import load_workbook

from metarecord.models import (PersonalData, ProtectionClass, PublicityClass, RetentionPeriod, RetentionReason,
                               SecurityPeriod, SecurityReason, SocialSecurityNumber, Function)
from metarecord.models.attributes import AttributeValueInteger


class TOSImporter:

    ATTRIBUTE_MAPPING = {
        'Julkisuusluokka': PublicityClass,
        'Salassapitoaika': SecurityPeriod,
        'Salassapitoperuste': SecurityReason,
        'Henkilötietoluonne': PersonalData,
        'Säilytysaika': RetentionPeriod,
        'Säilytysajan peruste': RetentionReason,
        'Suojeluluokka': ProtectionClass,
        'Henkilötunnus': SocialSecurityNumber,
    }

    def __init__(self, fname):
        self.wb = load_workbook(fname, read_only=True)

    def import_codesets(self):
        print('Importing codesets...')
        try:
            sheet = self.wb['Koodistot']
        except KeyError:
            print('Cannot import codesets, the workbook does not contain sheet "Koodistot".')
            return
        HEADER_ROW = 5
        VALUE_ROW = 5 + 1

        max_col = sheet.max_column + 1
        attr_names = [sheet.cell(row=HEADER_ROW, column=x).value for x in range(1, max_col)]

        for col, attr in enumerate(attr_names):
            print()

            model = self.ATTRIBUTE_MAPPING.get(attr)
            if not model:
                print('Unknown attribute %s' % attr)
                continue

            print('Processing attribute %s' % attr)
            for row in range(VALUE_ROW, sheet.max_row + 1):
                val = sheet.cell(row=row, column=col + 1).value
                if val is None:
                    if row == VALUE_ROW:
                        print('    No values')
                    break
                if issubclass(model, AttributeValueInteger):
                    # strip stuff within parentheses
                    val = re.sub(r' \(.+\)', '', str(val))

                try:
                    obj, created = model.objects.get_or_create(value=val)
                except ValueError as e:
                    # TODO just printing errors and continuing here for now
                    print('    !!!! Cannot create value: %s' % e)
                    continue

                info_str = 'Created' if created else 'Already exist'
                print('    %s: %s' % (info_str, val))

        print('\nDone.')

    def _get_function_data(self, sheet):

        # get all four function id hierarchy levels
        # for example ['5', '05 01', '05 01 03', None]
        function_ids = [sheet.cell(row=row, column=1).value for row in range(2, 6)]

        # find the last index before none (or the last one in the list if none doesn't exist)
        # that is the index of this function's id
        index = len(function_ids) - 1
        while function_ids[index] is None and index > 0:
            index -= 1

        # get id, name and parent matching the index
        function_data = dict(
            function_id=str(function_ids[index]),
            name=sheet.cell(row=2+index, column=2).value,
            parent_function_id=function_ids[index - 1] if index > 2 else None
        )

        return function_data

    def import_data(self):
        print('Importing data...')

        for sheet in self.wb:
            print()
            print('Processing sheet %s' % sheet.title)
            if sheet.cell('A1').value != 'Tehtäväluokka':
                print('Skipping')
                continue

            print(' '*4 + 'Processing function')

            function_data = self._get_function_data(sheet)
            parent_id = function_data.pop('parent_function_id')
            if parent_id:
                try:
                    function_data['parent'] = Function.objects.get(function_id=parent_id)
                except Function.DoesNotExist:
                    print(' '*8 + '!!!! Cannot set parent, function %s does not exist.' % parent_id)
                    # TODO ignoring missing parent for now

            function, created = Function.objects.get_or_create(function_id=function_data['function_id'],
                                                               defaults=function_data)
            info_str = 'Created' if created else 'Already exist'
            print(' '*8 + '%s function %s %s' % (info_str, function.function_id, function))

        print('\nDone.')
