from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
import datetime , pdfkit , os


@app.route('/Master/Dashboard/Employee/Reports/')
def reports():
    pageContent = {
        "title": "GGC - Employee Reports"
    }
    return render_template('Master/Employee_report.html' , pageContent=pageContent)

@app.route('/Master/Dashboard/Employee/Reports/Current/Year/')
def reports_download():
    pageContent = {
        "title": "GGC - Employee Reports 2020"
    }
    x = datetime.datetime.now()
    pageContent['currentyear'] = x.year
    return render_template('Master/download_emp_current.html' , pageContent=pageContent)

@app.route('/Master/Dashboard/Employee/Attend')
def emp_attend():
    pageContent = {
        "title": "GGC - Employee Reports 2020"
    }
    x = datetime.datetime.now()
    pageContent['currentyear'] = x.year
    pageContent['currentmonth'] = x.month
    pageContent['currentday'] = x.day
    return render_template('Master/attendence_master.html' , pageContent=pageContent)



