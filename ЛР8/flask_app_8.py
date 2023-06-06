# cd "C:\\Users\Ilya\Desktop\university\4 семестр\Практикум по програмированию"
from flask import Flask, request
from flask_restful import Api, Resource
from datetime import datetime
from hashlib import sha256
import secrets
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json


# Initialize Flask app and API
app = Flask(__name__)
api = Api(app)

# Initialize database connection
engine = create_engine('sqlite:///./users.db', connect_args={'check_same_thread': False})
Base = declarative_base()
Session = sessionmaker(bind=engine)


# Define User model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(64), nullable=False)
    salt = Column(String(16), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(login='{self.login}', registered_at='{self.registered_at}')>"


# Create tables if they don't exist
Base.metadata.create_all(engine)


# Helper function to generate password hash with salt
def generate_password_hash(password, salt):
    return sha256((password + salt).encode('utf-8')).hexdigest()


# Define User resource
class UserResource(Resource):
    def post(self):
        # Get user data from request body
        data = request.get_json(force=True)
        login = data.get('login')
        password = data.get('password')

        session = Session()

        # Check if user with the same login already exists
        existing_user = session.query(User).filter_by(login=login).first()
        if existing_user:
            return {'message': 'User with the same login already exists'}, 409

        # Generate random salt
        salt = secrets.token_hex(8)

        # Generate password hash with salt
        password_hash = generate_password_hash(password, salt)

        # Store user data in database
        user = User(login=login, password_hash=password_hash, salt=salt)
        session.add(user)
        session.commit()

        # Return user data in response
        registered_at = user.registered_at.strftime('%d-%m-%Y %H:%M:%S')
        return {'id': user.id, 'login': user.login, 'registered_at': registered_at}


# Register User resource with API
api.add_resource(UserResource, '/user')


if __name__ == '__main__':
    app.run(debug=True, port=5001)
