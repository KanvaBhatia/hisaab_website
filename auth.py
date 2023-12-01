########################################################################################
######################          Import packages      ###################################
########################################################################################
import urllib 
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from __init__ import db
import pygsheets
gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')
import datetime
#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)


auth = Blueprint('auth', __name__) # create a Blueprint object that we name 'auth'

@auth.route('/login', methods=['GET', 'POST']) # define login page path
def login(): # define login page fucntion
    if request.method=='GET': # if the request is a GET we return the login page
        return render_template('login.html')
    else: # if the request is POST the we check if the user exist and with te right password
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False
        user = User.query.filter_by(email=email).first()
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not user:
            flash('Please sign up before!')
            return redirect(url_for('auth.signup'))
        elif not check_password_hash(user.password, password):
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page
        # if the above check passes, then we know the user has the right credentials
        login_user(user, remember=remember)
        
        return redirect(url_for('main.profile'))

@auth.route('/signup', methods=['GET', 'POST'])# we define the sign up path
def signup(): # define the sign up function
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('signup.html')
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        if user: # if a user is found, we want to redirect back to signup page so user can try again
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))
        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password)) #
        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()


        # gc.sheet.create(email)
        # sh = gc.open(email)
        # wks = sh[0]

        # pygsheets.Cell(pos = (1,1),worksheet = wks).set_value("Date").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,2),worksheet = wks).set_value("Expense for").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,3),worksheet = wks).set_value("Expense Amount").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,4),worksheet = wks).set_value("Classify").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,5),worksheet = wks).set_value("Food").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,6),worksheet = wks).set_value("Padhai").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,7),worksheet = wks).set_value("Travel").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,8),worksheet = wks).set_value("Others").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,9),worksheet = wks).set_value("Total").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        # pygsheets.Cell(pos = (1,10),worksheet = wks).set_value("Month").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)

        # pygsheets.Cell(pos = (2,1),worksheet = wks).set_value(str(datetime.date.today()))
        # pygsheets.Cell(pos = (2,2),worksheet = wks).set_value("Random record please don't delete!!")
        # pygsheets.Cell(pos = (2,3),worksheet = wks).set_value(1)
        # pygsheets.Cell(pos = (2,4),worksheet = wks).set_value('none')
        # pygsheets.Cell(pos = (2,5),worksheet = wks).set_value('=IF(D2="food", C2, 0)')
        # pygsheets.Cell(pos = (2,6),worksheet = wks).set_value('=IF(D2="padhai", C2, 0)')
        # pygsheets.Cell(pos = (2,7),worksheet = wks).set_value('=IF(D2="travel", C2, 0)')
        # pygsheets.Cell(pos = (2,8),worksheet = wks).set_value('=IF(D2="others", C2, 0)')
        # pygsheets.Cell(pos = (2,9),worksheet = wks).set_value("=E2+F2+G2+H2")
        # pygsheets.Cell(pos = (2,10),worksheet = wks).set_value('=year(A2) &"-"& MONTH(A2)')


        # sh.share("kbthebest181@gmail.com", role='writer', type = 'user', emailMessage = email+" just created an account and here's the spreadsheet.")
        # sh.share(email, role='reader', type = 'user', emailMessage = f"Congratulations for registering with OnlyHisaab, {name}!\nHere is the access to your spreadsheet. You cannot edit it, contact us for any issue.")
        data = "{'signup':True, 'email':'"+email+"', 'name':'"+name+"'}"
        data = urllib.parse.quote(convert(data))

        return render_template('loading.html', my_data = data)
        return redirect(url_for('auth.login'))

@auth.route('/logout') # define logout path
@login_required
def logout(): #define the logout function
    logout_user()
    return redirect(url_for('main.index'))


def convert(input):
    # Converts unicode to string
    if isinstance(input, dict):
        return {convert(key): convert(value) for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [convert(element) for element in input]
    elif isinstance(input, str):
        return input.encode('utf-8')
    else:
        return input
