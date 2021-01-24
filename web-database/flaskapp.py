from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
import sqlite3 as lite


app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///covid.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    IC = db.Column(db.String(32))
    temperature = db.Column(db.String(32))
    location = db.Column(db.String(32))

    db.create_all()

    def __init__(self, username, IC, temperature, location):
        self.username       = username
        self.IC         = IC
        self.temperature    = temperature
        self.location    = location


class UserSchema(ma.Schema):
    class Meta: 
        fields = ('id', 'username', 'IC', 'temperature', 'location')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


class UserManager(Resource):
    @staticmethod
    def get():
        users = User.query.all()
        return jsonify(users_schema.dump(users))
        """
        try: id = request.args['id']
        except Exception as _: id = None

        if not id:
            users = User.query.all()
            return jsonify(users_schema.dump(users))
        user = User.query.get(id)
        return jsonify(user_schema.dump(user))
        """

    @staticmethod
    def post():
        print("I received a post!")
        username = request.json['username']
        IC = request.json['IC']
        temperature = request.json['temperature']
        location = request.json['location']

        user = User(username, IC, temperature, location)
        db.session.update(user)
        db.session.commit()
        return jsonify({
            'Message': f'User, {username}, with IC {IC}, {temperature} Celsius inserted at {location}.'
        })

    @staticmethod
    def put():
        try: id = request.args['id']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the user ID' })
        user = User.query.get(id)

        username = request.json['username']
        IC = request.json['IC']
        temperature = request.json['temperature']
        location = request.json['location']

        user.username = username 
        user.IC = IC 
        user.temperature = temperature
        user.location = location

        db.session.commit()
        return jsonify({
            'Message': f'User, {username}, with IC {IC}, {temperature} Celsius altered at {location}.'
        })

    @staticmethod
    def delete():
        try: id = request.args['id']
        except Exception as _: id = None
        if not id:
            return jsonify({ 'Message': 'Must provide the user ID' })
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'Message': f'User {str(id)} deleted.'
        })


api.add_resource(UserManager, '/api/users')

if __name__ == '__main__':
    app.run(debug=True)