import re
from collections import OrderedDict

from openpyxl import load_workbook

from metarecord.models import Action, Attribute, AttributeValue, Function, Phase, Record


class TOSImporterException(Exception):
    pass


class TOSImporter:

    # valid attributes and their identifiers
    CHOICE_ATTRIBUTES = {
        'Julkisuusluokka': 'PublicityClass',
        'Salassapitoaika': 'SecurityPeriod',
        'Salassapitoperuste': 'SecurityReason',
        'Henkilötietoluonne': 'PersonalData',
        'Säilytysaika': 'RetentionPeriod',
        'Säilytysajan peruste': 'RetentionReason',
        'Suojeluluokka': 'ProtectionClass',
        'Henkilötunnus': 'SocialSecurityNumber',
        'Säilytysajan laskentaperuste': 'RetentionPeriodStart',
        'Paperiasiakirjojen säilytysjärjestys': 'StorageOrder',
        'Paperiasiakirjojen säilytysaika arkistossa': 'RetentionPeriodTotal',
        'Paperiasiakirjojen säilytysaika työpisteessä': 'RetentionPeriodOffice',
        'Salassapitoajan laskentaperuste': 'Restriction.SecurityPeriodStart',
        'Suojaustaso': 'Restriction.ProtectionLevel',
        'Turvallisuusluokka': 'Restriction.SecurityClass',
        'Asiakirjatyyppi': 'RecordType',
    }
    FREE_TEXT_ATTRIBUTES = {
        'Lisätietoja': 'AdditionalInformation',
        'Rekisteröinti/ Tietojärjestelmä': 'InformationSystem',
        'Paperiasiakirjojen säilytyspaikka': 'StorageLocation',
        'Paperiasiakirjojen säilytyksen vastuuhenkilö': 'StorageAccountable',
    }

    MODEL_MAPPING = OrderedDict([
        ('Asian metatiedot', Function),
        ('Käsittelyvaiheen metatiedot', Phase),
        ('Toimenpiteen metatiedot', Action),
        ('Asiakirjan metatiedot', Record),
        ('Asiakirjan liitteen metatiedot', Record),
    ])
    MODEL_HIERARCHY = list(MODEL_MAPPING.values())

    ATTACHMENT_RECORD_TYPE_NAME = 'liite'

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

    def _clean_attribute_value(self, s):
        if not s:
            return None
        return re.sub(r'\s\s+', ' ', str(s)).strip() or None

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

    def _get_first_data_row(self, sheet):
        data_row = 1
        while sheet.cell(row=data_row, column=1).value != 'Asian metatiedot':
            data_row += 1
            if data_row > sheet.max_row:
                print('Cannot find first data row')
                return None
        return data_row

    def _get_data(self, sheet):
        data_row = self._get_first_data_row(sheet)
        if not data_row:
            return None

        max_col = sheet.max_column + 1
        headers = [sheet.cell(row=1, column=x).value for x in range(1, max_col)]
        headers = [self._clean_header(s) for s in headers if s]
        data = []
        cells = sheet.get_squared_range(1, data_row, max_col, sheet.max_row + 1)
        for row in cells:
            attrs = {}
            for col, attr in enumerate(headers):
                cleaned_value = self._clean_attribute_value(row[col].value)
                if col == 0 and not cleaned_value:
                    break
                if cleaned_value:
                    attrs[attr] = cleaned_value
            data.append(attrs)
        return data

    def _get_function_data(self, sheet):
        first_data_row = self._get_first_data_row(sheet)
        if not first_data_row:
            return None

        # get all four function id hierarchy levels
        # for example ['5', '05 01', '05 01 03', None]
        function_ids = []
        for row in range(2, first_data_row):
            value = sheet.cell(row=row, column=1).value
            if value:
                value = str(value).strip()
            function_ids.append(value)

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
        if not function_data:
            return

        parent_id = function_data.pop('parent_function_id')
        if parent_id:
            try:
                function_data['parent'] = Function.objects.latest_version().get(function_id=parent_id)
            except Function.DoesNotExist:
                raise TOSImporterException(
                    'Cannot set parent for function %s, function %s does not exist' %
                    (function_data['function_id'], parent_id)
                )

        try:
            function = Function.objects.latest_version().get(function_id=function_data['function_id'])
            if function.phases.count() != 0:
                raise TOSImporterException(
                    'Function %s seems to be populated already.' % function_data['function_id']
                )

            function.metadata_versions.all().delete()
            for key, value in function_data.items():
                setattr(function, key, value)
            function.save()
            function.create_metadata_version()

        except Function.DoesNotExist:
            function = Function.objects.create(**function_data)

        return function

    def _get_attributes(self, data):
        all_attributes = dict(self.CHOICE_ATTRIBUTES, **self.FREE_TEXT_ATTRIBUTES)

        attributes = {}
        for attribute_name, attribute_value in data['attributes'].items():
            if attribute_name == 'Asiakirjan tyyppi':
                attribute_name = 'Asiakirjatyyppi'
            if attribute_name not in all_attributes:
                print('Illegal attribute: %s' % attribute_name)
                continue
            attributes[all_attributes[attribute_name]] = str(attribute_value)

        return attributes

    def _save_structural_element(self, model, parent, data, index, parent_record=None):
        model_attributes = {}  # model specific attributes
        name_attribute = {}  # attribute and value describing name, PhaseType, ActionType or TypeSpecifier

        if model == Phase:
            parent_field_name = 'function'
            # if the value is a valid PhaseType attribute value then PhaseType attribute is used for name,
            # otherwise TypeSpecifier
            is_phase_type = AttributeValue.objects.filter(
                attribute__identifier='PhaseType', value=data['name']
            ).exists()
            if is_phase_type:
                name_attribute = {'PhaseType': data['name']}
            else:
                name_attribute = {'TypeSpecifier': data['name']}
        elif model == Action:
            parent_field_name = 'phase'
            # if the value is a valid ActionType attribute value then ActionType attribute is used for name,
            # otherwise TypeSpecifier
            is_action_type = AttributeValue.objects.filter(
                attribute__identifier='ActionType', value=data['name']
            ).exists()
            if is_action_type:
                name_attribute = {'ActionType': data['name']}
            else:
                name_attribute = {'TypeSpecifier': data['name']}
        elif model == Record and parent_record is None:
            parent_field_name = 'action'
        else:  # attachment
            parent_field_name = 'action'
            model_attributes['parent'] = parent_record

        model_attributes[parent_field_name] = parent

        model_attributes['index'] = index

        new_obj = model(**model_attributes)

        new_obj.attributes = name_attribute
        new_obj.attributes.update(self._get_attributes(data))

        new_obj.save()
        return new_obj

    def _save_function(self, function):
        function_obj = function['obj']

        # Make sure children are nuked
        function_obj.phases.all().delete()

        for idx, phase in enumerate(function['phases'], 1):
            phase_obj = self._save_structural_element(Phase, function_obj, phase, idx)
            for idx, action in enumerate(phase['actions'], 1):
                action_obj = self._save_structural_element(Action, phase_obj, action, idx)
                record_idx = 0
                for record in action['records']:
                    record_idx += 1
                    record_obj = self._save_structural_element(Record, action_obj, record, record_idx)
                    for attachment in record['attachments']:
                        record_idx += 1
                        self._save_structural_element(Record, action_obj, attachment, record_idx, record_obj)

        function_obj.attributes = self._get_attributes(function)
        function_obj.error_count = function.get('error_count', 0)
        function_obj.save()

    def _process_data(self, sheet, function_obj):
        data = self._get_data(sheet)

        # Parse data with a state machine
        function = {'phases': []}
        target = function
        self.current_function = function
        phase = action = None
        previous = None
        for row in data:
            name = None
            child_list = []

            if not row:
                continue

            type_info = str(row.pop('Tehtäväluokka')).strip()
            if type_info == 'Asian metatiedot':
                target['obj'] = function_obj
                name = function_obj.name
                # Must be the first row
                assert phase is None and action is None
                previous = Function
            elif type_info.startswith('Asiakirjallisen tiedon käsittely'):
                assert phase is None and action is None
                # Skip row
                continue
            elif type_info == 'Käsittelyvaiheen metatiedot':
                if previous is None:
                    print('Parent of phase %s missing' % row.get('Käsittelyvaihe'))
                    continue
                phase = {}
                child_list = function['phases']
                phase['actions'] = []
                action = None
                target = phase
                name = row.pop('Käsittelyvaihe', None)
                assert name
                previous = Phase
            elif type_info == 'Toimenpiteen metatiedot':
                if previous == Function:
                    print('Parent of action %s missing' % row.get('Toimenpide'))
                    continue
                action = {}
                child_list = phase['actions']
                action['records'] = []
                target = action
                name = row.pop('Toimenpide', None)
                previous = Action
            elif type_info == 'Asiakirjan metatiedot':
                if previous in (Function, Phase):
                    print('Parent of record %s missing' % row.get('Asiakirjatyypin tarkenne'))
                    continue
                record = {}
                child_list = action['records']
                record['attachments'] = []
                target = record
                name = row.pop('Asiakirjatyypin tarkenne', None)
                previous = Record
            elif type_info == 'Asiakirjan liitteen metatiedot':
                if previous in (Function, Phase, Action):
                    print('Parent of attachment %s missing' % row.get('Asiakirjan liitteet'))
                attachment = {}
                child_list = record['attachments']
                target = attachment
                name = row.pop('Asiakirjan liitteet', '---')
                row.pop('Asiakirjatyypin tarkenne', None)

            if type_info not in self.MODEL_MAPPING:
                self._emit_error('Skipping row with type %s' % type_info)
                continue
            target_model = self.MODEL_MAPPING[type_info]
            if not target_model:
                continue

            if target_model != Function and (not name or len(name) <= 2):
                if row:
                    self._emit_error('No name for %s, data: %s' % (target_model._meta.verbose_name, row))
                continue

            target['name'] = name

            # Clean some attributes
            for name in ('Säilytysaika', 'Paperiasiakirjojen säilytysaika arkistossa'):
                s = row.get(name)
                if isinstance(s, str) and s.startswith('-1'):
                    row[name] = '-1'

            target['attributes'] = row
            child_list.append(target)

        self._save_function(function)

    def import_attributes(self):
        print('Importing attributes...')

        try:
            sheet = self.wb['Koodistot']
        except KeyError:
            print('Cannot import attributes, the workbook does not contain sheet "Koodistot".')
            return

        codesets = self._get_codesets(sheet)
        handled_attrs = set()

        for attr, values in codesets.items():
            print('\nProcessing %s' % attr)

            all_attributes = self.CHOICE_ATTRIBUTES.copy()
            all_attributes.update(self.FREE_TEXT_ATTRIBUTES)

            if attr == 'Asiakirjatyypit':
                attr = 'Asiakirjatyyppi'

            if attr not in all_attributes:
                print('    skipping ')
                continue

            try:
                attribute_obj, created = Attribute.objects.update_or_create(
                    identifier=all_attributes.get(attr), defaults={'name': attr}
                )
            except ValueError as e:
                print('    !!!! Cannot create attribute: %s' % e)
                continue
            handled_attrs.add(all_attributes.get(attr))

            if attr in self.FREE_TEXT_ATTRIBUTES:
                print('    free text attribute')
                continue

            for value in values:
                try:
                    cleaned_value = self._clean_attribute_value(value)
                    if not cleaned_value:
                        raise ValueError('Invalid value: "%s"' % value)
                    obj, created = AttributeValue.objects.get_or_create(attribute=attribute_obj, value=cleaned_value)
                except ValueError as e:
                    # TODO just printing errors and continuing here for now
                    print('    !!!! Cannot create attribute value: %s' % e)
                    continue

                info_str = 'Created' if created else 'Already exist'
                print('    %s: %s' % (info_str, value))

        # add also free text attributes that don't exist in the codesets sheet
        for name, identifier in self.FREE_TEXT_ATTRIBUTES.items():
            if identifier not in handled_attrs:
                attribute_obj, created = Attribute.objects.update_or_create(
                    identifier=identifier, defaults={'name': name}
                )
                info_str = 'Created' if created else 'Already exist'
                print("\n%s: free text attribute %s that doesn't exist in the sheet" % (info_str, name))

        print('\nDone.')

    def import_data(self):
        print('Importing data...')

        for sheet in self.wb:
            print('Processing sheet %s' % sheet.title)
            if (sheet.max_column <= 2 or sheet.max_row <= 2 or sheet.cell('A1').value != 'Tehtäväluokka' or
                    sheet.cell('A2').value == 'Kaikki Ahjo-luokat'):
                print('Skipping')
                continue

            # process function
            function = self._import_function(sheet)

            # process data
            if function:
                self._process_data(sheet, function)

        print('Done.')

    def import_template(self, sheet_name, template_name):
        print('Importing template...')

        sheet = self.wb.get_sheet_by_name(sheet_name)
        template_name = template_name or sheet_name

        function, created = Function.objects.get_or_create(name=template_name, is_template=True)

        if created:
            print('Creating new template %s' % template_name)
        else:
            print('Updating template %s' % template_name)

        self._process_data(sheet, function)

        print('Done.')
