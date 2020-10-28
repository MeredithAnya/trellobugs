import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    # project dooom 
    dsn="https://4c0b4d78a85e4531a128a4730cd4c70b@o49697.ingest.sentry.io/4511291",
    integrations=[FlaskIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0
)

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.route('/')
def bugs():
    somthing()
    return 'bleep bloop'


if __name__ == '__main__':
    app.run()