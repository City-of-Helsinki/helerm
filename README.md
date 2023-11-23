# helerm - Helsinki Electronic Records Management Classification System

## Installation

### Manual setup

- Make sure you have the following prerequisites installed:
  - Python 3.9
  - PostgreSQL 14.x

- Setup and activate a virtualenv, for example using the built in venv
```bash
python -m venv venv
source venv/bin/activate
```
- Install required Python packages

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
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

You're now ready to go! The Django dev server is available at http://127.0.0.1:8080/

You can run `manage.py` commands in the container. E.g. to perform database migrations:

```
docker compose exec django python manage.py migrate
```

## Development

- [pip-tools](https://github.com/nvie/pip-tools) is used to ease requirement handling.
  To install development packages, run

```
pip-sync requirements.txt requirements-dev.txt
```

- To start the development server, run

```
python manage.py runserver 127.0.0.1:8080
```

Admin UI is located at http://127.0.0.1:8080/admin/

API root is located at http://127.0.0.1:8080/v1/

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

- Temporary step: the old data model requires a function object for every available
  function code even when there is no actual data for the function. Those initial
  functions can be created based on current classification by running

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

- Or using the API http://127.0.0.1:8080/export/

## Commit message format

New commit messages must adhere to the [Conventional Commits](https://www.conventionalcommits.org/)
specification, and line length is limited to 72 characters.

When [`pre-commit`](https://pre-commit.com/) is in use, [`commitlint`](https://github.com/conventional-changelog/commitlint)
checks new commit messages for the correct format.

## Using local Tunnistamo instance for development with docker

### Set tunnistamo hostname

Add the following line to your hosts file (`/etc/hosts` on mac and linux):

    127.0.0.1 tunnistamo-backend

### Create a new OAuth app on GitHub

Go to https://github.com/settings/developers/ and add a new app with the following settings:

- Application name: can be anything, e.g. local tunnistamo
- Homepage URL: http://tunnistamo-backend:8000
- Authorization callback URL: http://tunnistamo-backend:8000/accounts/github/login/callback/

Save. You'll need the created **Client ID** and **Client Secret** for configuring tunnistamo in the next step.

### Install local tunnistamo

Clone https://github.com/City-of-Helsinki/tunnistamo/.

Follow the instructions for setting up tunnistamo locally. Before running `docker compose up` set the following settings in tunnistamo roots `docker-compose.env.yaml`:

- SOCIAL_AUTH_GITHUB_KEY: **Client ID** from the GitHub OAuth app
- SOCIAL_AUTH_GITHUB_SECRET: **Client Secret** from the GitHub OAuth app

After you've got tunnistamo running locally, ssh to the tunnistamo docker container:

`docker compose exec django bash`

and execute the following four commands inside your docker container:

```bash
./manage.py add_oidc_client -n helerm-api -t "code" -u http://localhost:8080/pysocial/complete/tunnistamo/ -i https://api.hel.fi/auth/helerm -m github -s dev -c
./manage.py add_oidc_client -n helerm-api-admin -t "code" -u http://localhost:8080/pysocial/complete/tunnistamo/ -i helerm-api-admin -m github -s dev -c
./manage.py add_oidc_client -n helerm-ui -t "id_token token" -u "http://localhost:3000/callback" "http://localhost:3000/renew" -i helerm-ui -m github -s dev
./manage.py add_oidc_api -n helerm -d https://api.hel.fi/auth -s email,profile -c https://api.hel.fi/auth/helerm
./manage.py add_oidc_api_scope -an helerm -c https://api.hel.fi/auth/helerm -n "helerm" -d "Lorem ipsum"
./manage.py add_oidc_client_to_api_scope -asi https://api.hel.fi/auth/helerm -c helerm-api-admin
./manage.py add_oidc_client_to_api_scope -asi https://api.hel.fi/auth/helerm -c helerm-ui
```

### Configure Tunnistamo to backend

Change the following configuration in `.docker/django/.env`

```
SOCIAL_AUTH_TUNNISTAMO_KEY=helerm-api-admin
SOCIAL_AUTH_TUNNISTAMO_SECRET=<helerm-api-admin client secret from Tunnistamo here>
SOCIAL_AUTH_TUNNISTAMO_OIDC_ENDPOINT=http://tunnistamo-backend:8000/openid
OIDC_API_TOKEN_AUTH_AUDIENCE=https://api.hel.fi/auth/helerm
OIDC_API_TOKEN_AUTH_ISSUER=http://tunnistamo-backend:8000/openid
```
