import os  # noqa
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

STAGING = PROD = DEV = LOCAL = False

if Path(os.path.join(os.path.dirname(BASE_DIR), '..', '..', 'init', 'staging_check_file')).is_file():
    STAGING = True
elif Path(os.path.join(os.path.dirname(BASE_DIR), '..', '..', 'init', 'prod_check_file')).is_file():
    PROD = True
elif Path(os.path.join(os.path.dirname(BASE_DIR), '..', '..', 'init', 'dev_check_file')).is_file():
    DEV = True
else:
    LOCAL = True


if PROD:
    BLINK_ADMIN_BASE_URL = "https://api.admin.blinklastmile.com/"
    CLIENT_ID = "cqmqSIfM0LxmCMvNWz1SNByOVAZ0XIm2algUT6Ib"
    CLIENT_SECRET = "cUGfWRgf1yTcOUxgdrNZXwAmepzfam5Fta31QzX6SSYslhdZkfJ48pIc8IFYvrfo0KPggeP1oxj4ifsMklh8DlN7qjC4Y9RrukcERZYsCHEPDKIIgYwhicvV4tmhwWPu"
elif STAGING:
    BLINK_ADMIN_BASE_URL = "https://api.admin.staging.blinklastmile.com/"
    CLIENT_ID = "cqmqSIfM0LxmCMvNWz1SNByOVAZ0XIm2algUT6Ib"
    CLIENT_SECRET = "cUGfWRgf1yTcOUxgdrNZXwAmepzfam5Fta31QzX6SSYslhdZkfJ48pIc8IFYvrfo0KPggeP1oxj4ifsMklh8DlN7qjC4Y9RrukcERZYsCHEPDKIIgYwhicvV4tmhwWPu"
elif DEV:
    BLINK_ADMIN_BASE_URL = "https://api.admin.dev.blinklastmile.com/"
    CLIENT_ID = "cqmqSIfM0LxmCMvNWz1SNByOVAZ0XIm2algUT6Ia"
    CLIENT_SECRET = "cUGfWRgf1yTcOUxgdrNZXwAmepzfam5Fta31QzX6SSYslhdZkfJ48pIc8IFYvrfo0KPggeP1oxj4ifsMklh8DlN7qjC4Y9RrukcERZYsCHEPDKIIgYwhicvV4tmhwWPt"
elif LOCAL:
    BLINK_ADMIN_BASE_URL = "http://localhost:8000/"
    CLIENT_ID = "cqmqSIfM0LxmCMvNWz1SNByOVAZ0XIm2algUT6Ia"
    CLIENT_SECRET = "cUGfWRgf1yTcOUxgdrNZXwAmepzfam5Fta31QzX6SSYslhdZkfJ48pIc8IFYvrfo0KPggeP1oxj4ifsMklh8DlN7qjC4Y9RrukcERZYsCHEPDKIIgYwhicvV4tmhwWPt"
