from app.api import app
import settings

if __name__ == "__main__":
    try:
        config = settings.load_config()
        app.run(host=config.HOST, port=int(config.PORT), debug=False)
    except KeyboardInterrupt:
        pass
