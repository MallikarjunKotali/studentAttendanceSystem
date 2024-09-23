from flask import Blueprint, render_template, request, redirect, redirect, url_for, flash
from database import Database, MBA_Database
import pandas as pd
from bson import ObjectId

student = Blueprint('student', __name__)
db = Database()
MBA_db = MBA_Database()

#Searching MCA students by Faculty
@student.route('/findStudents', methods= ['GET', 'POST'])
def findStudents():
    students = []
    batches = db.MCAbatches.find({}, {'batch': 1})
    error_message = None
    semesters = db.MCA_subjects.distinct('semester')
    if request.method == 'POST':
        batch = request.form.get('batch')
        division = request.form.get('division')

        if batch == "Select Batch" or division == "Select Division":
            error_message = "Please Select Batch and Division. All Fields are Required"
            return render_template("findStudents.html", batches=batches, error_message=error_message)

        students = list(db.MCA_Students.find({'batch': batch, 'division': division}))

        if students:
            return render_template('markAttendance.html', students=students, semesters=semesters, batch=batch, division=division)
        
        if not students:
            error_message = "No Students Found For The Selected Fields."
    return render_template('findStudents.html', batches=batches,error_message=error_message)






#Adding MCA Students Data by Admin
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@student.route('/addMCAStudents', methods=['GET', 'POST'])
def addMCAStudents():
    batches = db.MCAbatches.find()
    if request.method == 'POST':
        if 'data' not in request.files:
            flash('No file part')
            return redirect(request.url)
        

        batch = request.form['batch']
        division = request.form['division']
        file = request.files['data']

        if batch == "Select Batch" or division == "Select Division":
            flash('Please Select all Fields. All Fields are Required')
            return render_template("addMCAStudents.html", batches=batches)
        
        if file.filename == '':
            flash('No selected file')
            return render_template('addMCAStudents.html', batches=batches)
        
        if file and allowed_file(file.filename):
            df = pd.read_excel(file)
            added_count = 0
            skipped_count = 0
            
            for index, row in df.iterrows():
                roll = row['Roll']
                name = row['Name']
                
                # Add your validation logic here
                if not roll or not name:
                    flash('Invalid data in Excel file')
                    return render_template('addMCAStudents.html', batches=batches)
                
                if db.MCA_Students.find_one({'roll': roll}):
                    skipped_count += 1
                else:
                    db.MCA_Students.insert_one({
                        'roll': roll,
                        'name': name,
                        'batch': batch,
                        'division': division
                    })
                    added_count += 1
            
            flash(f'{added_count} rows added, {skipped_count} rows skipped (already existed).')
            return render_template('addMCAStudents.html', batches=batches)
        else:
            flash('Allowed file types are xls and xlsx')
            return redirect(request.url)   
    return render_template('addMCAStudents.html', batches=batches)


#Fetching MCA Students Based on Batch and Division by Admin
@student.route('/fetchMCA_students', methods=['GET', 'POST'])
def fetchStudent():
    batches = db.MCAbatches.find({}, {'batch': 1})
    num_students = 0 
    batch = ''
    division = ''
    students = []
    
    if request.method == 'POST':
        batch = request.form['batch']
        division = request.form['division']
        
        if batch == "Select Batch" or division == "Select Division":
            flash('Please select both batch and division. All fields are required.')
            return render_template("fetchMCA_students.html", batches=batches)

        students = db.MCA_Students.find({'batch': batch, 'division': division})
        num_students = db.MCA_Students.count_documents({'batch': batch, 'division': division})

        if num_students == 0:
            flash('No students found for the selected batch and division')
    return render_template('fetchMCA_students.html', batches=batches, students=students, batch=batch, division=division, num_students=num_students)


#Updating MCA Students Data by Admin
@student.route('/update_student', methods=['GET', 'POST'])
def updateStudent():
    if request.method == 'GET':
        batch = request.args.get('batch')
        division = request.args.get('division')
        roll = request.args.get('roll')
        name = request.args.get('name')
        return render_template('update_student.html', roll=roll, name=name, batch=batch, division=division)
    
    elif request.method == 'POST':
        batch = request.form['batch']
        division = request.form['division']
        roll = request.form['roll']
        name = request.form['name']
        
        # Find the existing student document to update
        existing_student = db.MCA_Students.find_one({'roll': roll})
        if existing_student:
            update_result = db.MCA_Students.update_one({'roll': roll}, {'$set': {'batch': batch, 'division': division, 'name': name}})
            
            if update_result.modified_count > 0:
                flash('Student data has been updated successfully')
            else:
                flash('Failed to update student data')
        else:
            flash('Student not found')
        return render_template('update_student.html', roll=roll, name=name, batch=batch, division=division)
    return render_template('update_student.html')



