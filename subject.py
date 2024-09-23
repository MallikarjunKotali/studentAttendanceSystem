from flask import Blueprint, render_template, jsonify, request, flash, url_for, redirect
from database import Database, MBA_Database
from bson import ObjectId

subject = Blueprint('subject', __name__)
db = Database()
MBA_db = MBA_Database()



@subject.route('/getSubjects/<semester>', methods=['GET'])
def get_subjects(semester):
    subjects = db.MCA_subjects.find({'semester': semester}, {'_id': 0, 'subName': 1})
    subject_list = [subject['subName'] for subject in subjects]
    return jsonify(subject_list)



# #Adding Subjects Based on Semester
@subject.route('/MCA_Subjects', methods=['GET', 'POST'])
def MCA_Subjects():
    deletion_message = ""
    subjects = db.MCA_subjects.find()
    facultyList = db.MCA_faculty.find()

    subjects_by_semester = {}
    for subject in subjects:
        semester = subject['semester']
        if semester not in subjects_by_semester:
            subjects_by_semester[semester] = []
        subjects_by_semester[semester].append(subject)

    semesters = subjects_by_semester.keys()

    if request.method == 'POST':
        semester = request.form['semester']
        subCode = request.form['subCode']
        subName = request.form['subName']
        facultyName = request.form['facultyName']

        if semester == "Select Semester" or facultyName == "Select Faculty Name":
            flash("Please select All Fields")
            return render_template("MCA_Subjects.html", facultyList=facultyList,
                                       subjects_by_semester=subjects_by_semester, subjects=subjects,semesters=semesters)

        existing_subject = db.MCA_subjects.find_one({
                'semester': semester,
                'subCode': subCode,
                'subName': subName,
                'facultyName': facultyName
        })

        if existing_subject:
            flash("Semester, Subject code, and Subject Name already Existed.")
        else:
            db.MCA_subjects.insert_one({
                    'semester': semester, 'subCode': subCode,
                    'subName': subName, 'facultyName': facultyName
                })
            flash("Subject added successfully!")
            
    return render_template("MCA_Subjects.html",subjects=subjects, semesters=semesters, facultyList=facultyList,
                           subjects_by_semester=subjects_by_semester, deletion_message=deletion_message)





@subject.route('/updateMCA_Subjects', methods=['GET', 'POST'])
def updateMCA_Subjects():
    if request.method == 'GET':
        subCode = request.args.get('subCode')
        subName = request.args.get('subName')
        facultyName = request.args.get('facultyName')
        return render_template('updateMCA_Subjects.html', subCode=subCode, subName=subName, facultyName=facultyName)
    
    elif request.method == 'POST':
        subCode = request.form['subCode']
        subName = request.form['subName']
        facultyName = request.form['facultyName']
        
        # Find the existing subject document to update
        existing_subject = db.MCA_subjects.find_one({'subCode': subCode})
        if existing_subject:
            update_result = db.MCA_subjects.update_one({'subCode': subCode}, {'$set': {'subName': subName, 'facultyName': facultyName}})
            
            if update_result.modified_count > 0:
                flash("Subject details have been updated successfully.")
            else:
                flash("Failed to update subject details.")
        else:
            flash("Subject not found.")
        return render_template('updateMCA_Subjects.html')   
    return render_template('updateMCA_Subjects.html')



@subject.route('/delete_MCAsubject/<subject_id>', methods=['GET'])
def delete_MCAsubject(subject_id):
    facultiesList = db.MCA_faculty.find()
    subjects = db.MCA_subjects.find()

    subjects_by_semester = {}
    for subject in subjects:
        semester = subject['semester']
        if semester not in subjects_by_semester:
            subjects_by_semester[semester] = []
        subjects_by_semester[semester].append(subject)

    semesters = subjects_by_semester.keys()

    db.MCA_subjects.delete_one({'_id': ObjectId(subject_id)})
    deletion_message = "Subject Deleted Successfully!"
    return render_template('MCA_Subjects.html', facultiesList=facultiesList, subjects=subjects, 
                           subjects_by_semester=subjects_by_semester, semesters=semesters, 
                           deletion_message=deletion_message)





# #Adding MBA Subjects according to semester
@subject.route('/MBA_semI', methods=['GET', 'POST'])
def MBA_semI():
    exists = ""
    subject = ""
    subjectList = MBA_db.sub_semOne.find()
    facultyList = MBA_db.MBA_faculty.find()
    if request.method == 'POST':
        subjectCode = request.form['subjectCode']
        subjectName = request.form['subjectName']
        facultyName = request.form['facultyName']

        existing_subject = MBA_db.sub_semOne.find_one({
            'subjectCode': subjectCode,
            'subjectName': subjectName,
            'facultyName': facultyName
        })

        if existing_subject:
            exists = "Subject code and Subject Name already Existed in this semester."
        else:
            MBA_db.sub_semOne.insert_one({'subjectCode': subjectCode, 'subjectName': subjectName, 'facultyName': facultyName})
            subject = "New Subject added successfully!"
        return render_template('MBA_semI.html', subject=subject, exists=exists,subjectList=subjectList, facultyList=facultyList)
    return render_template('MBA_semI.html',subjectList=subjectList,facultyList=facultyList)






# #Adding Subjects for Sem II according to specialization
@subject.route('/MBA_semII', methods=['GET', 'POST'])
def MBA_semII():
    exists = ""
    msg = ""
    subjectList = MBA_db.sub_semTwo.find()
    facultyList = MBA_db.MBA_faculty.find()

    subjects_by_specialization = {}
    for subject in subjectList:
        specialization = subject['specialization']
        if specialization not in subjects_by_specialization:
            subjects_by_specialization[specialization] = []
        subjects_by_specialization[specialization].append(subject)

    specialization = subjects_by_specialization.keys()

    if request.method == 'POST':
        specialization = request.form['specialization']
        subjectCode = request.form['subjectCode']
        subjectName = request.form['subjectName']
        facultyName = request.form['facultyName']

        if specialization == "Select Specialization" or facultyName == "Select Faculty Name":
            exists = "All Fields are Required. Please select all the fields."
            return render_template('MBA_semII.html', exists=exists, facultyList=facultyList, subjects_by_specialization=subjects_by_specialization, 
                               specialization=specialization, subjectList=subjectList)

        existing_subject = MBA_db.sub_semTwo.find_one({
                'specialization': specialization,
                'subjectCode': subjectCode,
                'subjectName': subjectName,
                'facultyName': facultyName
        })
        if existing_subject:
            exists = "Subject code and Subject Name already Existed in this Specialization."
        else:
            MBA_db.sub_semTwo.insert_one({'specialization': specialization, 'subjectCode': subjectCode, 
                                'subjectName': subjectName, 'facultyName': facultyName})
            msg = "Subject added successfully!"
        return render_template('MBA_semII.html', subjectList=subjectList, exists=exists, msg=msg, 
                               facultyList=facultyList, subjects_by_specialization=subjects_by_specialization, 
                               specialization=specialization)
    return render_template('MBA_semII.html', subjectList=subjectList, specialization=specialization, 
                           subjects_by_specialization=subjects_by_specialization, facultyList=facultyList)




# @subject.route('/delsemIIsubject', methods=['POST'])
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

