from flask import Blueprint, render_template, request, send_file
from database import Database, MBA_Database
import pandas as pd


attendance = Blueprint('attendance', __name__)
db=Database()
MBA_db = MBA_Database()

@attendance.route('/takeAttendance', methods=['GET', 'POST'])
def mark_attendance():
    success = []
    error_msg = None
    semesters = db.MCA_subjects.distinct('semester')
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

            if time == "Select Time" or selected_semester == "Select Semester" or month == "Select Month":
                error_msg = "All Fields are required. Please Select all Fields!"
                students = db.MCA_Students.find({'batch': batch, 'division': division})
                return render_template('markAttendance.html', error=error_msg, semesters=semesters, students=students)

            existing_data = db.MCA_Attendance.find_one({
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
                students = db.MCA_Students.find({'batch': batch, 'division': division})
                return render_template('markAttendance.html', error=error_msg, semesters=semesters, students=students)

            students = db.MCA_Students.find({'batch': batch, 'division': division})
            for student in students:
                roll = student['roll']
                name = student['name'].strip()


                checkbox_name = f'attendance_{roll}_{name}'
                checkbox_value = request.form.get(checkbox_name)
                
                # Check if checkbox_value is truthy (not an empty string)
                if checkbox_value:
                    attendance_value = 'P'  # If checked, mark as present
                else:
                    attendance_value = 'A'

                for key, value in request.form.items():
                    print(f"Checkbox Name: {key}, Value: {value}")
                 
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
                db.MCA_Attendance.insert_one(student_data)

            success.append("Attendance Marked Successfully.")
            students = db.MCA_Students.find({'batch': batch, 'division': division})
            return render_template('markAttendance.html', success=success, students=students, semesters=semesters)
    except Exception as e:
        print(f"An error occurred: {e}")
    return render_template('markAttendance.html', success=success, students=students, semesters=semesters)



@attendance.route("/monthlyReport", methods=["GET", "POST"])
def generate_report():
    batches = db.MCAbatches.find({}, {'batch': 1})
    semesters = db.MCA_subjects.distinct('semester')

    if request.method == "POST":
        batch = request.form['batch']
        division = request.form['division']
        subject_name = request.form['subject_name']
        semester = request.form['semester']
        selected_month = request.form['month']


        if batch == "Select Batch" or division=="Select Division" or subject_name=="Select Subject" or semester=="Select Semester" or selected_month=="Select Month":
            error="Please Select All Fields. All Fields are Required to Generate the Report"
            return render_template("monthlyReport.html", batches=batches, semesters=semesters, error=error )

        # Fetch attendance data based on the selected criteria
        selected_attendance = db.MCA_Attendance.find({"batch": batch, "division":division, "semester": semester, "subject_name": subject_name, "month": selected_month})

        distinct_dates = db.MCA_Attendance.distinct('date', {
            "batch": batch,
            "division": division,
            "semester": semester,
            "subject_name": subject_name,
            "month": selected_month
        })

        student_attendance = {}

        for attendance_record in selected_attendance:
            student_roll = attendance_record['roll']

            student_details = db.MCA_Students.find_one({"roll": student_roll})

            if student_details:
                if student_roll not in student_attendance:
                    student_attendance[student_roll] = {
                        'batch': student_details['batch'],
                        'name': student_details['name'],
                        'division': student_details['division'],
                        'attendance_by_date': {date: 'A' for date in distinct_dates},
                        'total_lectures': 0,
                        'attended_lectures': 0
                    }

                student_attendance[student_roll]['total_lectures'] += 1
                
                date = attendance_record['date']
                student_attendance[student_roll]['attendance_by_date'][date] = attendance_record['attendance']

                if attendance_record['attendance'] == "P":
                    student_attendance[student_roll]['attended_lectures'] += 1

        # Calculate attendance percentage for each student
        total_lectures = 0
        student_percentages = {}
        for student_roll, data in student_attendance.items():
            total_lectures = data['total_lectures']
            attended_lectures = data['attended_lectures']

            if total_lectures > 0:
                attendance_percentage = (attended_lectures / total_lectures) * 100
            else:
                attendance_percentage = 0

            student_percentages[student_roll] = {
                'batch': data['batch'],
                'name': data['name'],
                'division': data['division'],
                'percentage': attendance_percentage
            }
        subject_doc = db.MCA_subjects.find_one({"subName": subject_name})

        if subject_doc:
            faculty_name = subject_doc.get('facultyName', 'Faculty not found')
        else:
            faculty_name = 'Faculty not found'

        return render_template("attendanceReport.html", batch=batch, division=division, semester=semester, student_percentages=student_percentages,student_attendance=student_attendance, 
                               selected_month=selected_month, faculty_name=faculty_name,
                               subject_name=subject_name, total_lectures=total_lectures, distinct_dates=distinct_dates)
    return render_template("monthlyReport.html", batches=batches, semesters=semesters)


@attendance.route("/saveToExcel", methods=["POST"])
def save_to_excel():
    subject_name = request.form['subject_name']
    batch = request.form['batch']
    division = request.form['division']
    semester = request.form['semester']
    selected_month = request.form['month']

    selected_attendance = db.MCA_Attendance.find({
        "batch": batch,
        "division": division,
        "semester": semester,
        "subject_name": subject_name,
        "month": selected_month
    })

    student_attendance = {}
    dates = set()
    for attendance_record in selected_attendance:
        student_roll = attendance_record['roll']
        student_details = db.MCA_Students.find_one({"roll": student_roll})

        if student_details:
            if student_roll not in student_attendance:
                student_attendance[student_roll] = {
                    'roll': student_details['roll'],
                    'name': student_details['name'],
                    'attendance_by_date': {},
                    'total_lectures': 0,
                    'attended_lectures': 0,
                    'batch': student_details.get('batch', 'Unknown Batch')
                }

            student_attendance[student_roll]['total_lectures'] += 1
            date = attendance_record['date']
            dates.add(date)
            student_attendance[student_roll]['attendance_by_date'][date] = attendance_record['attendance']

            if attendance_record['attendance'] == "P":
                student_attendance[student_roll]['attended_lectures'] += 1



    for student_roll, data in student_attendance.items():
        total_lectures = data['total_lectures']
        attended_lectures = data['attended_lectures']
        if total_lectures > 0:
            attendance_percentage = (attended_lectures / total_lectures) * 100
        else:
            attendance_percentage = 0
        student_attendance[student_roll]['percentage'] = attendance_percentage


    subject_doc = db.MCA_subjects.find_one({"subName": subject_name})
    faculty_name = subject_doc.get('facultyName', 'Faculty not found')

    df_columns = ['Batch', 'Subject Name', 'Faculty Name']
    df_data = [[batch, subject_name, faculty_name]]
    batch_subject_df = pd.DataFrame(df_data, columns=df_columns)

    df_columns = ['Roll No', 'Student Name'] + sorted(dates) + ['Total Lectures', 'Attended Lectures', 'Attendance Percentage']
    df_data = []
    for student_roll, data in student_attendance.items():
        row = [data['roll'], data['name']]
        for date in sorted(dates):
            row.append(data['attendance_by_date'].get(date, '-'))
        row += [data['total_lectures'], data['attended_lectures'], data['percentage']]
        df_data.append(row)

    attendance_df = pd.DataFrame(df_data, columns=df_columns)

    excel_filename = 'MCA_report.xlsx'
    with pd.ExcelWriter(excel_filename) as writer:
        batch_subject_df.to_excel(writer, index=False)
        attendance_df.to_excel(writer, index=False, startrow=2)
    return send_file(excel_filename, as_attachment=True)



#==================================================================================
@attendance.route('/take_SemIAttendance', methods=['GET', 'POST'])
def mark_SemIAttendance():
    sdata = ""
    subjectList =MBA_db.sub_semOne.find()
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

            students = MBA_db.MBA_Students.find({'batch': batch, 'division': division})
            if time == "Select Time" or selected_semester == "Select Semester" or subject_name == "Select Subject" or month == "Select Month":
                error_msg = "All Fields are required. Please Select all Fields!"
                return render_template('mark_SemIAttendance.html',error=error_msg, subjectList=subjectList, students=students)

            existing_data = MBA_db.MBA_SemIAttendance.find_one({
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
                return render_template('mark_SemIAttendance.html',error=error_msg, subjectList=subjectList, students=students)
            
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
                    MBA_db.MBA_SemIAttendance.insert_one(student_data)
            
            sdata = "Attendance Marked Successfully."

            students = MBA_db.MBA_Students.find({'batch': batch, 'division': division})
            return render_template('mark_SemIAttendance.html', data=sdata, students=students, subjectList=subjectList)
    except Exception as e:
        print(f"An error occurred: {e}")
    return render_template('mark_SemIAttendance.html', data=sdata, students=students, subjectList=subjectList)


# @attendance.route('/MBA_SemOne_Reports', methods=['GET', 'POST'])
# def MBA_SemOne_Reports():
#     batches = MBA_db.MBAbatches.find({}, {'batch': 1})
#     subjectList = MBA_db.sub_semOne.find()

#     if request.method == "POST":
#         batch = request.form['batch']
#         division = request.form['division']
#         subject_name = request.form['subject_name']
#         semester = request.form['semester']
#         selected_month = request.form['month']


#         if batch == "Select Batch" or division=="Select Division" or subject_name=="Select Subject" or semester=="Select Semester" or selected_month=="Select Month":
#             error="Please Select All Fields. All Fields are Required to Generate the Report"
#             return render_template("monthlyReport.html", batches=batches, subjectList=subjectList, error=error )

#         # Fetch attendance data based on the selected criteria
#         selected_attendance = MBA_db.MBA_SemIAttendance.find({"batch": batch, "division":division, "semester": semester, "subject_name": subject_name, "month": selected_month})

#         distinct_dates = MBA_db.MBA_SemIAttendance.distinct('date', {
#             "batch": batch,
#             "division": division,
#             "semester": semester,
#             "subject_name": subject_name,
#             "month": selected_month
#         })

#         student_attendance = {}

#         for attendance_record in selected_attendance:
#             student_roll = attendance_record['roll']

#             student_details = MBA_db.MBA_Students.find_one({"roll": student_roll})

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
#         subject_doc = MBA_db.sub_semOne.find_one({"subjectName": subject_name})

#         if subject_doc:
#             faculty_name = subject_doc.get('facultyName', 'Faculty not found')
#         else:
#             faculty_name = 'Faculty not found'

#         return render_template("MBA_semOneReport.html", batch=batch, division=division, semester=semester, student_percentages=student_percentages,student_attendance=student_attendance, 
#                                selected_month=selected_month, faculty_name=faculty_name,
#                                subject_name=subject_name, total_lectures=total_lectures, distinct_dates=distinct_dates)
#     return render_template('MBA_SemOne_Reports.html', subjectList=subjectList)