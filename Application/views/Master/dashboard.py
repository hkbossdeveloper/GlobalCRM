from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect


@app.route('/')
@app.route('/Master/Dashboard/')
def login():
    pageContent = {
        "title": "GGC - DASHBOARD"
    }
    return render_template('Master/Dashboard.html' , pageContent=pageContent)



@app.route('/Master/Dashboard/Employee/Create/')
def emp_create():
    pageContent = {
        "title": "GGC - Employee Create"
    }
    return render_template('Master/Employee_create.html' , pageContent=pageContent)

