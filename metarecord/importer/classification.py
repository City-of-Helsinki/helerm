import csv

from metarecord.models import Classification


class ClassificationImporter:
    def __init__(self, filename):
        with open(filename, 'r') as csvfile:
            self.csv_data = list(csv.reader(csvfile, delimiter=','))

    def _get_parent_code(self, code):
        if len(code) == 2:
            return None
        return code[:-3]

    def import_classifications(self):
        print('Importing classifications...')
        for row in self.csv_data:
            code = row[0]
            parent_code = self._get_parent_code(code)
            if parent_code:
                parent = Classification.objects.get(code=parent_code)
            else:
                parent = None
            defaults = {
                'title': row[1],
                'parent': parent
            }
            obj, created = Classification.objects.get_or_create(code=code, defaults=defaults)
            print(obj)
        print('Done.')
