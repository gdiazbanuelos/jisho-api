import sys
import flask
import json
from flask import Flask, render_template
import requests

app = flask.Flask(__name__)


@app.after_request
def set_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route('/')
def greeting():
    return flask.render_template('index.html')


@app.route('/<target>')
def makeApiCall(target):
    base_url = 'https://jisho.org/api/v1/search/words?keyword='
    api_url = base_url+target

    response = requests.get(api_url)
    if response.status_code == 200:
        dict1 = response.json()
        reading = dict1['data'][0]['japanese'][0]['reading']
        parts_of_speech = dict1['data'][0]['senses'][0]['parts_of_speech']
        parts_of_speech = ', '.join(parts_of_speech)
        translation = dict1['data'][0]['senses'][0]['english_definitions']
        translation = ', '.join(translation)

        outDict = {
            'reading': reading,
            'parts_of_speech': parts_of_speech,
            'translation' : translation        
        }
        
    outDict = json.dumps(outDict, ensure_ascii=False)
    return outDict


if __name__ == '__main__':
    print(makeApiCall('学生'))
    print(makeApiCall('買う'))
