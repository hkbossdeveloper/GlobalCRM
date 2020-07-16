from Application import app , db
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
import datetime , pdfkit , os , random
from datetime import date
x = datetime.datetime.now()

@app.route('/Master/Dashboard/Leads/Create/')
def leads_create():
    pageContent = {
        "title": "GGC - LEADS PANEL"
    }
    return render_template('Master/create_leads.html', pageContent=pageContent)



@app.route('/Master/Dashboard/Leads/List/')
def leads_list():
    pageContent = {
        "title": "GGC - LEADS LIST"
    }
    Main_lead_list = db.MainLead.find()
    pageContent['Lists'] = Main_lead_list
    return render_template('Master/leads_list.html', pageContent=pageContent)

@app.route('/Master/Dashboard/Leads/Create/POST/' , methods=["POST"])
def lead_post():
    if request.method == 'POST':
        Type = request.form['type']
        GNAME = request.form['gname']
        GEMAIL = request.form['gemail']
        GCELL = request.form['gcell']
        create_random_id = random.randrange(888888, 9999999,575)
        Token_id = "LD-"+str(create_random_id)+"-"+Type
        ToDay = str(x.day)+'-'+str(x.month)+'-'+str(x.year)
        Add_To_DB = {
            "ID" : Token_id,
            "TYPE" : Type,
            "GNAME" : GNAME,
            "GEMAIL": GEMAIL,
            "GCELL" : GCELL,
            "STATUS" : "ACTION NOT TAKEN",
            "Created" : ToDay,
            "CreatedBy" : "Master",
            "Month" : str(x.month),
            "Year" : str(x.year),
            "Day" : str(x.day)
        }
        try:
            db.MainLead.insert_one(
                Add_To_DB
            )
            flash("New Lead Created !",'success')
            return redirect('/Master/Dashboard/Leads/List/')
        except NameError:
            flash( NameError ,'error')
            return redirect('/Master/Dashboard/Leads/Create/')
