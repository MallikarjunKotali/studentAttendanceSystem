
from flask import Flask, render_template, request
from flask_pymongo import PyMongo
from authentication import auth
from batch import batch
from subject import subject
from faculty import faculty
from student import student
from attendance import attendance
from database import Database, MBA_Database
from pymongo import MongoClient

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/Attendance"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.secret_key = "Mk_Empire"
mongo = PyMongo(app)
db = Database()
db = MBA_Database()

app.register_blueprint(auth)
app.register_blueprint(batch)
app.register_blueprint(subject)
app.register_blueprint(faculty)
app.register_blueprint(student)
app.register_blueprint(attendance)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showStream')
def showStream():
    return render_template('showStream.html')

@app.route('/MCA_stream')
def batchDetails():
    batches = db.MCAbatches.find({}, {"batch": 1})
    return render_template('adminBatches.html', batches=batches)



@app.route('/MCA_Admin')
def adminMCA():
    return render_template('MCA_Admin.html')


@app.route('/MBA_Admin')
def adminMBA():
    return render_template('MBA_Admin.html')


@app.route('/MBA_Subjects')
def MBA_Subjects():
    return render_template('MBA_Subjects.html')


if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, jsonify, render_template, request, redirect, send_file, session
# from flask_pymongo import PyMongo, MongoClient
# from datetime import datetime

# import pandas as pd

# mk = Flask(__name__)
# mk.config["MONGO_URI"] = "mongodb://127.0.0.1:27017/Attendance"
# mk.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
# mongo = PyMongo(mk)
# mk.secret_key = "Mk_Empire"


# #Database For MCA Department
# client_MCA = MongoClient("mongodb://127.0.0.1:27017")
# db = client_MCA['Attendance']
# MCAbatches = db['All_Batches']
# register = db['facultyRegister']
# MCA_subjects = db['subjectDetails']
# MCA_faculty = db['facultiesList']
# MCA_Students = db['studentList']
# MCA_Attendance = db['attendance']




# @mk.route('/')
# def index():
#     return render_template('index.html')

# @mk.route('/showStream')
# def showStream():
#     return render_template('showStream.html')


# #Faculty Dashboard
# @mk.route('/register', methods = ['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         error = []
#         message = []
#         try:
#             if len(password) >=6  and len(password)<= 12:
#                 if mongo.db.facultyRegister.find_one({'email': email, 'password': password}):
#                     error.append("User Already Existed")
#                 else:
#                     mongo.db.facultyRegister.insert_one({'email': email, 'password': password})
#                     message.append("Account Created Succssfully...!")
#             else:
#                 error.append("Password must be greater than 6 and less than 12 character")        
#         except Exception as e:
#             print("Error", e)
        
#         if error:
#             return render_template('register.html', err=error)
#         else:
#             return render_template('register.html', msg=message)

#     return render_template('register.html')


# @mk.route('/facultyLogin', methods = ['GET', 'POST'])
# def facultyLogin():
#     passw = "Invalid Email or Password"
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']

#         user = mongo.db.facultyRegister.find_one({'email': email, 'password': password})
#         if user:
#             session['email'] = email
#             return render_template('showStream.html')
#         return render_template('facultyLogin.html', passw=passw)
#     return render_template('facultyLogin.html')

# @mk.route('/logout')
# def logout():
#     session.clear()
#     session['user_id']= False
#     return redirect('/')


# @mk.route('/facultyBatches')
# def facultyBatches():
#     batches = MCAbatches.find({}, {'batch': 1})
#     return render_template('facultyBatches.html', batches=batches)

# @mk.route('/MCA_stream')
# def batchDetails():
#     batches = MCAbatches.find({}, {"batch": 1})
#     return render_template('adminBatches.html', batches=batches) 


# @mk.route('/getSubjects/<semester>', methods=['GET'])
# def get_subjects(semester):
#     subjects = MCA_subjects.find({'semester': semester}, {'_id': 0, 'subName': 1})
#     subject_list = [subject['subName'] for subject in subjects]
#     return jsonify(subject_list)


# @mk.route('/findStudents', methods= ['GET', 'POST'])
# def findStudents():
#     students = []
#     batches = MCAbatches.find({}, {'batch': 1})
#     error_message = None
#     semesters = MCA_subjects.distinct('semester')
#     if request.method == 'POST':
#         batch = request.form.get('batch')
#         division = request.form.get('division')

#         if batch == "Select Batch" or division == "Select Division":
#             error_message = "Please Select Batch and Division. All Fields are Required"
#             return render_template("findStudents.html", batches=batches, error_message=error_message)

#         students = list(MCA_Students.find({'batch': batch, 'division': division}))

#         if students:
#             return render_template('markAttendance.html', students=students, semesters=semesters, batch=batch, division=division)
        
#         if not students:
#             error_message = "No Students Found For The Selected Fields."
#     return render_template('findStudents.html', batches=batches,error_message=error_message)


