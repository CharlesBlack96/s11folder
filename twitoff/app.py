from flask import Flask, render_template
from .models import DB, User, Tweet
from .twitter import add_or_update_user


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

    DB.init_app(app)
    #conecting app and database -- passing flask app to database
    #we are now ready to interact to our database through our routes

    @app.route('/')
    def root():
        
        users = User.query.all()
        
        return render_template('base.html', title="Home", users=users)

    @app.route('/populate')
    def populate():
        #create some fake users in the DB
        add_or_update_user('nasa')
        add_or_update_user('ryanallred')

        return render_template('base.html', title='Populate')


    @app.route('/update')
    def update():
        '''get list of usernames of all users'''
        users = User.query.all()
        usernames = [user.username for user in users]
        for username in usernames:
            add_or_update_user(username)

        return render_template('base.html', title='Update')


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

        return render_template('base.html', title="Reset")
        #we are creating database with tables or the "users" with the reset route
        #then see if you can query them from the database with the home route
    
    return app