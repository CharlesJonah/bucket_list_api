from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from application.config import Config
from main import app,db

app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
   manager.run()