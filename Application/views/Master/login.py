from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://GCU:03162400202@cluster0-rczww.gcp.mongodb.net/admin?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db = client.GlobalCRM




@app.route('/',methods=['POST','GET'])
@app.route('/Master/login',methods=['POST','GET'])
def login():
    if 'MasterEmail' in session:
        return redirect('/Master/Dashboard')
    else:
        if request.method == "POST":
            username = request.form['user_email']
            passwords = request.form['user_pass']
            total_count = db.Master.find({"Email":username}).count()
            if total_count == 0:
                flash("USERNAME NOT FOUND","error")
                return redirect('/')
            else:
                check_pass  = db.Master.find_one({"Email":username})
                result = check_pass.get('password')
                if passwords == result:
                    session['MasterEmail'] = username
                    return redirect('/Master/Dashboard')
                else:
                    flash("PASSWORD  NOT CORRECT ","error")
                    return redirect('/')
        else:
            pageContent = {
                'title' : 'GLOBAL GATEWAY CONSULT'
            }
            return render_template('Master/login.html' , pageContent=pageContent)

@app.route('/Master/logout')
def Mast_logout():
    session.pop('MasterEmail',"none")
    return redirect('/')