# @student.route('/delete_student/<student_roll>', methods=['POST'])
# def deleteStudent(student_id):
#     if request.method == 'POST':
#         if request.form.get('confirm_delete'):
#             student_id_obj = ObjectId(student_id)
#             db.MCA_Students.delete_one({'_id': student_id_obj})
#             flash('Student data has been deleted successfully.')
#         else:
#             flash('Deletion canceled. Student data remains unchanged.')
#     return render_template('fetchMCA_students.html')



#==================================================================================
#==================================================================================
#==================================================================================


@student.route('/MBA_Semesters')
def MBA_Semesters():
    return render_template('MBA_Semesters.html')


@student.route('/searchSemI', methods = ['GET','POST'])
def searchSemI():
    students = []
    error_message = None
    subjectList =MBA_db.sub_semOne.find()
    if request.method == 'POST':
        batch = request.form.get('batch')
        division = request.form.get('division')

        students = list(MBA_db.MBA_Students.find({'batch': batch, 'division': division}))

        if students:
            return render_template('mark_SemIAttendance.html', students=students, subjectList=subjectList, batch=batch, division=division)
        
        if not students:
            error_message = "No Students Found For The Selected Fields."

    batches = MBA_db.MBAbatches.find({}, {'batch': 1})
    return render_template('searchSemI.html', batches=batches, error_message=error_message, subjectList=subjectList)





#Adding MBA Students Data by Admin
@student.route('/addMBAStudents', methods=['GET', 'POST'])
def addMBAStudents():
    batches = MBA_db.MBAbatches.find()
    if request.method == 'POST':
        if 'data' not in request.files:
            flash('No file part')
            return redirect(request.url)
        

        batch = request.form['batch']
        division = request.form['division']
        file = request.files['data']

        if batch == "Select Batch" or division == "Select Division":
            flash('Please Select all Fields. All Fields are Required')
            return render_template("addMBAStudents.html", batches=batches)
        
        if file.filename == '':
            flash('No selected file')
            return render_template('addMBAStudents.html', batches=batches)
        
        if file and allowed_file(file.filename):
            df = pd.read_excel(file)
            added_count = 0
            skipped_count = 0
            
            for index, row in df.iterrows():
                roll = row['Roll']
                name = row['Name']
                
                # Add your validation logic here
                if not roll or not name:
                    flash('Invalid data in Excel file')
                    return render_template('addMBAStudents.html', batches=batches)
                
                if MBA_db.MBA_Students.find_one({'roll': roll}):
                    skipped_count += 1
                else:
                    MBA_db.MBA_Students.insert_one({
                        'roll': roll,
                        'name': name,
                        'batch': batch,
                        'division': division
                    })
                    added_count += 1
            
            flash(f'{added_count} rows added, {skipped_count} rows skipped (already existed).')
            return render_template('addMBAStudents.html', batches=batches)
        else:
            flash('Allowed file types are xls and xlsx')
            return redirect(request.url)   
    return render_template('addMBAStudents.html', batches=batches)


#Fetching MBA Students Based on Batch and Division by Admin
@student.route('/fetchMBA_students', methods=['GET', 'POST'])
def fetchMBAStudent():
    batches = MBA_db.MBAbatches.find({}, {'batch': 1})
    num_students = 0 
    batch = ''
    division = ''
    students = []
    
    if request.method == 'POST':
        batch = request.form['batch']
        division = request.form['division']
        
        if batch == "Select Batch" or division == "Select Division":
            flash('Please select both batch and division. All fields are required.')
            return render_template("fetchMBA_students.html", batches=batches)

        students = MBA_db.MBA_Students.find({'batch': batch, 'division': division})
        num_students = MBA_db.MBA_Students.count_documents({'batch': batch, 'division': division})

        if num_students == 0:
            flash('No students found for the selected batch and division')
    return render_template('fetchMBA_students.html', batches=batches, students=students, batch=batch, division=division, num_students=num_students)


#Updating MBA Students Data by Admin
@student.route('/updateMBA_Students', methods=['GET', 'POST'])
def updateMBA_Students():
    if request.method == 'GET':
        batch = request.args.get('batch')
        division = request.args.get('division')
        roll = request.args.get('roll')
        name = request.args.get('name')
        return render_template('updateMBA_Students.html', roll=roll, name=name, batch=batch, division=division)
    
    elif request.method == 'POST':
        batch = request.form['batch']
        division = request.form['division']
        roll = request.form['roll']
        name = request.form['name']
        
        # Find the existing student document to update
        existing_student = MBA_db.MBA_Students.find_one({'roll': roll})
        if existing_student:
            update_result = MBA_db.MBA_Students.update_one({'roll': roll}, {'$set': {'batch': batch, 'division': division, 'name': name}})
            
            if update_result.modified_count > 0:
                flash('Student data has been updated successfully')
            else:
                flash('Failed to update student data')
        else:
            flash('Student not found')
        return render_template('updateMBA_Students.html', roll=roll, name=name, batch=batch, division=division)
    return render_template('updateMBA_Students.html')