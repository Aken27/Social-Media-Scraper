from utils.file_utils import join_post_files, join_comment_files
from utils.nlp_utils import NLP
import os
import time
import datetime
import ast
from flask import *

app = Flask(__name__)
app.secret_key = 'MBM'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/twitter')
def twitterAnalysis():
    return render_template('index.html')
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
