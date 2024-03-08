from flask import Flask
from flask_cors import CORS  # Import CORS
from config.database_config import db, Database_Config
from controller.expenses_controller import Expenses_Controller
from controller.groups_controller import Groups_Controller
from controller.grouping_controller import Grouping_Controller
from controller.currency_controller import Currency_Controller
from controller.category_controller import Category_Controller
from controller.recurring_frequency_controller import Recurring_Frequency_Controller
from controller.icon_controller import Icon_Controller

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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


    app.run(debug=True, host='0.0.0.0', port=8081)