# @mk.route('/takeAttendance', methods=['GET', 'POST'])
# def mark_attendance():
#     sdata = []
#     semesters = MCA_subjects.distinct('semester')
#     students = None  
#     try:
#         if request.method == 'POST':
#             date = request.form['date']
#             time = request.form['time']
#             selected_semester = request.form['semester']
#             subject_name = request.form['subject']
#             month = request.form['month']
#             batch = request.form['batch']
#             division = request.form['division']

#             # Check if all fields are filled
#             if time == "Select Time" or selected_semester == "Select Semester" or subject_name == "Select Subject" or month == "Select Month":
#                 error_msg = "All Fields are required. Please Select all Fields!"
#                 return render_template('markAttendance.html', error=error_msg, semesters=semesters)

#             # Check if attendance already marked for the same parameters
#             existing_data = MCA_Attendance.find_one({
#                 'date': date,
#                 'time': time,
#                 'semester': selected_semester,
#                 'subject_name': subject_name,
#                 'month': month,
#                 'batch': batch,
#                 'division': division
#             })
#             if existing_data:
#                 error_msg = "Attendance already exists for the selected parameters."
#                 return render_template('markAttendance.html', error=error_msg, semesters=semesters)

#             # Retrieve only the selected students
#             students = MCA_Students.find({'batch': batch, 'division': division})

#             # Process attendance for each selected student
#             for student in students:
#                 roll = student['roll']
#                 name = student['name']

#                 if request.form.get(f'attendance_{roll}_{name}'):
#                     attendance_value = 'P'
#                 else:
#                     attendance_value = 'A'

#                 student_data = {
#                     'batch': batch,
#                     'date': date,
#                     'time': time,
#                     'roll': roll,
#                     'name': name,
#                     'semester': selected_semester,
#                     'division': division,
#                     'subject_name': subject_name,
#                     'month': month,
#                     'attendance': attendance_value
#                 }
#                 MCA_Attendance.insert_one(student_data)

#             sdata.append("Attendance Marked Successfully.")
#             # Fetch students again after marking attendance to display them
#             students = MCA_Students.find({'batch': batch, 'division': division})
#             return render_template('markAttendance.html', data=sdata, students=students, semesters=semesters)
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     return render_template('markAttendance.html', data=sdata, students=students, semesters=semesters)


# @mk.route("/monthlyReport", methods=["GET", "POST"])
# def generate_report():
#     batches = MCAbatches.find({}, {'batch': 1})
#     semesters = MCA_subjects.distinct('semester')

#     if request.method == "POST":
#         batch = request.form['batch']
#         division = request.form['division']
#         subject_name = request.form['subject_name']
#         semester = request.form['semester']
#         selected_month = request.form['month']


#         if batch == "Select Batch" or division=="Select Division" or subject_name=="Select Subject" or semester=="Select Semester" or selected_month=="Select Month":
#             error="Please Select All Fields. All Fields are Required to Generate the Report"
#             return render_template("monthlyReport.html", batches=batches, semesters=semesters, error=error )

#         # Fetch attendance data based on the selected criteria
#         selected_attendance = MCA_Attendance.find({"batch": batch, "division":division, "semester": semester, "subject_name": subject_name, "month": selected_month})

#         distinct_dates = MCA_Attendance.distinct('date', {
#             "batch": batch,
#             "division": division,
#             "semester": semester,
#             "subject_name": subject_name,
#             "month": selected_month
#         })

#         student_attendance = {}

#         for attendance_record in selected_attendance:
#             student_roll = attendance_record['roll']

#             student_details = MCA_Students.find_one({"roll": student_roll})

#             if student_details:
#                 if student_roll not in student_attendance:
#                     student_attendance[student_roll] = {
#                         'batch': student_details['batch'],
#                         'name': student_details['name'],
#                         'division': student_details['division'],
#                         'attendance_by_date': {date: 'A' for date in distinct_dates},
#                         'total_lectures': 0,
#                         'attended_lectures': 0
#                     }

#                 student_attendance[student_roll]['total_lectures'] += 1
                
#                 date = attendance_record['date']
#                 student_attendance[student_roll]['attendance_by_date'][date] = attendance_record['attendance']

#                 if attendance_record['attendance'] == "P":
#                     student_attendance[student_roll]['attended_lectures'] += 1

#         # Calculate attendance percentage for each student
#         total_lectures = 0
#         student_percentages = {}
#         for student_roll, data in student_attendance.items():
#             total_lectures = data['total_lectures']
#             attended_lectures = data['attended_lectures']

#             if total_lectures > 0:
#                 attendance_percentage = (attended_lectures / total_lectures) * 100
#             else:
#                 attendance_percentage = 0

#             student_percentages[student_roll] = {
#                 'batch': data['batch'],
#                 'name': data['name'],
#                 'division': data['division'],
#                 'percentage': attendance_percentage
#             }
#         subject_doc = MCA_subjects.find_one({"subName": subject_name})

