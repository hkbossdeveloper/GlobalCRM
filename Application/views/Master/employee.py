from Application import app
from flask import render_template , url_for , request ,jsonify, session , flash ,make_response,redirect
from pymongo import MongoClient
from bson import ObjectId
import json ,requests ,os, hashlib
import time
from datetime import date


client = MongoClient("mongodb+srv://GCU:03162400202@cluster0-rczww.gcp.mongodb.net/admin?authSource=admin&replicaSet=Cluster0-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true")
db = client.GlobalCRM

@app.route('/Master/Dashboard/Employees/Section')
def Mas_emp():
    if 'MasterEmail' in session:
        pageContent = {
            'title' : 'EMPLOYEES -- GLOBAL GATEWAY CRM'
        }
        departs = db.Deparments.find({'status':'Active'})
        pageContent["departs"] = departs
        departs_count = db.Deparments.find({'status':'Active'}).count()
        pageContent["DE_COUNT"] = departs_count
        em = db.Employees.find({'Emp_status':'Active'}).count()
        pageContent["EmployeeS"] = em
        return render_template('/Master/master_employees.html',pageContent=pageContent)
    else:
        return redirect('/')


@app.route('/Master/Dashboard/Employees/List')
def emp_list():
    if 'MasterEmail' in session:
        pageContent = {
            'title' : 'EMPLOYEES -- GLOBAL GATEWAY CRM'
        }
        
        newEmployess = db.Employees.aggregate([
        {
            "$lookup":
            {
                'from': "Deparments",
                'localField': "Emp_depart",
                'foreignField': "Main_ID",
                'as': "inventory_docs"
            }
        }
        ])
        pageContent['Employees'] = newEmployess
        return render_template('/Master/master_employee_list.html',pageContent=pageContent)
    else:
        return redirect('/')

@app.route('/Master/Dashboard/Employee/Create',methods=['POST'])
def Mas_emp_create():
    if request.method == 'POST':
        mycount = db.Employees.find().count()
        identity_card = request.files['emp_pro_img']
        name = request.form['emp_name']
        client_id = request.form['emp_id']
        client_cell = request.form['emp_cell']
        client_email = request.form['emp_email']
        client_city = request.form['emp_city']
        client_address = request.form['emp_address']
        client_pass = request.form['emp_pass']
        h = hashlib.md5(client_pass.encode())
        client_depart = request.form['emp_dep']
        today = date.today()
        try:
            location =   "Application/static/upload/"
            mycount = int(mycount) +1
            identity_card.save(location+str(today)+identity_card.filename)
            create_employee = {
                "_id" : str(mycount),
                'Name' : name,
                'Identity_number' : client_id,
                'Emp_cell' : client_cell,
                'Emp_email': client_email,
                'Emp_pass' : h.hexdigest(),
                'Emp_city' : client_city,
                'Emp_add' : client_address,
                'Emp_depart' : client_depart,
                'Emp_profile' : str(today)+identity_card.filename,
                'Emp_status' : 'Active',
                'Emp_Created_ON' : str(date.today()),
                'Emp_Created_BY' : session['MasterEmail']
            }
            if db.Employees.insert_one(create_employee):
                return redirect('/Master/Dashboard/Employees/Section')

        except NameError:
            return "Image Not Uploaded !"
    



@app.route('/Master/Dashboard/Department/Create',methods=["GET","POST"])
def create_depar():

    pageContent = {
                'title' : 'Departments -- GLOBAL GATEWAY CRM'
            }
    Departments = db.Deparments.aggregate([
            {
                "$lookup":
                {
                    'from': "Employees",
                    'localField': "Main_ID",
                    'foreignField': "Emp_depart",
                    'as': "Combinded"
                }
            }
            ])
    pageContent['Departments'] = Departments
    if 'MasterEmail' in session:
        if request.method == "POST":
            title = request.form['NewDepart']
            total_ids = db.Deparments.find().count()
            set_id = total_ids
            new_ID = int(set_id) +1
            NEW_DEPART = {
                'title' : title,
                'Main_ID': new_ID,
                "status" :'Active'
            }
            try:
                db.Deparments.insert_one(NEW_DEPART)
                print(NEW_DEPART)
                flash("New Department Created !",'success')
                return redirect('/Master/Dashboard/Department/Create')
            except:
                flash("Error Found !",'error')
                return redirect('/Master/Dashboard/Department/Create')
        else:
            return render_template('/Master/Department.html' , pageContent=pageContent)
    else:
        return redirect('/')

