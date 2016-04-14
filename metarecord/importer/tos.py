import re

from openpyxl import load_workbook

from metarecord.models import (PersonalData, ProtectionClass, PublicityClass, RetentionPeriod, RetentionReason,
                               SecurityPeriod, SecurityReason, SocialSecurityNumber)
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
