import os
import atexit

from cs import APP
from cs import CONFIG
from cs.contact_scheduler import ContactScheduler

if __name__ == '__main__':
    APP.config['SERVER_NAME'] = CONFIG['SERVER_NAME']
    APP.secret_key = os.environ['APP_SECRET_KEY']
    with APP.app_context():
        SCHEDULER = ContactScheduler()
        SCHEDULER.start()
    atexit.register(SCHEDULER.shutdown)
    APP.run(debug=False, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
