from flask import Flask, render_template, redirect, url_for, request
import requests
import json

app = Flask(__name__)


@app.route('/')
def main():
    return redirect(url_for('login'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/success')
def success():
    return render_template('success.html')


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
        "redirect_uri": "<redirect_uri>",
        "client_id": "<client_id>",
        "client_secret": "<client_secret>"
    }
    response = session.post(authorize_url, headers=headers, data=data)
    try:
        access_token = json.loads(response.text)['access_token']
    except KeyError:
        return redirect(url_for('login'))

    profile_url = "https://api.line.me/v2/profile"
    profile_text = requests.get(profile_url, headers={"Authorization": "Bearer %s" % access_token}).text
    profile_json = json.loads(profile_text)

    userId = profile_json['userId']
    displayName = profile_json['displayName']
    try:
        statusMessage = profile_json['statusMessage']
    except KeyError:
        statusMessage = None
    try:
        pictureUrl = profile_json['pictureUrl']
    except KeyError:
        pictureUrl = None

    return render_template(
        'profile.html',
        userId=userId,
        displayName=displayName,
        statusMessage=statusMessage,
        pictureUrl=pictureUrl
    )


if __name__ == '__main__':
    app.run()
