from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_jwt_extended import JWTManager
from flask_smorest import Api 

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
api = Api()
migrate = Migrate()