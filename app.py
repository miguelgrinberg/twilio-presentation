import os

from flask import Flask, request, jsonify, render_template, abort
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import VideoGrant

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/token', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username:
        abort(401)

    if password == 'test':
        presenter = username
    else:
        presenter = ''

    # get credentials from environment variables
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    api_key = os.getenv('TWILIO_API_KEY')
    api_secret = os.getenv('TWILIO_API_SECRET')

    # create access token with credentials
    print(account_sid, api_key, api_secret, username)
    token = AccessToken(account_sid, api_key, api_secret, identity=username)
    # create a Video grant and add to token
    video_grant = VideoGrant(room='My Presentation')
    token.add_grant(video_grant)
    return jsonify(token=token.to_jwt(), presenter=presenter)
