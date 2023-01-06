from flask import Flask, render_template, request
from .models import DB, User, Tweet
from .twitter import add_or_update_user
from .predict import predict_user


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    DB.init_app(app)
    #conecting app and database -- passing flask app to database
    #we are now ready to interact to our database through our routes

    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users = User.query.all())


    @app.route('/update')
    def update():
        '''get list of usernames of all users'''
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update Users')


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        #===============================================================
        #visit reset route to create sqlite db and tables within
        #once we create the app.condig code and the DB drop all and create all
        #  we should immediately access the reset route to make sure our
        # database is created in the first place, if it is everything else
        # should work like normal
        #================================================================

        return render_template('base.html', title="Reset Database")
        #we are creating database with tables or the "users" with the reset route
        #then see if you can query them from the database with the home route
    
    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f'User "{name}" was successfully added.'

            tweets = User.query.filter(User.username == name).one().tweets

        except Exception as e:
            message = f"Error adding {name}: {e}"
            tweets=[]

        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare users to themselves!'
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = '"{}" is more likely to be said by {} than {}.'.format(request.values['tweet_text'], 
                                                                             user1 if prediction else user0,
                                                                             user0 if prediction else user1)
        return render_template('prediction.html', title='Prediction', message=message)

    return app