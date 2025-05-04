import csv
import matplotlib.pyplot as plt
import os
import time
import urllib3

from bs4 import BeautifulSoup as bs4
from flask import Flask

# instance of flask application
app = Flask(__name__)

# home route that returns below text when root url is accessed
@app.route("/")
def hello_world():
    http = urllib3.PoolManager()
    resp = http.request("GET", "")
    return "<p>Hello, World!</p>"

if __name__ == '__main__':  
   app.run()  
