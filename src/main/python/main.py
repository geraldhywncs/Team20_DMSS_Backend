from flask import Flask, current_app
from flask_cors import CORS  # Import CORS
from config.database_config import db, Database_Config
from controller.expenses_controller import Expenses_Controller
from controller.groups_controller import Groups_Controller
from controller.grouping_controller import Grouping_Controller
from controller.currency_controller import Currency_Controller
from controller.category_controller import Category_Controller
from controller.recurring_frequency_controller import Recurring_Frequency_Controller
from controller.icon_controller import Icon_Controller
from controller.user_controller import User_Controller
from utility.recurring_frequency_utility import Recurring_Frequency_Utility
import schedule
import threading
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def scheduler_task(flask_app):
    try:
        with flask_app.app_context():
            Recurring_Frequency_Utility().recurring_scheduler()
    except Exception as e:
        print(f'Error reading recurring frequencies: {str(e)}')

def scheduler_thread(flask_app):
    # schedule.every(1).minutes.do(scheduler_task, flask_app)
    schedule.every().day.at("00:00").do(scheduler_task, flask_app)
    while True:
        schedule.run_pending()  # Check for pending tasks
        time.sleep(1)  # Sleep for a short duration

scheduler = threading.Thread(target=scheduler_thread, args=(app,))
scheduler.start()

if __name__ == '__main__':
    app.config['SQLALCHEMY_DATABASE_URI'] = Database_Config.SQLALCHEMY_DATABASE_URI1
    app.config['SQLALCHEMY_BINDS'] = {
        'db1': Database_Config.SQLALCHEMY_DATABASE_URI1
    }
    db.init_app(app)

    with app.app_context():
        db.create_all()

    Expenses_Controller(app)
    Groups_Controller(app)
    Grouping_Controller(app)
    Currency_Controller(app)
    Category_Controller(app)
    Recurring_Frequency_Controller(app)
    Icon_Controller(app)
    User_Controller(app)

    # scheduler = threading.Thread(target=scheduler_thread)
    # scheduler.start()

    # start_recurring_frequency_batch_job()


    app.run(debug=True, host='0.0.0.0', port=5000)
