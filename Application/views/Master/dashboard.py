from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://GCU:03162400202@cluster0-rczww.gcp.mongodb.net/admin?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db = client.GlobalCRM




@app.route('/',methods=['POST','GET'])
@app.route('/Master/login',methods=['POST','GET'])
def login():
    pageContent = {
        "title": "GGC - DASHBOARD"
    }
    return render_template('Master/Dashboard.html' , pageContent=pageContent)

