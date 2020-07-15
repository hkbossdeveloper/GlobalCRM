from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
import datetime , pdfkit , os


@app.route('/Master/Dashboard/Leads/Create/')
def leads_create():
    pageContent = {
        "title": "GGC - LEADS PANEL"
    }
    return render_template('Master/create_leads.html', pageContent=pageContent)