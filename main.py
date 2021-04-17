from utils.file_utils import join_post_files, join_comment_files
from utils.nlp_utils import NLP
import os
import time
import datetime
import ast
from flask import *
import tweepy
from utils.twitter_utils import get_profile_twitter, get_tweets_twitter

app = Flask(__name__)
app.secret_key = 'MBM'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/twitter',methods=['GET','POST'])
def twitter():
    # Record the start time of program execution
    api_key = "p55m9Q258cLWQnsQ786LXuUyc"
    api_secret = "vF3E9mEfZg8ddeR3dTEVSoKj1iZw3JQXDyKj4v4xlasgmipsgr"
    access_token = "1075334164704944128-IE2kW69CxUBvXReKGIe9dI2QUs6r0Z"
    access_token_secret = "XZ1gnMw0EIvKrOvuXTYva4z8LCjKh5qGiyZ6cAz3B9AI2"
    company = 'Twitter'

    # Code replacing Twitter.py
    if request.method == 'POST':
        user = request.form
        twitter_handle = user['twitteraccnt']
        print(twitter_handle)
        if twitter_handle != "":
            if twitter_handle[0] == "@":
                start = time.time()

                print('*' * 75 + '\nPhase 1: Scraping...\n' + '*' * 75)

                # Create the API object using Twitter's OAuth system
                auth = tweepy.OAuthHandler(api_key, api_secret)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)

                # If the Twitter folder is not in the company folder already, create it
                if 'Twitter' not in os.listdir('../{}'.format(company)):
                    os.mkdir('../{}/Twitter'.format(company))

                # Output files for the profile and tweets
                profile_output = "../{}/Twitter/{}_twitter_profile.csv".format(company, twitter_handle)
                tweet_output = "../{}/Twitter/{}_twitter_tweet.csv".format(company, twitter_handle)

                # Get the Twitter profile of the specified twitter handle and write it to profile_output
                get_profile_twitter(name=twitter_handle, api=api, output_file=profile_output)
                # Get the tweets of the specified twitter handle (at most num_tweets) and write it to tweet_output
                get_tweets_twitter(name=twitter_handle, api=api, output_file=tweet_output, num_tweets=1000)

                # Code replacing original main.py
                print('*' * 75 + '\nPhase 2: Natural Language Processing...\n' + '*' * 75)

                # Instantiate NLP engine
                now = datetime.datetime.strftime(datetime.datetime.now(), '[%B %d, %Y %H:%M:%S]')
                print(now + " - Starting up NLP engine...\n")

                nlp = NLP()

                # Run NLP on Twitter tweets

                nlp.process_nlp('../{}/Twitter'.format(company), company, 'Twitter tweet')

                # Delete NLP engine since we are not using anymore
                now = datetime.datetime.strftime(datetime.datetime.now(), '[%B %d, %Y %H:%M:%S]')
                print(now + " - Shutting down NLP engine...\n")
                del nlp
                NLP.count -= 1

                print('*' * 75 + '\nPhase 3: Post-Processing...\n' + '*' * 75)

                # Combine all posts/tweets and comments into 2 big files
                join_post_files('../{}'.format(company), company)
                join_comment_files('../{}'.format(company), company)

                end = time.time()
                print("Entire process finished in {} seconds!".format(end - start))
                return redirect(url_for('results'))
            else:
                flash("Please add @ before the username", "danger")

    return render_template('twitterAnalysis.html')


@app.route('/results')
def results():
    return render_template('results.html')


def execute():
    # Get the folder name where the Facebook, Instagram, LinkedIn, Twitter, and Weibo folders are stored
    with open('key_params.json', 'r') as f:
        keys = ast.literal_eval(f.read())
        company = keys['parameters']['main']['company_folder']

    # If the designated folder doesn't exist, create it
    # if company not in os.listdir('../'):
    #     os.mkdir('../{}'.format(company))

    # Record the start time of program execution
    start = time.time()

    print('*' * 75 + '\nPhase 1: Scraping...\n' + '*' * 75)

    # Scrape Instagram; runs the script on the command line
    os.system('python instagram.py')
    print()

    # Scrape Twitter; runs the script on the command line
    # os.system('python twitter.py')

    print('*' * 75 + '\nPhase 2: Natural Language Processing...\n' + '*' * 75)

    # Instantiate NLP engine
    now = datetime.datetime.strftime(datetime.datetime.now(), '[%B %d, %Y %H:%M:%S]')
    print(now + " - Starting up NLP engine...\n")
    nlp = NLP()

    # Run NLP on Instagram posts
    nlp.process_nlp('../{}/Instagram'.format(company), company, 'Instagram post')

    # Run NLP on Instagram comments
    nlp.process_nlp('../{}/Instagram'.format(company), company, 'Instagram comment')

    # Run NLP on Twitter tweets
    # nlp.process_nlp('../{}/Twitter'.format(company), company, 'Twitter tweet')

    # Delete NLP engine since we are not using anymore
    now = datetime.datetime.strftime(datetime.datetime.now(), '[%B %d, %Y %H:%M:%S]')
    print(now + " - Shutting down NLP engine...\n")
    del nlp
    NLP.count -= 1

    print('*' * 75 + '\nPhase 3: Post-Processing...\n' + '*' * 75)

    # Combine all posts/tweets and comments into 2 big files
    join_post_files('../{}'.format(company), company)
    join_comment_files('../{}'.format(company), company)

    end = time.time()
    print("Entire process finished in {} seconds!".format(end - start))


if __name__ == "__main__":
    app.run()