@app.route('/Master/Dashboard/Employee/<ID>')
def em_profile(ID):
    
    pageContent = {
                'title' : 'Profile -- GLOBAL GATEWAY CRM'
    }
    if 'MasterEmail' in session:
        profile = db.Employees.find_one({ "_id": ID })
        deparment = db.Deparments.find_one({ "Main_ID":profile['Emp_depart'] })
    
        pageContent['Empl'] = profile
        pageContent['DEP'] = deparment
        return render_template('/Master/em_profile.html', pageContent=pageContent)
    else:
        redirect('/')


@app.route('/Master/Dashboard/Employee/Lead/Create/<ids>/<name>')
def lead_create(ids,name):
    pageContent = {
            'title' : 'Leads -- GLOBAL GATEWAY CRM'
    }
    if 'MasterEmail' in session:
        emp = db.Employees.find({"Emp_status":"Active"})
        pageContent["EMP"] = emp
        pageContent["Setid"] = ids
        pageContent['Setname'] = name
        return render_template('/Master/master_lead.html', pageContent=pageContent)
    else:
        redirect('/')

@app.route('/Master/Dashboard/Employee/Lead/List')
def lead_list():
    pageContent = {
            'title' : 'Lead List -- GLOBAL GATEWAY CRM'
    }
    if 'MasterEmail' in session:
        emp = db.EmpLead.find({"Status" : "Pending"})
        pageContent["LEAD"] = emp
        comp_lead = db.EmpLead.find({"Status" : "Completed"})
        pageContent["LEAD_COMP"] = comp_lead
        return render_template('/Master/Lead_list.html', pageContent=pageContent)
    else:
        redirect('/')

@app.route('/Master/Dashboard/Employee/Lead/Set', methods=["POST"])
def lead_set():
    if 'MasterEmail' in session:
        worktodo = request.form['leads']
        priority = request.form['pr']
        selected_emp = request.form['selected_emp']
        today = date.today()
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        New_lead = {
            "Emp_Name" : selected_emp,
            "Emp_work" : worktodo,
            "Priority" : priority,
            "Created"  : str(today),
            "Created_time" : str(current_time),
            "Status" : "Pending",
            "Comfirm_time" : "None",
            "Complete_time": "None",
            "Reason" : "None"
        }
        if db.EmpLead.insert_one(New_lead):
            flash("Lead Created","success")
            return redirect('/Master/Dashboard/Employee/Lead/List')
    else:
        redirect('/')

@app.route('/Master/Dashboard/Employee/<delete_id>/Delete')
def del_emp(delete_id):
    if 'MasterEmail' in session:

        if db.Employees.find_one_and_delete({"_id": ObjectId(delete_id)}):
            flash("Employee Deleted")
            return redirect('/Master/Dashboard/Employees/List')
        else:
            flash("Found Some Error In Deleteing The Employee")
            return redirect('/Master/Dashboard/Employees/List')
    else:
        redirect('/')

@app.route('/Master/Dashboard/Employee/Attendence')
def set_att():
    pageContent = {
            'title' : 'Attendace -- GLOBAL GATEWAY CRM'
    }
    today = date.today()
    pageContent['today'] = today
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    pageContent['localtime'] = current_time
    pageContent['employess'] = db.Employees.find({'Emp_status':'Active'})
    pageContent["Attend"] = db.Attendence.aggregate([
        {
            "$lookup":
            {
                'from': 'Employees',
                'localField': 'emp_name',
                'foreignField': '_id',
                'as': 'Commbinded'
            },
        },
        {
            "$match":{
                "Status" : 'Active',
                "Created_Date" : str(today)
            }
        }
    ])
    return render_template('/Master/Emp_aat.html', pageContent=pageContent)

@app.route('/Master/Dashboard/Employee/Attendence/Create', methods=["POST"])
def set_create():
    if request.method == "POST":
        selected_emp = request.form['sel_emp']
        option= request.form['sel_opt']
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        today = date.today()
        if option == "Leave":
            St_L = request.form['start_date']
            ed_L = request.form['end_date']
            Reason = request.form['reason']
            leave = {
                "emp_name" : selected_emp,
                "start_time" : St_L,
                "end_time" : ed_L,
                "Reason" : Reason,
                "Created_time" : str(current_time),
                "Created_Date" : str(today),
                "Status" : "Deactive"
            }
            try:
                db.Attendence.insert_one(leave)
                flash("Leave Set ","success")
                return redirect("/Master/Dashboard/Employee/Attendence")
            except NameError:
                flash("Not Found ","error")
                return redirect("/Master/Dashboard/Employee/Attendence")
        else:
            try:
                attendace = {
                    "emp_name" : selected_emp,
                    "Created_time" : str(current_time),
                    "Created_Date" : str(today),
                    "Status" : "Active"
                }
                db.Attendence.insert_one(attendace)
                flash("Attend Set ","success")
                return redirect("/Master/Dashboard/Employee/Attendence")
            except NameError:
                flash("Not Found ","error")
                return redirect("/Master/Dashboard/Employee/Attendence")