#         if subject_doc:
#             faculty_name = subject_doc.get('facultyName', 'Faculty not found')
#         else:
#             faculty_name = 'Faculty not found'

#         return render_template("attendanceReport.html", batch=batch, division=division, semester=semester, student_percentages=student_percentages,student_attendance=student_attendance, 
#                                selected_month=selected_month, faculty_name=faculty_name,
#                                subject_name=subject_name, total_lectures=total_lectures, distinct_dates=distinct_dates)
#     return render_template("monthlyReport.html", batches=batches, semesters=semesters)


# @mk.route("/saveToExcel", methods=["POST"])
# def save_to_excel():
#     subject_name = request.form['subject_name']
#     batch = request.form['batch']
#     division = request.form['division']
#     semester = request.form['semester']
#     selected_month = request.form['month']

#     # Filter attendance records based on form data
#     selected_attendance = MCA_Attendance.find({
#         "batch": batch,
#         "division": division,
#         "semester": semester,
#         "subject_name": subject_name,
#         "month": selected_month
#     })

#     student_attendance = {}
#     dates = set()
#     for attendance_record in selected_attendance:
#         student_roll = attendance_record['roll']
#         student_details = MCA_Students.find_one({"roll": student_roll})

#         if student_details:
#             if student_roll not in student_attendance:
#                 student_attendance[student_roll] = {
#                     'roll': student_details['roll'],
#                     'name': student_details['name'],
#                     'attendance_by_date': {},
#                     'total_lectures': 0,
#                     'attended_lectures': 0,
#                     'batch': student_details.get('batch', 'Unknown Batch')
#                 }

#             student_attendance[student_roll]['total_lectures'] += 1
#             date = attendance_record['date']
#             dates.add(date)
#             student_attendance[student_roll]['attendance_by_date'][date] = attendance_record['attendance']

#             if attendance_record['attendance'] == "P":
#                 student_attendance[student_roll]['attended_lectures'] += 1

#     for student_roll, data in student_attendance.items():
#         total_lectures = data['total_lectures']
#         attended_lectures = data['attended_lectures']
#         if total_lectures > 0:
#             attendance_percentage = (attended_lectures / total_lectures) * 100
#         else:
#             attendance_percentage = 0
#         student_attendance[student_roll]['percentage'] = attendance_percentage

#     # Fetch faculty name based on the selected subject name
#     subject_doc = MCA_subjects.find_one({"subName": subject_name})
#     faculty_name = subject_doc.get('facultyName', 'Faculty not found')

#     # Create DataFrame from student attendance
#     df_columns = ['Batch', 'Subject Name', 'No. of Lectures', 'Faculty Name']
#     df_data = [[batch, subject_name, len(dates), faculty_name]]
#     batch_subject_df = pd.DataFrame(df_data, columns=df_columns)

#     df_columns = ['Roll No', 'Student Name'] + sorted(dates) + ['Total Lectures', 'Attended Lectures', 'Attendance Percentage']
#     df_data = []
#     for student_roll, data in student_attendance.items():
#         row = [data['roll'], data['name']]
#         for date in sorted(dates):
#             row.append(data['attendance_by_date'].get(date, '-'))
#         row += [data['total_lectures'], data['attended_lectures'], data['percentage']]
#         df_data.append(row)

#     attendance_df = pd.DataFrame(df_data, columns=df_columns)

#     # Save DataFrames to an Excel file
#     excel_filename = 'attendance_report.xlsx'
#     with pd.ExcelWriter(excel_filename) as writer:
#         batch_subject_df.to_excel(writer, index=False)
#         attendance_df.to_excel(writer, index=False, startrow=2)

#     # Provide the Excel file for download
#     return send_file(excel_filename, as_attachment=True)




# #MCA Admin Panel
# @mk.route('/adminLogin', methods=['GET', 'POST'])
# def adminLogin():
#     passw = 'Invalid username or Password'
#     if request.method == 'POST':
#         adminEmail = request.form['adminEmail']
#         password = request.form['password']

#         admin = mongo.db.adminLogin.find_one({'adminEmail': adminEmail, 'password': password})
#         if admin:
#             session['adminEmail'] = adminEmail
#             return render_template('showStream.html')
#         return render_template('adminLogin.html', passw=passw)
#     return render_template('adminLogin.html')


# @mk.route('/MCA_Admin')
# def adminMCA():
#     return render_template('MCA_Admin.html')

# #Adding MCA Batches
# @mk.route('/MCA_Batch', methods = ['GET', 'POST'])
# def MCA_Batch():
#     error=""
#     msg=""
#     batches= MCAbatches.find()
#     if request.method == 'POST':
#         batch = request.form['batch']

