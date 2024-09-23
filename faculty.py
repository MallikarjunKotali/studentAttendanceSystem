from flask import Blueprint, render_template, request, flash
from database import Database, MBA_Database
from bson import ObjectId

faculty = Blueprint('faculty', __name__)
db = Database()
MBA_db= MBA_Database()

@faculty.route('/MCA_Faculty', methods = ['GET', 'POST'])
def MCA_Faculty():
    error=""
    msg=""
    facultiesList = db.MCA_faculty.find()
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']

        existing_faculty = db.MCA_faculty.find_one({'name': name, 'design': designation})
        if existing_faculty:
            error = "Faculty Already Existed"
        else:
            db.MCA_faculty.insert_one({'name': name, 'design': designation})
            msg = "New Faculty Added Successfully!"
        return render_template('MCA_Faculty.html', msg=msg, error=error, facultiesList=facultiesList)    
    return render_template('MCA_Faculty.html', facultiesList=facultiesList)


@faculty.route('/delete_faculty/<faculty_id>', methods=['GET'])
def delete_faculty(faculty_id):
    facultiesList = db.MCA_faculty.find()
    db.MCA_faculty.delete_one({'_id': ObjectId(faculty_id)})
    flash("Faculty Deleted Successfully!")
    return render_template('MCA_Faculty.html', facultiesList=facultiesList)



#Adding MBA Facutlies
@faculty.route('/MBA_Faculty', methods = ['GET', 'POST'])
def MBA_Faculty():
    error=""
    msg=""
    facultiesList = MBA_db.MBA_faculty.find()
    if request.method == 'POST':
        name = request.form['name']
        designation = request.form['designation']

        existing_faculty = MBA_db.MBA_faculty.find_one({'name': name, 'design': designation})
        if existing_faculty:
            error = "Faculty Already Existed"
        else:
            MBA_db.MBA_faculty.insert_one({'name': name, 'design': designation})
            msg = "New Faculty Added Successfully!"
        return render_template('MBA_Faculty.html', msg=msg, error=error, facultiesList=facultiesList)    
    return render_template('MBA_Faculty.html', facultiesList=facultiesList)



@faculty.route('/deleteMBA_faculty/<faculty_id>', methods=['GET'])
def deleteMBA_faculty(faculty_id):
    facultiesList = MBA_db.MBA_faculty.find()
    MBA_db.MBA_faculty.delete_one({'_id': ObjectId(faculty_id)})
    flash("Faculty Deleted Successfully!")
    return render_template('MBA_Faculty.html', facultiesList=facultiesList)