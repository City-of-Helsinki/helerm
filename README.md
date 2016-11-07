# helerm - Helsinki Electronic Records Management Classification System

## Prerequisites

- Python 3.4+
- PostgreSQL 9.1+

## Installation

- Setup and activate a virtualenv ([virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) is a nice tool to handle virtualenvs)
 
- Install required Python packages

```
pip install -r requirements.txt
```

- Create `local_settings.py` file in the project root and use it to override settings as needed.

- Create a database

```
sudo -u postgres createuser -L -R -S helerm
sudo -u postgres createdb -Ohelerm helerm
```

- Create database tables etc.

```
python manage.py migrate
```

- To enable Finnish translations, run

```
python manage.py compilemessages
```

- You will probably need a superuser as well

```
python manage.py createsuperuser
```

## Development

- [pip-tools](https://github.com/nvie/pip-tools) is used to ease requirement handling. 
  To install development packages, run
  
```
pip-sync requirements.txt dev-requirements.txt
```

- To start the development server, run

```
python manage.py runserver 127.0.0.1:8000
```

Admin ui will be located at http://127.0.0.1:8000/admin/

API root will be located at http://127.0.0.1:8000/v1/

## Import

- First you need to import functions and attributes. An excel file containing the attributes is needed.

```
python manage.py import_functions data/helsinki-functions.csv
python manage.py import_attributes <excel file>
```

- Actual data can then be imported by running

```
python manage.py import_data <data excel file>
```

- To import a function template run

```
python manage.py import_template <data excel file> <sheet name> [template name]
```

## Export
 
- All data can be exported to a XML file by running

```
python manage.py export_data <xml file>
```
