import re
from collections import OrderedDict

from openpyxl import load_workbook

from metarecord.models import Action, Attribute, AttributeValue, Function, Phase, Record, RecordType


class TOSImporter:

    CHOICE_ATTRIBUTES = {
        'Julkisuusluokka',
        'Salassapitoaika',
        'Salassapitoperuste',
        'Henkilötietoluonne',
        'Säilytysaika',
        'Säilytysajan peruste',
        'Suojeluluokka',
        'Henkilötunnus',
        'Asiakirjatyypit',
        'Säilytysajan laskentaperuste',
        'Paperiasiakirjojen säilytysjärjestys',
        'Paperiasiakirjojen säilytysaika arkistossa',
        'Paperiasiakirjojen säilytysaika työpisteessä',
        'Salassapitoajan laskentaperuste',
    }

    FREE_TEXT_ATTRIBUTES = {
        'Lisätietoja',
        'Rekisteröinti/ Tietojärjestelmä',
        'Paperiasiakirjojen säilytyspaikka',
        'Paperiasiakirjojen säilytyksen vastuuhenkilö',
    }

    MODEL_MAPPING = OrderedDict([
        ('Asian metatiedot', Function),
        ('Käsittelyvaiheen metatiedot', Phase),
        ('Toimenpiteen metatiedot', Action),
        ('Asiakirjan metatiedot', Record),
        ('Asiakirjan liitteen metatiedot', None),  # FIXME: Implement attachment?
    ])
    MODEL_HIERARCHY = list(MODEL_MAPPING.values())

    def __init__(self, fname):
        self.wb = load_workbook(fname, read_only=True)

    def _emit_error(self, text):
        print(text)
        self.current_function['error_count'] = self.current_function.get('error_count', 0) + 1

    def _clean_header(self, s):
        if not s:
            return s
        # strip leading numeric ids
        s = re.sub(r'^[0-9. ]+', '', s)
        # strip stuff within parentheses
        s = re.sub(r' \(.+\)', '', s)
        # convert multiple spaces into one
        s = re.sub(r' {2,}', ' ', s)
        # if there's a '=' in the header, remove the last part
        s = s.split('=')[0].strip()
        return s

    def _get_codesets(self, sheet):
        HEADER_ROW = 5
        VALUE_ROW = 5 + 1

        max_col = sheet.max_column + 1
        attr_names = [sheet.cell(row=HEADER_ROW, column=x).value for x in range(1, max_col)]

        codesets = {}

        for col, attr in enumerate(attr_names):
            attr = self._clean_header(attr)

            # fix inconsistencies in headers between codesets and the actual data
            if attr == 'Paperiasiakirjojen säilytysaika työpisteeessä':
                attr = 'Paperiasiakirjojen säilytysaika työpisteessä'
            elif attr == 'Rekisteröinti/tietojärjestelmä':
                attr = 'Rekisteröinti/ Tietojärjestelmä'

            codesets[attr] = []
            for row in range(VALUE_ROW, sheet.max_row + 1):
                val = sheet.cell(row=row, column=col + 1).value
                if val is None:
                    break

                # strip stuff within parentheses from value
                val = re.sub(r' \(.+\)', '', str(val))

                codesets[attr].append(val)

        return codesets

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

    def _import_function(self, sheet):
        function_data = self._get_function_data(sheet)
        parent_id = function_data.pop('parent_function_id')
        if parent_id:
            try:
                function_data['parent'] = Function.objects.get(function_id=parent_id.strip())
            except Function.DoesNotExist:
                print('!!!! Cannot set parent, function %s does not exist.' % parent_id)
                # TODO ignoring missing parent for now

        function, created = Function.objects.get_or_create(function_id=function_data['function_id'],
                                                           defaults=function_data)
        return function

    def _get_common_attribute_values(self, data):
        attributes = data['attributes']
        attribute_values = []
        for attribute_name, value in attributes.items():
            try:
                attribute = Attribute.objects.get(name=attribute_name)
            except Attribute.DoesNotExist:
                self._emit_error('Invalid attribute %s' % attribute_name)
                continue

            # handle free_text attributes
            if attribute_name in self.FREE_TEXT_ATTRIBUTES:
                attribute_value = AttributeValue.objects.create(attribute=attribute, value=value)
            else:
                try:
                    attribute_value = AttributeValue.objects.get(attribute=attribute, value=value)
                except AttributeValue.DoesNotExist:
                    self._emit_error('Invalid value %s for attribute %s' % (value, attribute_name))
                    continue
            attribute_values.append(attribute_value)

        return attribute_values

    def _save_structural_element(self, model, parent, data, order):
        record_type = data['attributes'].pop('Asiakirjan tyyppi', None)
        paper_record_archive_retention_period = data['attributes'].pop(
            'Paperiasiakirjojen säilytysaika arkistossa', None)
        paper_record_workplace_retention_period = data['attributes'].pop(
            'Paperiasiakirjojen säilytysaika työpisteessä', None)

        model_attributes = {}  # model specific attributes
        attribute_values = self._get_common_attribute_values(data)

        if model == Phase:
            parent_field_name = 'function'
        elif model == Action:
            parent_field_name = 'phase'
        elif model == Record:
            if not record_type:
                self._emit_error('Record type missing')
                return
            model_attributes['type'] = RecordType.objects.get(value=record_type)
            parent_field_name = 'action'
        else:
            raise Exception('Attachments not supported yet')
        model_attributes[parent_field_name] = parent

        model_attributes['name'] = data['name']
        model_attributes['order'] = order

        new_obj = model.objects.create(**model_attributes)
        for attribute_value in attribute_values:
            new_obj.attribute_values.add(attribute_value)
        return new_obj

    def _save_function(self, function):
        function_obj = function['obj']

        # Make sure children and attribute values are nuked
        function_obj.phases.all().delete()
        function_obj.attribute_values.remove()

        attribute_values = self._get_common_attribute_values(function)
        for attribute_value in attribute_values:
            function_obj.attribute_values.add(attribute_value)

        for idx, phase in enumerate(function['phases']):
            phase_obj = self._save_structural_element(Phase, function_obj, phase, idx)
            for idx, action in enumerate(phase['actions']):
                action_obj = self._save_structural_element(Action, phase_obj, action, idx)
                for idx, record in enumerate(action['records']):
                    record_obj = self._save_structural_element(Record, action_obj, record, idx)

        function_obj.error_count = function.get('error_count', 0)
        function_obj.save()

    def _process_data(self, sheet, function_obj):
        data = self._get_data(sheet)

        # Parse data with a state machine
        function = {'phases': []}
        target = function
        self.current_function = function
        phase = action = None
        for row in data:
            name = None
            child_list = []

            if not row:
                continue
            # from pprint import pprint
            # pprint(row)
            type_info = row.pop('Tehtäväluokka').strip()
            if type_info == 'Asian metatiedot':
                target['obj'] = function_obj
                name = function_obj.name
                # Must be the first row
                assert phase is None and action is None
            elif type_info.startswith('Asiakirjallisen tiedon käsittely'):
                assert phase is None and action is None
                # Skip row
                continue
            elif type_info == 'Käsittelyvaiheen metatiedot':
                phase = {}
                child_list = function['phases']
                phase['actions'] = []
                action = None
                target = phase
                name = row.pop('Käsittelyvaihe', None)
                assert name
            elif type_info == 'Toimenpiteen metatiedot':
                action = {}
                child_list = phase['actions']
                action['records'] = []
                target = action
                name = row.pop('Toimenpide', None)
            elif type_info == 'Asiakirjan metatiedot':
                record = {}
                child_list = action['records']
                target = record
                name = row.pop('Asiakirjatyypin tarkenne', None)
                # FIXME: Attachments?

            if type_info not in self.MODEL_MAPPING:
                self._emit_error('Skipping row with type %s' % type_info)
                continue
            target_model = self.MODEL_MAPPING[type_info]
            if not target_model:
                continue

            if not name or len(name) <= 2:
                self._emit_error('No name for %s' % target_model._meta.verbose_name)
                continue

            target['name'] = name
            # Clean some attributes
            s = row.get('Säilytysaika')
            if isinstance(s, str) and s.startswith('-1'):
                row['Säilytysaika'] = '-1'

            target['attributes'] = row
            child_list.append(target)

        self._save_function(function)

    def import_codesets(self):
        print('Importing codesets...')

        try:
            sheet = self.wb['Koodistot']
        except KeyError:
            print('Cannot import codesets, the workbook does not contain sheet "Koodistot".')
            return

        codesets = self._get_codesets(sheet)

        for attr, values in codesets.items():
            print('\nProcessing %s' % attr)

            if attr == 'Asiakirjatyypit':
                for value in values:
                    obj, created = RecordType.objects.get_or_create(value=value)
                    info_str = 'Created' if created else 'Already exist'
                    print('    %s: %s' % (info_str, value))
                continue

            valid_attributes = self.CHOICE_ATTRIBUTES | self.FREE_TEXT_ATTRIBUTES
            if attr not in valid_attributes:
                print('    skipping ')
                continue

            is_free_text = attr in self.FREE_TEXT_ATTRIBUTES

            try:
                attribute_obj, created = Attribute.objects.get_or_create(name=attr, is_free_text=is_free_text)
            except ValueError as e:
                print('    !!!! Cannot create attribute: %s' % e)
                continue

            if is_free_text:
                print('    free text attribute')
                continue

            for value in values:
                try:
                    obj, created = AttributeValue.objects.get_or_create(attribute=attribute_obj, value=value)
                except ValueError as e:
                    # TODO just printing errors and continuing here for now
                    print('    !!!! Cannot create attribute value: %s' % e)
                    continue

                info_str = 'Created' if created else 'Already exist'
                print('    %s: %s' % (info_str, value))

        print('\nDone.')

    def import_data(self):
        print('Importing data...')

        for sheet in self.wb:
            print('Processing sheet %s' % sheet.title)
            if sheet.max_column <= 2 or sheet.max_row <= 2 or sheet.cell('A1').value != 'Tehtäväluokka':
                print('Skipping')
                continue

            # process function
            function = self._import_function(sheet)

            # process data
            self._process_data(sheet, function)

        print('\nDone.')
