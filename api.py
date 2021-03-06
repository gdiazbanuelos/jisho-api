import sys
import flask
import json
from flask import Flask, render_template
import requests
from romanji import romanjiDic

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
    target = target.lower()
    api_url = base_url+target

    response = requests.get(api_url)
    if response.status_code == 200:
        dict1 = response.json()

        index = 0
        for x in range(0, len(dict1['data'])):
            if (dict1['data'][x]['slug'][0]) == target:
                index = x
                break

        reading = dict1['data'][index]['japanese'][0]['reading']
        parts_of_speech = dict1['data'][index]['senses'][0]['parts_of_speech']
        parts_of_speech = ', '.join(parts_of_speech)
        translation = dict1['data'][index]['senses'][0]['english_definitions']
        translation = ', '.join(translation)
        if('word' in dict1['data'][index]['japanese'][0]):
            kanji = dict1['data'][index]['japanese'][0]['word']
            kanji = ''.join(kanji)
        else:
            kanji = ''
        tags = dict1['data'][index]['senses'][0]['tags']
        tags = ', '.join(tags)

        pronunciation = ''
        for x in range(0, len(reading)):
            if reading[x] in ['っ','ッ']:
                pronunciation += romanjiDic[reading[x+1]][0]
            elif reading[x] == 'ー':
                pronunciation += romanjiDic[reading[x-1]][-1]
            elif reading[x] in ['ゃ','ゅ','ょ','ャ','ュ','ョ']:
                if reading[x-1] in ['し','ち','じ','シ','チ','ジ']:
                    pronunciation = pronunciation[:-1] + romanjiDic[reading[x]][-1]
                else:
                    pronunciation = pronunciation[:-1] + romanjiDic[reading[x]]
            else:
                pronunciation += romanjiDic[reading[x]]

        pronunciation = pronunciation.replace('nm', 'mm')
        pronunciation = pronunciation.replace('nb', 'mb')
        pronunciation = pronunciation.replace('np', 'mp')

        outDict = {
            'pronunciation': pronunciation,
            'reading': reading,
            'kanji': kanji,
            'parts_of_speech': parts_of_speech,
            'translation' : translation,
            'tags' : tags
        }
        
    outDict = json.dumps(outDict, ensure_ascii=False)
    return outDict


if __name__ == '__main__':
    print(makeApiCall('学生'))
    print(makeApiCall('買う'))
    print(makeApiCall('一人っ子'))
    print(makeApiCall('持ってくる'))
    print(makeApiCall('ice cream'))
    print(makeApiCall('soccer'))
    print(makeApiCall('milk'))
    print(makeApiCall('料理人'))
    print(makeApiCall('東京'))
    print(makeApiCall('とうきょうかぶしきしじょう'))
    print(makeApiCall('徐々'))
    print(makeApiCall('コンマ'))
    print(makeApiCall('本'))
    print(makeApiCall('さんぽ'))
    print(makeApiCall('とんぼ'))
    print(makeApiCall('computer'))
    print(makeApiCall('apple'))
    print(makeApiCall('here'))
    print(makeApiCall('歳'))
    print(makeApiCall('枚'))
