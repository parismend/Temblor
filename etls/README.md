# ¿Cómo se corren las cosas del luigi?

## Run

```
PYTHONPATH='.' python -m luigi --module todo RunAll --local-scheduler
```

## Instalación de todo el show
```
pip install -r requirements.txt
```

## Requerimientos
* Python 3.6
* Idealmente pyenv


## Variables de ambiente

- *MAILGUN_API_KEY*: API KEY de la cuenta de Mailgun
- *ETL_BOX_EMAIL*: Email destino de las alertas de error
- *GOOGLE_API_KEY*: API KEY DE GOOLE
- *PATH_DANIOS*: Path del archivo de danios intermedio
- *PATH_MANZANAS*: Path de archivos de manzanas en gblob