#         existing_batch = MCAbatches.find_one({'batch': batch})
#         if existing_batch:
#             error = "Batch Already Existed"
#         else:
#             MCAbatches.insert_one({'batch': batch})
#             msg = "New Batch Added Successfully!"
#         return render_template('MCA_Batch.html', msg=msg, error=error, batches=batches)    
#     return render_template('MCA_Batch.html', batches=batches)

# @mk.route('/delMCA_Batch', methods = ['POST'])
# def delete_Batch():
#     batch = request.form['batch']
#     MCAbatches.delete_one({'batch': batch})
#     deletion_message = "Batch Deleted Successfully!"
#     batches = MBAbatches.find()
#     return render_template('MCA_Batch.html', deletion_message=deletion_message, batches=batches)


# #Adding Subjects Based on Semester
# @mk.route('/MCA_Subjects', methods=['GET', 'POST'])
# def MCA_Subjects():
#     exists = ""
#     msg = ""
#     deletion_message = ""
#     subjects = MCA_subjects.find()
#     facultyList = MCA_faculty.find()

#     subjects_by_semester = {}
#     for subject in subjects:
#         semester = subject['semester']
#         if semester not in subjects_by_semester:
#             subjects_by_semester[semester] = []
#         subjects_by_semester[semester].append(subject)

#     semesters = subjects_by_semester.keys()

#     if request.method == 'POST':
#         # Check if the form is for deleting a subject
#         if 'deleteSubCode' in request.form:
#             subCode = request.form['deleteSubCode']
#             MCA_subjects.delete_one({'subCode': subCode})
#             deletion_message = "Subject Deleted Successfully!"
#         else:
#             # Form submission for adding a new subject
#             semester = request.form['semester']
#             subCode = request.form['subCode']
#             subName = request.form['subName']
#             facultyName = request.form['facultyName']

#             if semester == "Select Semester" or facultyName == "Select Faculty Name":
#                 error_msg = "Please select All Fields"
#                 return render_template("MCA_Subjects.html", error_msg=error_msg, facultyList=facultyList,
#                                        subjects_by_semester=subjects_by_semester, subjects=subjects,semesters=semesters)

#             existing_subject = MCA_subjects.find_one({
#                 'semester': semester,
#                 'subCode': subCode,
#                 'subName': subName,
#                 'facultyName': facultyName
#             })

#             if existing_subject:
#                 exists = "Semester, Subject code, and Subject Name already Existed."
#             else:
#                 MCA_subjects.insert_one({
#                     'semester': semester, 'subCode': subCode,
#                     'subName': subName, 'facultyName': facultyName
#                 })
#                 msg = "Subject added successfully!"
            
#     return render_template('MCA_Subjects.html', msg=msg, exists=exists, subjects=subjects,
#                            semesters=semesters, facultyList=facultyList,
#                            subjects_by_semester=subjects_by_semester, deletion_message=deletion_message)

# @mk.route('/updateMCA_Subjects', methods=['GET', 'POST'])
# def updateMCA_Subjects():
#     msg = ''
#     error = ''
    
#     if request.method == 'GET':
#         subCode = request.args.get('subCode')
#         subName = request.args.get('subName')
#         facultyName = request.args.get('facultyName')
#         return render_template('updateMCA_Subjects.html', subCode=subCode, subName=subName, facultyName=facultyName)
    
#     elif request.method == 'POST':
#         subCode = request.form['subCode']
#         subName = request.form['subName']
#         facultyName = request.form['facultyName']
        
#         # Find the existing student document to update
#         existing_student = MCA_subjects.find_one({'subCode': subCode})
#         if existing_student:
#             update_result = MCA_subjects.update_one({'subCode': subCode}, {'$set': {'subCode': subCode, 'subName': subName, 'facultyName': facultyName}})
            
#             if update_result.modified_count > 0:
#                 msg = "Subject Details has been updated successfully."
#             else:
#                 error = "Failed to update Subject Details"
#         else:
#             error = "Subject not found."
#         return render_template('updateMCA_Subjects.html', error=error, msg=msg, subCode=subCode, subName=subName, facultyName=facultyName)
#     return render_template('updateMCA_Subjects.html')


# #Adding Faculty with their Designation
# @mk.route('/MCA_Faculty', methods = ['GET', 'POST'])
# def MCA_Faculty():
#     error=""
#     msg=""
#     facultiesList = MCA_faculty.find()
#     if request.method == 'POST':
#         name = request.form['name']
#         designation = request.form['designation']

#         existing_faculty = MCA_faculty.find_one({'name': name, 'design': designation})
#         if existing_faculty:
#             error = "Faculty Already Existed"
#         else:
#             MCA_faculty.insert_one({'name': name, 'design': designation})
#             msg = "New Faculty Added Successfully!"
#         return render_template('MCA_Faculty.html', msg=msg, error=error, facultiesList=facultiesList)    
#     return render_template('MCA_Faculty.html', facultiesList=facultiesList)


