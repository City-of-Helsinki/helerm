import re
from collections import OrderedDict

from openpyxl import load_workbook

from metarecord.models import (Action, Function, PersonalData, Phase, ProtectionClass, PublicityClass, Record,
                               RetentionPeriod, RetentionReason, SecurityPeriod, SecurityReason, SocialSecurityNumber)
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
    MODEL_MAPPING = OrderedDict([
        ('Tehtäväluokka', Function),
        ('Käsittelyvaiheen metatiedot', Phase),
        ('Toimenpiteen metatiedot', Action),
        ('Asiakirjan metatiedot', Record),
    ])
    MODEL_HIERARCHY = list(MODEL_MAPPING.values())

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

    def _get_data(self, sheet):
        DATA_ROW = 6

        max_col = sheet.max_column + 1
        headers = [sheet.cell(row=1, column=x).value for x in range(1, max_col)]
        headers = [self._clean_header(s) for s in headers if s]
        data = []
        cells = sheet.get_squared_range(1, DATA_ROW, max_col, sheet.max_row + 1)
        for row in cells:
            attrs = {}
            for col, attr in enumerate(headers):
                val = row[col].value
                if col == 0 and not val:
                    break
                if val is not None:
                    attrs[attr] = val
            data.append(attrs)
        return data

    def _clean_header(self, s):
        if not s:
            return s
        # strip leading numeric ids
        s = re.sub(r'^[0-9. ]+', '', s)
        # strip stuff within parentheses
        s = re.sub(r' \(.+\)', '', s)
        # convert multiple spaces into one
        s = re.sub(r' {2,}', ' ', s)
        return s

    def _import_data_object(self, model, parent, attributes):
        if not model:
            return
        model_attributes = {}
        for attribute, value in attributes.items():
            attribute_class = self.ATTRIBUTE_MAPPING.get(attribute)
            if not attribute_class:
                #print('Invalid attribute %s' % attribute)
                continue
            value_object = None
            try:
                value_object = attribute_class.objects.get(value=value)
            except (attribute_class.DoesNotExist, ValueError):
                print(' '*12 + 'Invalid value %s' % value)
            if value_object:
                field_name = attribute_class.get_referencing_field_name(model)
                model_attributes[field_name] = value_object

        if model == Phase:
            parent_field_name = 'function'
            name = {'name': attributes.get('Käsittelyvaihe')}
        elif model == Action:
            parent_field_name = 'phase'
            name = {'name': attributes.get('Toimenpide')}
        else:
            parent_field_name = 'action'
            t = attributes.get('Asiakirjan tyyppi')
            if not t:
                print(' '*12 + 'type missing')
                t = 'not available'
            name = {'type': t}

        model_attributes.update(name)
        model_attributes[parent_field_name] = parent

        new_obj = model.objects.create(**model_attributes)
        return new_obj

    def _import_function(self, sheet):
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
        return function

    def _import_data_recursive(self, data, index, level, parent):
        model = self.MODEL_HIERARCHY[level]
        latest_obj = parent
        while index < len(data) - 1:
            print(' '*8 + 'Processing row %d' % index)
            datum = data[index]
            if not datum:
                index += 1
                continue
            try:
                new_model = self.MODEL_MAPPING.get(datum['Tehtäväluokka'])
                new_level = self.MODEL_HIERARCHY.index(new_model)
            except ValueError:
                print(' '*12 + 'skipping')
                index += 1
                continue
            if new_level == level:
                latest_obj = self._import_data_object(model, parent, datum)
                index += 1
            elif new_level > level:
                index = self._import_data_recursive(data, index, new_level, latest_obj)
                continue
            else:
                break
        return index

    def import_data(self):
        print('Importing data...')

        for sheet in self.wb:
            print()
            print('Processing sheet %s' % sheet.title)
            if sheet.cell('A1').value != 'Tehtäväluokka':
                print('Skipping')
                continue

            print(' '*4 + 'Processing function')
            function = self._import_function(sheet)

            print(' '*4 + 'Processing data')
            data = self._get_data(sheet)
            self._import_data_recursive(data, 0, 0, function)

        print('\nDone.')
