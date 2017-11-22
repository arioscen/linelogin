from flask import Flask, render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)


@app.route('/Index.html')
def index():
    return render_template('Index.html')


@app.route('/')
def main():
    return redirect(url_for('index'))


@app.route('/profile')
def profile():
    authorize_url = "https://api.line.me/oauth2/v2.1/token"
    session = requests.Session()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "code": request.args.get('code'),
        "redirect_uri": "https://arioscen-linelogin-flask.herokuapp.com/profile",
        "client_id": "1547929126",
        "client_secret": "b4d671b90cb6b791c12f2fc3380edb8e"
    }
    response = session.post(authorize_url, headers=headers, data=data)
    try:
        access_token = json.loads(response.text)['access_token']
    except KeyError:
        return redirect(url_for('index'))

    profile_url = "https://api.line.me/v2/profile"
    profile_text = requests.get(profile_url, headers={"Authorization": "Bearer %s" % access_token}).text
    profile_json = json.loads(profile_text)
    return render_template(
        'profile.html',
        userId=profile_json['userId'],
        displayName=profile_json['displayName'],
        statusMessage=profile_json['statusMessage'],
        pictureUrl=profile_json['pictureUrl']
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0')
