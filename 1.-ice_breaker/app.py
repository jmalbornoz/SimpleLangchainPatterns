# -*- coding: utf-8 -*-
"""
Created on Wed May  8 11:18:28 2024

@author: jm_al
"""
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from ice_breaker_v5 import ice_break_with

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    name = request.form['name']
    summary, profile_pic_url = ice_break_with(name=name)
    return jsonify(
        {
            'summary_and_facts': summary.to_dict(),
            'picture_url': profile_pic_url,
        }
    )
    

###############################################################################

if __name__ == "__main__":
    
     app.run(host="0.0.0.0", debug=False)