# #Adding Students According to Batches and Division
# @mk.route('/addMCAStudents', methods=['GET', 'POST'])
# def addStudents():
#     msg = ""
#     error = ""
#     batches = MCAbatches.find()

#     if request.method == 'POST':
#         batch = request.form['batch']
#         division = request.form['division']
#         file = request.files['file']

#         if batch == "Select Batch" or division == "Select Division":
#             error = "Please Select Batch and Division. All Fields are Required"
#             return render_template("addMCAStudents.html", batches=batches, error=error)


#         if file.filename != '':
#             try:
#                 df = pd.read_excel(file)

#                 existing_data_cursor = MCA_Students.find({'batch': batch, 'division': division})
#                 existing_data_df = pd.DataFrame(list(existing_data_cursor))

#                 if existing_data_df.empty:
#                     df['batch'] = batch
#                     df['division'] = division
#                     MCA_Students.insert_many(df.to_dict('records'))
#                     msg = "Students Data Successfully uploaded!"
#                 else:
#                     common_columns = set(df.columns).intersection(existing_data_df.columns)

#                     if 'roll_number' in common_columns:
#                         common_columns.remove('roll_number')

#                     existing_data = pd.merge(
#                         df,
#                         existing_data_df,
#                         left_on='Roll No',
#                         right_on='roll_number',
#                         how='inner',
#                         suffixes=('', '_existing')
#                     )

#                     if existing_data.empty:
#                         df['batch'] = batch
#                         df['division'] = division
#                         MCA_Students.insert_many(df.to_dict('records'))
#                         msg = "Students Data Successfully uploaded!"
#                     else:
#                         error_roll_numbers = existing_data['Roll No'].tolist()
#                         error = f"Students Data {', '.join(map(str, error_roll_numbers))} are already existed!"
#             except Exception as e:
#                 error = f"An error occurred: {e}"
#                 print(error)
#     return render_template("addMCAStudents.html", batches=batches, error=error, msg=msg)

# @mk.route('/update_student', methods=['GET', 'POST'])
# def updateStudent():
#     msg = ''
#     error = ''
    
#     if request.method == 'GET':
#         batch = request.args.get('batch')
#         division = request.args.get('division')
#         roll = request.args.get('roll')
#         name = request.args.get('name')
#         return render_template('update_student.html', roll=roll, name=name, batch=batch, division=division)
    
#     elif request.method == 'POST':
#         batch = request.form['batch']
#         division = request.form['division']
#         roll = request.form['roll']
#         name = request.form['name']
        
#         # Find the existing student document to update
#         existing_student = MCA_Students.find_one({'roll': roll})
#         if existing_student:
#             update_result = MCA_Students.update_one({'roll': roll}, {'$set': {'batch': batch, 'division': division, 'name': name}})
            
#             if update_result.modified_count > 0:
#                 msg = "Student data has been updated successfully."
#             else:
#                 error = "Failed to update student data."
#         else:
#             error = "Student not found."
#         return render_template('update_student.html', error=error, msg=msg, roll=roll, name=name, batch=batch, division=division)
#     return render_template('update_student.html')


#Fetching Students Based on Batch and Division
# @mk.route('/fetchMCA_students', methods=['GET', 'POST'])
# def fetchStudent():
#     error = ''
#     batches = MCAbatches.find({}, {'batch': 1})
#     num_students = 0 
#     students = []
#     batch = '' 
#     division = '' 
#     if request.method == 'POST':
#         batch = request.form['batch']
#         division = request.form['division']
        
#         if batch == "Select Batch" or division == "Select Division":
#             error = "Please Select Batch and Division. All Fields are Required"
#             return render_template("fetchMCA_students.html", batches=batches, error=error)

#         students = MCA_Students.find({'batch': batch, 'division': division})
#         num_students = MCA_Students.count_documents({'batch': batch, 'division': division})

#         if num_students == 0:
#             error = "No students found for the selected batch and division."
#     return render_template('fetchMCA_students.html', batches=batches, students=students, batch=batch, division=division, num_students=num_students, error=error)

# #===========================================================================================
# #===========================================================================================
# #===========================================================================================



# #Database For MBA Department
client_MBA = MongoClient("mongodb://127.0.0.1:27017/")
MBAdb = client_MBA['MBA_Attendance']
MBAbatches = MBAdb['MBABatches']
MBA_sem_one = MBAdb['Semester_I']
MBA_sem_two = MBAdb['Semester_II']
MBA_semIII = MBAdb['Semester_III']
MBA_semIV = MBAdb['Semester_IV']
MBA_faculty = MBAdb['facultiesList']
MBAStudents = MBAdb['studentList']
MBA_SemIAttendance = MBAdb['SemI_attendance']


# #MBA Faculty Panel
@app.route('/MBA_Semesters')
def MBA_Semesters():
    return render_template('MBA_Semesters.html')


