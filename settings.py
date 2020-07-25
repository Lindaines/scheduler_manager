import os

from dotenv import load_dotenv

load_dotenv(verbose=True)
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    ENVIRONMENT = os.getenv("ENVIRONMENT", "")

    # Config Flask
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))  # 5080
    CSRF_ENABLED = os.getenv("CSRF_ENABLED", True)
    SECRET_KEY = os.getenv("SECRET_KEY", "e6cf6d81-a23c-4712-96c8-c8e6c79cf11f")
    DEBUG = os.getenv("DEBUG", False)

    # Config MongoDB
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_DATABASE = os.getenv("MONGO_DATABASE", "scheduler-job-manager")
    MONGO_USERNAME = os.getenv("MONGO_USERNAME", "root")
    MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "KXZBE5PRfO")
    MONGO_COLLECTION_JOBS = os.getenv("MONGO_COLLECTION_JOBS", "jobs")
    MONGO_CONNECT_TIMEOUT = int(os.getenv("MONGO_CONNECT_TIMEOUT", "10000"))

    # Config RabbitMQ
    RABBIT_HOST = os.getenv("RABBIT_HOST", "localhost")
    RABBIT_PORT = int(os.getenv("RABBIT_PORT", 5672))
    RABBIT_MANAGEMENT_PORT = int(os.getenv("RABBIT_MANAGEMENT_PORT", 15672))
    RABBIT_USER = os.getenv("RABBIT_USER", "rabbitmq")
    RABBIT_PASSWORD = os.getenv("RABBIT_PASSWORD", "rabbitmq")
    RABBIT_VHOST = os.getenv("RABBIT_VHOST", "/")
    RABBIT_HEARTBEAT = int(os.getenv("RABBIT_HEARTBEAT", 80))
    EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "exc-worker")

    # Restplus
    SWAGGER_TITLE = os.getenv("SWAGGER_TITLE", "Job Scheduler Manager")
    SWAGGER_DESCRIPTION = os.getenv(
        "SWAGGER_DESCRIPTION", "Service to manage jobs"
    )
    SWAGGER_UI_DOC_EXPANSION = None  # None, "list", "full"
    RESTPLUS_VALIDATE = False
    RESTPLUS_MASK_SWAGGER = False
    ERROR_INCLUDE_MESSAGE = False
    ERROR_404_HELP = False

    #Job
    DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA = os.getenv("DESCRIPTION_ALLOWED_SPLITTED_BY_COMMMA",
        "LEGACY_DATA_IMPORT,FUND_DATA_IMPORT,INTEGRATION_DATA_IMPORT")
    MAX_TIME_ALLOWED = int(os.getenv("MAX_TIME_ALLOWED", 8))



class Development(Config):
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "DESENVOLVIMENTO")
    SWAGGER_VISIBLE = os.getenv("SWAGGER_VISIBLE", True)
    TESTING = os.getenv("TESTING", False)
    DEBUG = os.getenv("DEBUG", True)
    FLASK_ENV = os.getenv("FLASK_ENV", "development")


class Staging(Config):
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "HOMOLOGAÇÃO")
    SWAGGER_VISIBLE = os.getenv("SWAGGER_VISIBLE", True)
    DEBUG = os.getenv("DEBUG", False)
    TESTING = os.getenv("TESTING", True)
    FLASK_ENV = os.getenv("FLASK_ENV", "testing")


class Production(Config):
    ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME", "PRODUÇÃO")
    SWAGGER_VISIBLE = os.getenv("SWAGGER_VISIBLE", False)
    TESTING = os.getenv("TESTING", False)
    DEBUG = os.getenv("DEBUG", False)
    FLASK_ENV = os.getenv("FLASK_ENV", "production")


def load_config():
    envs = {
        "develop": Development,
        "development": Development,
        "staging": Staging,
        "production": Production,
        "master": Production,
    }

    return envs.get(Config.ENVIRONMENT, Development)
