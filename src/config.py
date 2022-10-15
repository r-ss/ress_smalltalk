import pathlib
from pydantic import BaseSettings
import pytz

"""
PROJECT'S FILE STRUCTURE

.                       < project root
├── Makefile
├── README.md
├── pyproject.toml
└── src                   < parent
    ├── main.py
    ├── config.py           < this file
    └── views
        └── info.py
"""

BASE_DIR = pathlib.Path.cwd()
SRC_DIR = pathlib.Path(__file__).parent  # path to this file

if BASE_DIR != SRC_DIR.parent:
    raise "Check directory sctructure in config.py"


PRODUCTION = False





class AppConfig(BaseSettings):
    """Using Pydantic's approach to manage application config
    Docs: https://pydantic-docs.helpmanual.io/usage/settings/
    """

    # GENERAL SETTINGS AND HOSTS
    PROJECT_NAME = "ress_smalltalk"
    BASE_DIR: str = str(BASE_DIR)
    SRC_DIR: str = str(SRC_DIR)
    PRODUCTION: bool = PRODUCTION
    DEBUG: bool = not PRODUCTION
    SECRET_KEY: str = None
    # DBHOST: str = None

    # TESTS
    TESTING_MODE: bool = False  # Must be set to True only in autotests

    # FORMATTERS
    DT_FORMAT_TECHNICAL: str = "%Y-%m-%d %H:%M:%S"
    DT_FORMAT_HUMAN: str = "%d.%m.%Y %H:%M"

    TZ = pytz.timezone('Europe/Madrid')

    # PATHS
    STORAGE: dict = {"ROOT": BASE_DIR, "UPLOADS": "%s/uploads/" % BASE_DIR}

    # ALLOWED_UPLOADS = ['jpg', 'jpeg', 'gif', 'png', 'zip', 'txt']

    # SECRETS NAMESPACE
    SECRET_KEY: str = None
    VALIDATORS_INDEXES: str
    ETHERSCAN_API_KEY: str
    ETH_FEE_ADDRESS: str
    BOT_TOKEN: str
    CHAT_ID: str

    class Config:
        """Loads secrets the dotenv file."""

        env_file: str = ".env.secrets"


config = AppConfig()