@app.route('/searchSemI', methods = ['GET','POST'])
def searchSemI():
    students = []
    error_message = None
    subjectList = MBA_sem_one.find()
    if request.method == 'POST':
        batch = request.form.get('batch')
        division = request.form.get('division')

        students = list(MBAStudents.find({'batch': batch, 'division': division}))

        if students:
            return render_template('mark_SemIAttendance.html', students=students, subjectList=subjectList)
        
        if not students:
            error_message = "No Students Found For The Selected Fields."

    batches = MBAbatches.find({}, {'batch': 1})
    return render_template('searchSemI.html', batches=batches, error_message=error_message)


@app.route('/take_SemIAttendance', methods=['GET', 'POST'])
def mark_SemIAttendance():
    sdata = ""
    subjectList = MBA_sem_one.find()
    students = None  
    try:
        if request.method == 'POST':
            date = request.form['date']
            time = request.form['time']
            selected_semester = request.form['semester']
            subject_name = request.form['subject']
            month = request.form['month']
            batch = request.form['batch']
            division = request.form['division']


            if time == "Select Time" or selected_semester == "Select Semester" or subject_name == "Select Subject" or month == "Select Month":
                error_msg = "All Fields are required. Please Select all Fields!"
                return render_template('mark_SemIAttendance.html', data=sdata, error=error_msg, subjectList=subjectList, students=students)

            existing_data = MBA_SemIAttendance.find_one({
                'date': date,
                'time': time,
                'semester': selected_semester,
                'subject_name': subject_name,
                'month': month,
                'batch': batch,
                'division': division
            })
            if existing_data:
                error_msg = "Attendance already exists for the selected parameters."
                return render_template('mark_SemIAttendance.html', error=error_msg, subjectList=subjectList, students=students)
            
            # Iterate through form data to get attendance for each student
            for key, value in request.form.items():
                if key.startswith("attendance_"):
                    roll = key.split("_")[1]  # Extract roll number from form field name
                    name = request.form[f"name_{roll}"]  # Get student name from hidden field

                    # Check if attendance checkbox is checked
                    if value == "1":
                        attendance_value = 'P'
                    else:
                        attendance_value = 'A'

                    # Insert attendance data into database
                    student_data = {
                        'batch': batch,
                        'date': date,
                        'time': time,
                        'roll': roll,
                        'name': name,
                        'semester': selected_semester,
                        'division': division,
                        'subject_name': subject_name,
                        'month': month,
                        'attendance': attendance_value
                    }
                    MBA_SemIAttendance.insert_one(student_data)
            
            sdata = "Attendance Marked Successfully."

            students = MBAStudents.find({'batch': batch, 'division': division})
            return render_template('mark_SemIAttendance.html', data=sdata, students=students, subjectList=subjectList)
    except Exception as e:
        print(f"An error occurred: {e}")
    return render_template('mark_SemIAttendance.html', data=sdata, students=students, subjectList=subjectList)



# @mk.route('/searchSemII', methods = ['GET','POST'])
# def searchSemII():
#     students = []
#     error_message = None
#     subjectList = MBA_sem_two.find()
#     if request.method == 'POST':
#         batch = request.form.get('batch')
#         division = request.form.get('division')

#         students = list(MBAStudents.find({'batch': batch, 'division': division}))

#         if students:
#             return render_template('mark_SemIIAttendance.html', students=students, subjectList=subjectList)
        
#         if not students:
#             error_message = "No Students Found For The Selected Fields."

#     batches = MBAbatches.find({}, {'batch': 1})
#     return render_template('searchSemII.html', batches=batches, error_message=error_message)




# #MBA Admin Panel
# @mk.route('/MBA_Admin')
# def adminMBA():
#     return render_template('MBA_Admin.html')

# @mk.route('/MBA_Batch', methods = ['GET', 'POST'])
# def MBA_Batch():
#     error=""
#     msg=""
#     batches= MBAbatches.find()
#     if request.method == 'POST':
#         batch = request.form['batch']

#         existing_batch = MBAbatches.find_one({'batch': batch})
#         if existing_batch:
#             error = "Batch Already Existed"
#         else:
#             MBAbatches.insert_one({'batch': batch})
#             msg = "New Batch Added Successfully!"
#         return render_template('MBA_Batch.html', msg=msg, error=error, batches=batches)    
#     return render_template('MBA_Batch.html', batches=batches)

# @mk.route('/deleteBatch', methods = ['POST'])
# def delBatch():
#     batch = request.form['batch']
#     MBAbatches.delete_one({'batch': batch})
#     deletion_message = "Batch Deleted Successfully!"
#     batches = MBAbatches.find()
#     return render_template('MBA_Batch.html', deletion_message=deletion_message, batches=batches)


# @mk.route('/addMBAStudents', methods=['GET', 'POST'])
# def MBAStudent():
#     msg = ""
#     error = ""
#     batches = MBAbatches.find()

#     if request.method == 'POST':
#         batch = request.form['batch']
#         division = request.form['division']
#         file = request.files['file']

