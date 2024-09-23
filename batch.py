from flask import Blueprint, render_template, request, redirect, session
from database import Database, MBA_Database

batch = Blueprint('batch', __name__)
db = Database()
MBA_db = MBA_Database()

#Adding MCA Batches
@batch.route('/MCA_Batch', methods = ['GET', 'POST'])
def MCA_Batch():
    error=""
    msg=""
    batches= db.MCAbatches.find()
    if request.method == 'POST':
        batch = request.form['batch']

        existing_batch = db.MCAbatches.find_one({'batch': batch})
        if existing_batch:
            error = "Batch Already Existed"
        else:
            db.MCAbatches.insert_one({'batch': batch})
            msg = "New Batch Added Successfully!"
        return render_template('MCA_Batch.html', msg=msg, error=error, batches=batches)    
    return render_template('MCA_Batch.html', batches=batches)

#Deleting MCA Batches
@batch.route('/delMCA_Batch', methods = ['POST'])
def delete_Batch():
    batch = request.form['batch']
    db.MCAbatches.delete_one({'batch': batch})
    deletion_message = "Batch Deleted Successfully!"
    batches = db.MCAbatches.find()
    return render_template('MCA_Batch.html', deletion_message=deletion_message, batches=batches)



#Adding MBA Batches
@batch.route('/MBA_Batch', methods = ['GET', 'POST'])
def MBA_Batch():
    error=""
    msg=""
    batches= MBA_db.MBAbatches.find()
    if request.method == 'POST':
        batch = request.form['batch']

        existing_batch = MBA_db.MBAbatches.find_one({'batch': batch})
        if existing_batch:
            error = "Batch Already Existed"
        else:
            MBA_db.MBAbatches.insert_one({'batch': batch})
            msg = "New Batch Added Successfully!"
        return render_template('MCA_Batch.html', msg=msg, error=error, batches=batches)    
    return render_template('MBA_Batch.html', batches=batches)



#Deleting MBA Batches
@batch.route('/delMBA_Batch', methods = ['POST'])
def deleteMBA_Batch():
    batch = request.form['batch']
    MBA_db.MBAbatches.delete_one({'batch': batch})
    deletion_message = "Batch Deleted Successfully!"
    batches = MBA_db.MBAbatches.find()
    return render_template('MBA_Batch.html', deletion_message=deletion_message, batches=batches)