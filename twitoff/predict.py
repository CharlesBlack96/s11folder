from .models import User
import numpy as np
from sklearn.linear_model import LogisticRegression
from .twitter import vectorize_tweet






def predict_user(user0_name, user1_name, hypo_tweet_text):

    user0 = User.query.filter(user.username == user0_name).one()
    user1 = User.query.filter(user.username == user1_name).one()

    user0_vects = np.array([tweet.vect for tweet in user0.tweets])
    user1_vects = np.array([tweet.vect for tweet in user1.tweets])

    #combine np arrays into one big array with v stack
    #2d arrays
    #x matrix for training logistic regression
    vects = np.vstack([user0_vects, user1_vects])

    #create an np array of labels that corespond to user that said vectorization
    #1d arrays
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    #y_vector (target) for training logistic regression
    labels = np.concatenate([zeros, ones])

    #instantiate our logistic regression
    log_reg = LogisticRegression()

    #train our log reg
    log_reg.fit(vects, labels)

    #vecttorize our hypothetical tweet text 
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)

    #get a prediction for which user is more likely to say the text
    prediction = log_reg.predict(hypo_tweet_text.reshape(1, -1))

    #we should then print prediction immediately after writing code to test
    
    #print(prediction)

    return prediction[0]