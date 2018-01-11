import csv
import re

from metarecord.models import Classification


def clean_row(row):
    return [cell.strip('\n ') for cell in row]


class ClassificationImporter:
    def __init__(self, filename):
        with open(filename, 'r') as csvfile:
            sniffer = csv.Sniffer()
            sniffer.preferred = [',', ';', '\t']

            dialect = sniffer.sniff(csvfile.readline())
            csvfile.seek(0)

            self.csv_data = list(csv.reader(csvfile, dialect=dialect))

    def _get_parent_code(self, code):
        if len(code) == 2:
            return None
        return code[:-3]

    def import_classifications(self):
        print('Importing classifications...')

        count = 0
        for row in self.csv_data:
            row = clean_row(row)

            count += 1
            if len(row) < 2 or not re.match(r"^\d\d(?:\s\d\d)*$", row[0]):
                print('Skipping row number {}'.format(count))
                continue

            code = row[0]
            parent_code = self._get_parent_code(code)

            if parent_code:
                try:
                    parent = Classification.objects.get(code=parent_code)
                except Classification.DoesNotExist:
                    parent = None
            else:
                parent = None

            defaults = {
                'title': row[1],
                'parent': parent
            }

            additional_cells = (
                ('description', 2),
                ('related_classification', 4),
                ('description_internal', 5),
                ('additional_information', 6),
            )

            for (field_name, cell_num) in additional_cells:
                try:
                    defaults[field_name] = row[cell_num]
                except IndexError:
                    pass

            obj, created = Classification.objects.update_or_create(code=code, defaults=defaults)

            print(obj)

        print('Done.')
