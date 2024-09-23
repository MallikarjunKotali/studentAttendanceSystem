from flask import Blueprint, render_template, request, redirect, session
from database import Database

auth = Blueprint('auth', __name__)
db = Database()

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        error = []
        message = []
        try:
            if len(password) >=6  and len(password)<= 12:
                if db.register.find_one({'email': email, 'password': password}):
                    error.append("User Already Existed")
                else:
                    db.register.insert_one({'email': email, 'password': password})
                    message.append("Account Created Succssfully...!")
            else:
                error.append("Password must be greater than 6 and less than 12 character")        
        except Exception as e:
            print("Error", e)
        
        if error:
            return render_template('register.html', err=error)
        else:
            return render_template('register.html', msg=message)

    return render_template('register.html')


@auth.route('/facultyLogin', methods = ['GET', 'POST'])
def facultyLogin():
    passw = "Invalid Email or Password"
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = db.register.find_one({'email': email, 'password': password})
        if user:
            session['email'] = email
            return render_template('showStream.html')
        return render_template('facultyLogin.html', passw=passw)
    return render_template('facultyLogin.html')



#MCA Admin Login
@auth.route('/adminLogin', methods=['GET', 'POST'])
def adminLogin():
    passw = 'Invalid username or Password'
    if request.method == 'POST':
        adminEmail = request.form['adminEmail']
        password = request.form['password']

        admin = db.adminLogin.find_one({'adminEmail': adminEmail, 'password': password})
        if admin:
            session['adminEmail'] = adminEmail
            return render_template('showStream.html')
        return render_template('adminLogin.html', passw=passw)
    return render_template('adminLogin.html')



@auth.route('/logout')
def logout():
    session.clear()
    session['user_id']= False
    return redirect('/')