#         if batch == "Select Batch" or division == "Select Division":
#             error = "Please select batch and division. All fields are required."
#             return render_template("addMBAStudents.html", batches=batches, error=error)

#         if file.filename != '':
#             try:
#                 df = pd.read_excel(file)

#                 existing_data_cursor = MBAStudents.find({'batch': batch, 'division': division})
#                 existing_data_df = pd.DataFrame(list(existing_data_cursor))

#                 if existing_data_df.empty:
#                     df['batch'] = batch
#                     df['division'] = division
#                     MBAStudents.insert_many(df.to_dict('records'))
#                     msg = "Students data successfully uploaded!"
#                 else:
#                     common_columns = set(df.columns).intersection(existing_data_df.columns)

#                     if 'Roll No' in common_columns:  # Assuming 'Roll No' is the column name for roll numbers
#                         common_columns.remove('Roll No')

#                     existing_data = pd.merge(
#                         df,
#                         existing_data_df,
#                         left_on='Roll No',  # Use the correct column name for merging
#                         right_on='Roll No',  # Use the correct field name in MongoDB documents
#                         how='inner',
#                         suffixes=('', '_existing')
#                     )

#                     if existing_data.empty:
#                         df['batch'] = batch
#                         df['division'] = division
#                         MBAStudents.insert_many(df.to_dict('records'))
#                         msg = "Students data successfully uploaded!"
#                     else:
#                         error_roll_numbers = existing_data['Roll No'].tolist()
#                         error = f"Students Data already existed for the selected fields.!"
#             except Exception as e:
#                 error = f"An error occurred while processing the uploaded file: {str(e)}"
#                 print(error)
#     return render_template("addMBAStudents.html", batches=batches, error=error, msg=msg)

# @mk.route('/fetchMBA_students', methods=['GET', 'POST'])
# def fetchMBA():
#     error = ""
#     students = []
#     batches = MBAbatches.find({}, {'batch': 1})

#     if request.method == 'POST':
#         batch = request.form['batch']
#         division = request.form['division']

#         if batch == "Select Batch" or division == "Select Division":
#             error = "Please select batch and division. All fields are required."
#         else:
#             students_cursor = MBAStudents.find({'batch': batch, 'division': division}, {'Roll No': 1, 'Name': 1})
#             students = list(students_cursor)  # Convert cursor to list

#             if not students:
#                 error = "No students found for the selected batch and division."
#         return render_template('fetchMBA_students.html', batches=batches, batch=batch, division=division, students=students, error=error)
#     return render_template('fetchMBA_students.html', batches=batches, students=students, error=error)


# @mk.route('/updateMBA_Students', methods=['GET', 'POST'])
# def updateMBA_Students():
#     msg = ''
#     error = ''
#     if request.method == 'GET':
#         roll = request.args.get('roll')
        
#         # Find the existing student document to update
#         existing_student = MBAStudents.find_one({'Roll No': roll})
#         if existing_student:
#             batch = existing_student.get('batch', '')
#             division = existing_student.get('division', '')
#             name = existing_student.get('Name', '')
#             return render_template('updateMBA_Students.html', roll=roll, name=name, batch=batch, division=division)
#         else:
#             error = "Student not found."
#             return render_template('updateMBA_Students.html', error=error)
    
#     elif request.method == 'POST':
#         batch = request.form['batch']
#         division = request.form['division']
#         roll = request.form['roll']
#         name = request.form['name']
        
#         update_result = MBAStudents.update_one({'Roll No': roll}, {'$set': {'batch': batch, 'division': division, 'Name': name}})
        
#         if update_result.modified_count > 0:
#             msg = "Student data has been updated successfully."
#         else:
#             error = "Failed to update student data."

#         existing_student = MBAStudents.find_one({'Roll No': roll})
#         if existing_student:
#             batch = existing_student.get('batch', '')
#             division = existing_student.get('division', '')
#             name = existing_student.get('Name', '')
#             return render_template('updateMBA_Students.html', roll=roll, name=name, batch=batch, division=division, msg=msg, error=error)
#         else:
#             error = "Student not found."
#             return render_template('updateMBA_Students.html', error=error)  
#     return render_template('updateMBA_Students.html')



# #MBA Faculties List
# @mk.route('/MBA_Faculties', methods = ['GET', 'POST'])
# def MBA_Faculties():
#     error=""
#     msg=""
#     facultiesList = MBA_faculty.find()
#     if request.method == 'POST':
#         name = request.form['name']
#         designation = request.form['designation']

#         existing_faculty = MBA_faculty.find_one({'name': name, 'design': designation})
#         if existing_faculty:
#             error = "Faculty Already Existed"
#         else:
#             MBA_faculty.insert_one({'name': name, 'design': designation})
#             msg = "New Faculty Added Successfully!"
#         return render_template('MBA_Faculties.html', msg=msg, error=error, facultiesList=facultiesList)    
#     return render_template('MBA_Faculties.html', facultiesList=facultiesList)


