'''Database models-- python classes that inherit from SQLalchemy
database models. This allows us to declare python classes that
will be used to create the database schemas of our sqlite
database'''

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()

class User(DB.Model):
    '''creating id and username columns/schemas for a User'''
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    username = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.column(DB.BigInteger)
    #tweets = []

class Tweet(DB.Model):
    '''creating id, text, user_id, and user schemas for each Tweet'''
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    text = DB.Column(DB.Unicode(300))
    vect = DB.Column(DB.PickleType, nullable=False)
    #creating a relationship between users and tweets
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    #create a whole list of tweets to be attatched to the user
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)
