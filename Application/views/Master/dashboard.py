from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
from pymongo import MongoClient
import json ,requests


client = MongoClient("mongodb+srv://GCU:03162400202@cluster0-rczww.gcp.mongodb.net/admin?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db = client.GlobalCRM

@app.route('/Master/Dashboard')
def Mas_dash():
    if 'MasterEmail' in session:
        pageContent = {
            'title' : 'GLOBAL GATEWAY CRM'
        }
        name = db.Master.find_one({'Email':session['MasterEmail']})
        total_emp = db.Employees.find().count()
        pageContent['Name'] = name.get('Name')
        pageContent['Emp_count'] = total_emp
        return render_template('/Master/Dashboard.html',pageContent=pageContent)
    else:
        return redirect('/')