# #Adding Subjects according to semester
# @mk.route('/MBA_Subjects')
# def MBA_Subjects():
#     return render_template('MBA_Subjects.html')

# @mk.route('/MBA_semI', methods=['GET', 'POST'])
# def MBA_semI():
#     exists = ""
#     subject = ""
#     subjectList = MBA_sem_one.find()
#     facultyList = MBA_faculty.find()
#     if request.method == 'POST':
#         subjectCode = request.form['subjectCode']
#         subjectName = request.form['subjectName']
#         facultyName = request.form['facultyName']

#         existing_subject = MBA_sem_one.find_one({
#             'subjectCode': subjectCode,
#             'subjectName': subjectName,
#             'facultyName': facultyName
#         })

#         if existing_subject:
#             exists = "Subject code and Subject Name already Existed in this semester."
#         else:
#             MBA_sem_one.insert_one({'subjectCode': subjectCode, 'subjectName': subjectName, 'facultyName': facultyName})
#             subject = "Subject added successfully!"
#         return render_template('MBA_semI.html', subject=subject, exists=exists,subjectList=subjectList, facultyList=facultyList)
#     return render_template('MBA_semI.html',subjectList=subjectList,facultyList=facultyList)


# @mk.route('/delete_subject', methods=['POST'])
# def delete_subject():
#     subjectCode = request.form['subjectCode']
#     MBA_sem_one.delete_one({'subjectCode': subjectCode})
#     deletion_message = "Subject Deleted Successfully!"
#     subjectList = MBA_sem_one.find()
#     return render_template('MBA_semI.html', deletion_message=deletion_message, subjectList=subjectList)


# #Adding Subjects for Sem II according to specialization
# @mk.route('/MBA_semII', methods=['GET', 'POST'])
# def MBA_semII():
#     exists = ""
#     msg = ""
#     subjectList = MBA_sem_two.find()
#     facultyList = MBA_faculty.find()

#     subjects_by_specialization = {}
#     for subject in subjectList:
#         specialization = subject['specialization']
#         if specialization not in subjects_by_specialization:
#             subjects_by_specialization[specialization] = []
#         subjects_by_specialization[specialization].append(subject)

#     specialization = subjects_by_specialization.keys()

#     if request.method == 'POST':
#         specialization = request.form['specialization']
#         subjectCode = request.form['subjectCode']
#         subjectName = request.form['subjectName']
#         facultyName = request.form['facultyName']

#         if specialization == "Select Specialization" or facultyName == "Select Faculty Name":
#             exists = "All Fields are Required. Please select all the fields."
#             return render_template('MBA_semII.html', exists=exists, facultyList=facultyList, subjects_by_specialization=subjects_by_specialization, 
#                                specialization=specialization, subjectList=subjectList)

#         existing_subject = MBA_sem_two.find_one({
#                 'specialization': specialization,
#                 'subjectCode': subjectCode,
#                 'subjectName': subjectName,
#                 'facultyName': facultyName
#         })
#         if existing_subject:
#             exists = "Subject code and Subject Name already Existed in this Specialization."
#         else:
#             MBA_sem_two.insert_one({'specialization': specialization, 'subjectCode': subjectCode, 
#                                 'subjectName': subjectName, 'facultyName': facultyName})
#             msg = "Subject added successfully!"
#         return render_template('MBA_semII.html', subjectList=subjectList, exists=exists, msg=msg, 
#                                facultyList=facultyList, subjects_by_specialization=subjects_by_specialization, 
#                                specialization=specialization)
#     return render_template('MBA_semII.html', subjectList=subjectList, specialization=specialization, 
#                            subjects_by_specialization=subjects_by_specialization, facultyList=facultyList)



# @mk.route('/delsemIIsubject', methods=['POST'])
# def delsemIIsubject():
#     facultyList = MBA_faculty.find()
#     deleteSubCode = request.form['deleteSubCode']
#     subject = MBA_sem_two.find_one({'subjectCode': deleteSubCode})
#     if subject:
#         MBA_sem_two.delete_one({'subjectCode': deleteSubCode})
#         deletion_message = f"Subject '{subject['subjectName']}' deleted successfully!"
#     else:
#         deletion_message = "Subject not found."
#     subjectList = MBA_sem_two.find()

#     subjects_by_specialization = {}
#     for subject in subjectList:
#         specialization = subject['specialization']
#         if specialization not in subjects_by_specialization:
#             subjects_by_specialization[specialization] = []
#         subjects_by_specialization[specialization].append(subject)
#     return render_template('MBA_semII.html', deletion_message=deletion_message, subjectList=subjectList, 
#                            subjects_by_specialization=subjects_by_specialization, facultyList=facultyList)





       

# if __name__ == '__main__':
#     mk.run(debug=True)