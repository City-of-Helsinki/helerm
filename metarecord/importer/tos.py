import re
from collections import OrderedDict

from openpyxl import load_workbook

from metarecord.models import (Action, AdditionalInformation, Function, InformationSystem,
                               PaperRecordArchiveRetentionPeriod, PaperRecordRetentionLocation,
                               PaperRecordRetentionOrder, PaperRecordRetentionResponsiblePerson,
                               PaperRecordWorkplaceRetentionPeriod, PersonalData, Phase, ProtectionClass,
                               PublicityClass, Record, RecordType, RetentionCalculationBasis, RetentionPeriod,
                               RetentionReason, SecurityPeriod, SecurityPeriodCalculationBasis, SecurityReason,
                               SocialSecurityNumber)
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
        'Asiakirjan tyyppi': RecordType,
        'Säilytysajan laskentaperuste': RetentionCalculationBasis,
        'Paperiasiakirjojen säilytysjärjestys': PaperRecordRetentionOrder,
        'Rekisteröinti/ Tietojärjestelmä': InformationSystem,
        'Paperiasiakirjojen säilytysaika arkistossa = kokonaissäilytysaika': PaperRecordArchiveRetentionPeriod,
        'Paperiasiakirjojen säilytysaika työpisteeessä': PaperRecordWorkplaceRetentionPeriod,
        'Salassapitoajan laskentaperuste': SecurityPeriodCalculationBasis,
        'Paperiasiakirjojen säilytyspaikka': PaperRecordRetentionLocation,
        'Paperiasiakirjojen säilytyksen vastuuhenkilö': PaperRecordRetentionResponsiblePerson,
        'Lisätietoja': AdditionalInformation,

        # different names between data and codesets
        'Paperiasiakirjojen säilytysaika arkistossa': PaperRecordArchiveRetentionPeriod,
        'Paperiasiakirjojen säilytysaika työpisteessä': PaperRecordWorkplaceRetentionPeriod,
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
            if attr == 'Asiakirjatyypit':
                attr = 'Asiakirjan tyyppi'
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
        # if there's a '=' in the header, remove the last part
        s = s.split('=')[0].strip()
        return s

    def _get_model_attributes(self, model, data):
        model_attributes = {}
        attributes = data['attributes']
        for attribute, value in attributes.items():
            if attribute not in self.ATTRIBUTE_MAPPING:
                self._emit_error('Invalid attribute %s' % attribute)
                continue
            attribute_class = self.ATTRIBUTE_MAPPING[attribute]
            if not attribute_class:
                # Skipping known unknowns
                continue

            value_object = None
            try:
                value_object = attribute_class.objects.get(value=value)
            except (attribute_class.DoesNotExist, ValueError):
                self._emit_error('Invalid value for %s: %s' % (attribute_class._meta.verbose_name, value))
            if value_object:
                field_name = attribute_class.get_referencing_field_name(model)
                model_attributes[field_name] = value_object
        return model_attributes

    def _save_data_object(self, model, parent, data, order):
        model_attributes = self._get_model_attributes(model, data)

        if model == Phase:
            parent_field_name = 'function'
        elif model == Action:
            parent_field_name = 'phase'
        elif model == Record:
            parent_field_name = 'action'
        else:
            raise Exception('Attachments not supported yet')
        model_attributes[parent_field_name] = parent

        model_attributes['name'] = data['name']
        model_attributes['order'] = order

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

    def _emit_error(self, text):
        print(text)
        self.current_function['error_count'] = self.current_function.get('error_count', 0) + 1

    def _save_function(self, sheet, function):
        function_obj = function['obj']

        # Make sure children are nuked
        function_obj.phases.all().delete()

        function_attributes = self._get_model_attributes(Function, function)
        for attribute, value in function_attributes.items():
            setattr(function_obj, attribute, value)

        for idx, phase in enumerate(function['phases']):
            phase_obj = self._save_data_object(Phase, function_obj, phase, idx)
            for idx, action in enumerate(phase['actions']):
                action_obj = self._save_data_object(Action, phase_obj, action, idx)
                for idx, record in enumerate(action['records']):
                    record_obj = self._save_data_object(Record, action_obj, record, idx)

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

        self._save_function(sheet, function)


    def import_data(self):
        print('Importing data...')

        for sheet in self.wb:
            print('Processing sheet %s' % sheet.title)
            if sheet.max_column <= 2 or sheet.max_row <= 2 or sheet.cell('A1').value != 'Tehtäväluokka':
                print('Skipping')
                continue

            print(' '*4 + 'Processing function')
            function = self._import_function(sheet)

            print(' '*4 + 'Processing data')
            self._process_data(sheet, function)
            # self._import_data_recursive(data, 0, 0, function)

        print('\nDone.')
