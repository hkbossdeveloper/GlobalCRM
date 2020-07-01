from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
from pymongo import MongoClient
import json




@app.route('/',methods=['POST','GET'])
@app.route('/Master/login',methods=['POST','GET'])
def login():
    pageContent = {
        "title": "GGC - DASHBOARD"
    }
    return render_template('Master/Dashboard.html' , pageContent=pageContent)

