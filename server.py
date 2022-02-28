from flask import Flask, render_template, jsonify, request
import json
import requests
import urllib
from random import randrange

app = Flask(__name__)

api_key = "YWBTHvQRy8ePcV2XQPgGYOttyET2hQdk"
url = "http://api.giphy.com/v1/gifs/search"
trending = "http://api.giphy.com/v1/gifs/trending"
limit = 10

@app.route("/", methods=['GET', 'POST'])
def hello():
  params = urllib.parse.urlencode({
                                  "api_key": api_key,
                                  "limit": str(limit)
                                  })
  with urllib.request.urlopen("".join((trending, "?", params))) as response:
    data = json.loads(response.read())
  list = []
  for i in range(limit):
    list.append(data["data"][i]["images"]["original"]["url"])
  return render_template("index.html", images = list, nextpage = "https://inquisitive-simplistic-lotus.glitch.me/nextpage")

@app.route("/nextpage", methods=['GET', 'POST'])
def nextpage():
  params = urllib.parse.urlencode({
                                  "api_key": api_key,
                                  "limit": str(limit),
                                  "offset": str(randrange(100))
                                  })
  with urllib.request.urlopen("".join((trending, "?", params))) as response:
    data = json.loads(response.read())
  list = []
  for i in range(limit):
    list.append(data["data"][i]["images"]["original"]["url"])
  return render_template("nextpage.html", images = list, nextpage = "https://inquisitive-simplistic-lotus.glitch.me/nextpage")

@app.route("/result", methods=['GET', 'POST'])
def result():
  params = urllib.parse.urlencode({
                          "q": request.form['query'],
                          "api_key": api_key,
                          "limit": "1"
                          })
  with urllib.request.urlopen("".join((url, "?", params))) as response:
    data = json.loads(response.read())

  image_url = data["data"][0]["images"]["original"]["url"]
  return render_template("result.html", gif_url = image_url)
  
if __name__ == "__main__":
  app.run()
