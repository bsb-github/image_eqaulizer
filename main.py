import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import os
from math import sqrt
from flask import Flask, request, jsonify
global embed
embed = hub.KerasLayer(os.getcwd())

class TensorVector(object):

    def __init__(self, FileName=None):
        self.FileName = FileName

    def process(self):

        img = tf.io.read_file(self.FileName)
        img = tf.io.decode_jpeg(img, channels=3)
        img = tf.image.resize_with_pad(img, 224, 224)
        img = tf.image.convert_image_dtype(img,tf.float32)[tf.newaxis, ...]
        features = embed(img)
        feature_set = np.squeeze(features)
        return list(feature_set)
    

def cosineSim(a1,a2):
    sum = 0
    suma1 = 0
    sumb1 = 0
    for i,j in zip(a1, a2):
        suma1 += i * i
        sumb1 += j*j
        sum += i*j
    cosine_sim = sum / ((sqrt(suma1))*(sqrt(sumb1)))
    return cosine_sim



app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return jsonify({"message": "working", "code": 0})


@app.route("/score", methods=["POST"])
def index():
    image_one = request.files['image_one']
    image_one.save('iamgetwo.jpg')
    image_two = request.files['image_two']
    image_two.save('imageone.jpg')
    helper = TensorVector('iamgetwo.jpg')
    vector = helper.process()

    helper = TensorVector('imageone.jpg')
    vector2 = helper.process()
    
    similarity=cosineSim(vector, vector2)
    

    response = jsonify({"confidence": similarity})
    response.headers.add('Content-Type', 'application/json')

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", default=5000), debug=True)

