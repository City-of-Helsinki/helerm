# helerm - Helsinki Electronic Records Management Classification System

[![Requirements](https://requires.io/github/City-of-Helsinki/helerm/requirements.svg?branch=master)](https://requires.io/github/City-of-Helsinki/helerm/requirements/?branch=master)


## Installation

### Manual setup

- Make sure you have the following prerequisites installed:
  - Python 3.7
  - PostgreSQL 10.x

- Setup and activate a virtualenv ([virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) is a nice tool to handle virtualenvs)
 
- Install required Python packages

```
pip install -r requirements.txt
```

- Copy `config_dev.env.example` to `config_dev.env` and edit according
  to your needs. DATABASE_URL is the one setting that you will need to
  uncomment and possibly edit.

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

### Docker compose setup

Make sure you have Docker and Docker Compose 2.x installed. See
https://docs.docker.com/compose/install/ for instructions.

Copy `.docker/django/.env.example` to `.docker/django/.env` and edit according
to your needs. The file is copiously commented.
- See the docker-entrypoint.sh part in .env.example file for setting what
  happens when the container starts.

```
cp .docker/django/.env.example .docker/django/.env
```

Build and start the containers. By default, the container initializes the
database and starts the Django dev server.

```
docker compose up
```

You're now ready to go! The Django dev server is available at http://localhost:8080/

You can run `manage.py` commands in the container. E.g. to perform database migrations:

```
docker compose exec django python manage.py migrate
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

- First you need to import classifications and create attributes

```
python manage.py import_classifications data/helsinki-functions.csv
python manage.py create_attributes
```

- It is also possible to import attributes from an excel file

```
python manage.py import_attributes <excel file>
```

- Temporary step: the old data model requires a function object for every available function code even when there is no actual data for the function. Those initial functions can be created based on current classification by running

```
python manage.py create_initial_functions
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

- Or using the API http://127.0.0.1:8000/export/

### Python XML Schema files and Python bindings

The export uses [pyxb](http://pyxb.sourceforge.net/) library and needs Python bindings to be generated from XSD schema files.

The repo contains two sets of JHS XML Schema files located in `data` directory. In addition to original ones, there are also HKI customized versions, which are in use at least for now.

Generated bindings are included in `metarecord/binding/` so the export should work out of the box.

To generate new bindings from (HKI customized) JHS schema files run

```
pyxbgen -u Skeema_TOS_kooste_HKI_custom.xsd --module-prefix=metarecord.binding --schema-root=data -m jhs
```

By default the generated bindings contain unnecessary references to local files. If the bindings are shared to somewhere, put into the repo for example, it is a good idea to remove unnecessary references by

```
sed -i '' 's/pyxb.utils.utility.Location([^)]*)/None/' metarecord/binding/*jhs.py
```
