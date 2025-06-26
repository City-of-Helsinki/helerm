import csv

from metarecord.models import Function


class FunctionImporter:
    def __init__(self, filename):
        with open(filename, "r") as csvfile:
            self.csv_data = list(csv.reader(csvfile, delimiter=","))

    def _get_parent_function_id(self, function_id):
        if len(function_id) == 2:
            return None
        return function_id[:-3]

    def import_functions(self):
        print("Importing functions...")  # noqa: T201
        for row in self.csv_data:
            function_id = row[0]
            parent_function_id = self._get_parent_function_id(function_id)
            if parent_function_id:
                parent = Function.objects.latest_version().get(
                    function_id=parent_function_id
                )
            else:
                parent = None
            defaults = {"name": row[1], "parent": parent}
            obj, created = Function.objects.latest_version().get_or_create(
                function_id=function_id, defaults=defaults
            )
            print(obj)  # noqa: T201
        print("Done.")  # noqa: T201
