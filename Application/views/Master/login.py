from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://GCU:03162400202@cluster0-rczww.gcp.mongodb.net/admin?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db = client.GlobalCRM




@app.route('/')
@app.route('/Master/login',methods=['POST'])
def login():
    if 'MasterEmail' in session:
        return redirect('/Master/Dashboard')
    else:
        if request.method == "POST":
            data = request.get_json()
            print(data.get('email'))
            total_count = db.Master.find({"Email":data.get("email")}).count()
            print(total_count)
            if total_count == 0:
                res = make_response(jsonify({"error":"Email Not Found"}),404)
                return res
            else:
                check_pass  = db.Master.find_one({"Email":data.get("email")})
                if data.get('pass') == check_pass.get('password'):
                    session['MasterEmail'] = data.get("email")
                    return redirect('/Master/Dashboard')
                else:
                    res = make_response(jsonify({"error":"Pass Not Match"}),404)
                    return res
        else:
            pageContent = {
                'title' : 'GLOBAL GATEWAY CONSULT'
            }
            return render_template('Master/login.html' , pageContent=pageContent)

@app.route('/Master/logout')
def Mast_logout():
    session.pop('MasterEmail',"none")
    return redirect('/')