# CLI Commands

## migrationmanager:
It is used to manage the migrations. Its internally uses `alembic` command.
```bash
python manage.py migrationmanager
```
## test:
It is used to run the tests.
```bash
python manage.py test
```
## linter:
It is used to run the linter. Its internally uses `ruff` command.
```bash
python manage.py linter
```
## exportdata:
It is used to export the data from the database.
```bash
python manage.py exportdata
```
## importdata:
It is used to import the data to the database.
```bash
python manage.py importdata
```
## shell:
It is used to open the python shell.
```bash
python manage.py shell
```
## testconnection:
It is used to test the various services connection.
```bash
python manage.py testconnection
```