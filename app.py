from flask import Flask, render_template, request, session
from instagram.client import InstagramAPI
import requests

app = Flask(__name__)

CONFIG = {
    'client_id': "d82bdd8b244d442f8c41b5a65b5baabf",
    'client_secret': "e1bbfba547a841639d35a4de92de875c",
    'redirect_uri': "http://localhost:5000/oauth_callback"
}

api = None
#tag_media = api.tag(tag_name="sun")
unauthenticated_api = InstagramAPI(**CONFIG)


# @app.route('/')
# def index():
#     return render_template('index.html')

@app.route('/')
def home():
    try:
        url = unauthenticated_api.get_authorize_url(scope=["likes", "comments"])
        return '<a href="%s">Connect with Instagram</a>' % url
    except Exception as e:
        print(e)


@app.route('/oauth_callback')
def on_callback():
    code = request.args.get("code")
    if not code:
        return 'Missing code'
    try:
        access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
        if not access_token:
            return 'Could not get access token'
        api = InstagramAPI(access_token=access_token, client_secret=CONFIG['client_secret'])
        session['access_token'] = access_token
        return access_token
    except Exception as e:
        print(e)
    return "hello world"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
