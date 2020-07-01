from flask import Flask
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
#from pymongo import MongoClient
# client = MongoClient("mongodb+srv://GCU:03162400202@cluster0-rczww.gcp.mongodb.net/admin?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
# db = client.GlobalCRM

from Application.views.Master import  dashboard