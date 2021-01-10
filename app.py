import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.gridspec as gridspec
import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats

from math import *

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing

from flask import Flask, request, render_template, redirect, url_for, flash, jsonify

import pickle
import json

app = Flask(__name__, template_folder='templates', static_url_path="/static", static_folder='static')

@app.route('/')
def home():
    return render_template("main.html")

@app.route('/predict/', methods = ['POST'])
def predict():
    data = request.get_json()
    df_data = pd.DataFrame(data).T
    prediction = model.predict(df_data)
    return jsonify(result = round(float(prediction), 3))

@app.route('/prediction/', methods = ['POST'])
def predictSite():
    duration = float(request.form['duration'])
    width = float(request.form['width'])
    height = float(request.form['height'])
    bitrate = float(request.form['bitrate'])
    framerate = float(request.form['framerate'])
    i = float(request.form['i'])
    p = float(request.form['p'])
    b = float(request.form['b'])
    frames = float(request.form['frames'])
    i_size = float(request.form['i_size'])
    p_size = float(request.form['p_size'])
    size = float(request.form['size'])
    o_bitrate = float(request.form['o_bitrate'])
    o_framerate = float(request.form['o_framerate'])
    o_width = float(request.form['o_width'])
    o_height = float(request.form['o_height'])
    umem = float(request.form['umem'])
    
    codec = request.form['codec']
    list_codecs = ['mpeg4', 'h264', 'vp8', 'flv']
    values_codecs = [0., 0., 0., 0.]
    values_codecs[list_codecs.index(codec)] = 1
    
    o_codec = request.form['o_codec']
    list_o_codecs = ['o_mepg4', 'o_vp8', 'o_flv', 'o_h264']
    values_o_codecs = [0., 0., 0., 0.]
    values_o_codecs[list_o_codecs.index(o_codec)] = 1
    
    category = request.form['category']
    list_categories = ['Gaming', 'Entertainment', 'News & Politics', 'Autos & Vehicles', 'Travel & Events', 'People & Blogs', 'Pets & Animals', 'Sports', 'Music', 'Comedy', 'Nonprofit & Activis', 'Film & Animation', 'Science & Technology', 'Howto & Style', 'Education', 'Shows']
    values_categories = [0.] * len(list_categories)
    values_categories[list_categories.index(category)] = 1

    data = [duration, width, height, bitrate, framerate, i, p, b, frames, i_size, p_size, size, o_bitrate, o_framerate, o_width, o_height, umem] + values_codecs + values_o_codecs + values_categories
    
    df_data = pd.DataFrame(data).T
    prediction = model.predict([data])
    return render_template("result.html", utime=round(float(prediction), 3))

if __name__ == '__main__':
    model = keras.models.load_model('saves')
    app.run(debug = False, host='127.0.0.1')