########################################################################################
######################          Import packages      ###################################
########################################################################################
from crypt import methods
from flask import Blueprint, render_template, flash, Flask, request, redirect, url_for
from flask_login import login_required, current_user
from __init__ import create_app, db
import io
from time import strptime
import pygsheets
import datetime
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('SVG')
import numpy as np
import urllib
########################################################################################
# our main blueprint
main = Blueprint('main', __name__)

@main.route('/') # home page that return 'index'
def index():
    return render_template('index.html')

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

# app = create_app() # we initialize our flask app using the __init__.py function
# if __name__ == '__main__':
#     # db.create_all(app=create_app()) # create the SQLite database
#     app.run(debug=True) # run the flask app on debug mode





# from flask import Flask, request, render_template
# import io
# import os
# from time import strptime
# import pygsheets
# import datetime
# import base64
#authorization
# gc = pygsheets.authorize(service_file='leafy-stock-354615-5b6f0be4032f.json')
gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')

#open the google spreadsheet (where 'PY to Gsheet Test' is the name of my sheet)
# sh = gc.open('Expenses')

#select the first sheet 
# wks = sh[0]

@main.route('/hisaab')
def getHandler():
    from flask_login import current_user
    if current_user.is_authenticated:
        print(current_user.id)
    # except Exception as e:
    #     print(e)
    return render_template('hisaab.html')

@main.route('/post/addtohisaab', methods = ['POST'])
def hisaab():
    if current_user.email == 'kanva.bhatia@gmail.com':
        gc = pygsheets.authorize(service_file='leafy-stock-354615-5b6f0be4032f.json')
        sh = gc.open('Expenses')
        wks = sh[0]
        r = request.form
        dateee = r["date"]
        expensee = r["expense"]
        amount = r["amount"]
        classific = r["type"]
        try:
            lennn = (len(wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[0]))
            pygsheets.Cell(pos = (lennn+1, 1),worksheet = wks).set_value(dateee)
            pygsheets.Cell(pos = (lennn+1, 2),worksheet = wks).set_value(expensee)
            pygsheets.Cell(pos = (lennn+1, 3),worksheet = wks).set_value(int(amount))
            pygsheets.Cell(pos = (lennn+1, 10),worksheet = wks).set_value(classific)
            return render_template('success.html')
        except Exception as e:
            return render_template('error.html', error = e)
    # sh = gc.open(current_user.email)
    # print(current_user.email)
    # wks = sh[0]
    r = request.form
    # r = urllib.parse.quote(convert(r))
    dateee = r["date"]
    expensee = r["expense"]
    amount = r["amount"]
    classific = r["type"]
    data = "{'signup': False, 'date':'"+dateee+"', 'expense':'"+expensee+"', 'amount':"+amount+", 'type':'"+classific+"'}"
    data = urllib.parse.quote(convert(data))
    # if int(r["pass"]) == 1810:
    #     try:
    #         lennn = (len(wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[0]))
    #         pygsheets.Cell(pos = (lennn+1, 1),worksheet = wks).set_value(dateee)
    #         pygsheets.Cell(pos = (lennn+1, 2),worksheet = wks).set_value(expensee)
    #         pygsheets.Cell(pos = (lennn+1, 3),worksheet = wks).set_value(int(amount))
    #         pygsheets.Cell(pos = (lennn+1, 4),worksheet = wks).set_value(classific)
    #         pygsheets.Cell(pos = (lennn+1, 5),worksheet = wks).set_value(f'=IF(D{lennn+1}="food", E{lennn}+C{lennn+1}, E{lennn})')
    #         pygsheets.Cell(pos = (lennn+1, 6),worksheet = wks).set_value(f'=IF(D{lennn+1}="travel", F{lennn}+C{lennn+1}, F{lennn})')
    #         pygsheets.Cell(pos = (lennn+1, 7),worksheet = wks).set_value(f'=IF(D{lennn+1}="padhai", G{lennn}+C{lennn+1}, G{lennn})')
    #         pygsheets.Cell(pos = (lennn+1, 8),worksheet = wks).set_value(f'=IF(D{lennn+1}="others", H{lennn}+C{lennn+1}, H{lennn})')
    #         pygsheets.Cell(pos = (lennn+1, 9),worksheet = wks).set_value(f"=E{lennn+1}+F{lennn+1}+G{lennn+1}+H{lennn+1}")
    #         pygsheets.Cell(pos = (lennn+1, 10),worksheet = wks).set_value(f'=year(A{lennn+1}) &"-"& MONTH(A{lennn+1})')
    #         return render_template('success.html')
    #     except Exception as e:
    #         return e
    # else:
    #     return "TRAITOR"
    return render_template('loading.html', my_data = data)

@main.route('/processing')
def processing():
    if request.args.to_dict(flat=False)['data'][0]:
        r = str(request.args.to_dict(flat=False)['data'][0])
    print(r)
    r = eval(r)
    if r['signup']:
        email = r['email']
        gc.sheet.create(email)
        sh = gc.open(email)
        wks = sh[0]

        pygsheets.Cell(pos = (1,1),worksheet = wks).set_value("Date").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,2),worksheet = wks).set_value("Expense for").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,3),worksheet = wks).set_value("Expense Amount").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,4),worksheet = wks).set_value("Classify").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,5),worksheet = wks).set_value("Food").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,6),worksheet = wks).set_value("Travel").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,7),worksheet = wks).set_value("Padhai").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,8),worksheet = wks).set_value("Others").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,9),worksheet = wks).set_value("Total").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)
        pygsheets.Cell(pos = (1,10),worksheet = wks).set_value("Month").set_text_format('foregroundColor' , (1,1,1,0)).color = (7/255,55/255,99/255,0)

        pygsheets.Cell(pos = (2,1),worksheet = wks).set_value(str(datetime.date.today()))
        pygsheets.Cell(pos = (2,2),worksheet = wks).set_value("Random record please don't delete!!")
        pygsheets.Cell(pos = (2,3),worksheet = wks).set_value(1)
        pygsheets.Cell(pos = (2,4),worksheet = wks).set_value('none')
        pygsheets.Cell(pos = (2,5),worksheet = wks).set_value('=IF(D2="food", C2, 0)')
        pygsheets.Cell(pos = (2,6),worksheet = wks).set_value('=IF(D2="travel", C2, 0)')
        pygsheets.Cell(pos = (2,7),worksheet = wks).set_value('=IF(D2="padhai", C2, 0)')
        pygsheets.Cell(pos = (2,8),worksheet = wks).set_value('=IF(D2="others", C2, 0)')
        pygsheets.Cell(pos = (2,9),worksheet = wks).set_value("=E2+F2+G2+H2")
        pygsheets.Cell(pos = (2,10),worksheet = wks).set_value('=year(A2) &"-"& MONTH(A2)')


        sh.share("kbthebest181@gmail.com", role='writer', type = 'user', emailMessage = email+" just created an account and here's the spreadsheet.")
        sh.share(email, role='reader', type = 'user', emailMessage = f"Congratulations for registering with OnlyHisaab, {r['name']}!\nHere is the access to your spreadsheet. You cannot edit it, contact us for any issue.")

        return redirect(url_for('auth.login'))
    
#     if r['summary']:
#         None
    sh = gc.open(current_user.email)
    print(current_user.email)
    wks = sh[0]

    # if request.args.to_dict(flat=False)['data'][0]:
    #     r = str(request.args.to_dict(flat=False)['data'][0])
    dateee = r["date"]
    expensee = r["expense"]
    amount = r["amount"]
    classific = r["type"]
    # if int(r["pass"]) == 1810:
    try:
        lennn = (len(wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[0]))
        pygsheets.Cell(pos = (lennn+1, 1),worksheet = wks).set_value(dateee)
        pygsheets.Cell(pos = (lennn+1, 2),worksheet = wks).set_value(expensee)
        pygsheets.Cell(pos = (lennn+1, 3),worksheet = wks).set_value(int(amount))
        pygsheets.Cell(pos = (lennn+1, 4),worksheet = wks).set_value(classific)
        pygsheets.Cell(pos = (lennn+1, 5),worksheet = wks).set_value(f'=IF(D{lennn+1}="food", E{lennn}+C{lennn+1}, E{lennn})')
        pygsheets.Cell(pos = (lennn+1, 6),worksheet = wks).set_value(f'=IF(D{lennn+1}="travel", F{lennn}+C{lennn+1}, F{lennn})')
        pygsheets.Cell(pos = (lennn+1, 7),worksheet = wks).set_value(f'=IF(D{lennn+1}="padhai", G{lennn}+C{lennn+1}, G{lennn})')
        pygsheets.Cell(pos = (lennn+1, 8),worksheet = wks).set_value(f'=IF(D{lennn+1}="others", H{lennn}+C{lennn+1}, H{lennn})')
        pygsheets.Cell(pos = (lennn+1, 9),worksheet = wks).set_value(f"=E{lennn+1}+F{lennn+1}+G{lennn+1}+H{lennn+1}")
        pygsheets.Cell(pos = (lennn+1, 10),worksheet = wks).set_value(f'=year(A{lennn+1}) &"-"& MONTH(A{lennn+1})')
        return render_template('success.html')
    except Exception as e:
        return render_template('error.html', error = e)

    # else:
    #     return "TRAITOR"
    
@main.route('/post/summary', methods = ['POST', 'GET'])
def summary():
#     try:
    if current_user.email == 'kanva.bhatia@gmail.com':
        gc = pygsheets.authorize(service_file='leafy-stock-354615-5b6f0be4032f.json')
        sh = gc.open('Expenses')
        wks = sh[0]
        r = request.form
        month_chosen = r["month"]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        current_month = months.index(month_chosen)+1
        row_last = wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1]
        for i in range(len(row_last)-1,-1,-1):
            if row_last[i] == (f"{datetime.date.today().year}-{current_month}"):
                last_index = i
                break
        first = ((wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1].index(f"{datetime.date.today().year}-{current_month}")))
        month_total_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][14])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][14])))
        month_others_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][13])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][13])))
        month_padhai_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][12])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][12])))
        month_travel_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][11])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][11])))
        month_food_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][10])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][10])))

    else:
        gc = pygsheets.authorize(service_file='silent-blade-278608-97476201bec3.json')
        sh = gc.open(current_user.email)
        wks = sh[0]
        r = request.form
        month_chosen = r["month"]
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        current_month = months.index(month_chosen)+1
        row_last = wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1]
        for i in range(len(row_last)-1,-1,-1):
            if row_last[i] == (f"{datetime.date.today().year}-{current_month}"):
                last_index = i
                break
        first = ((wks.get_all_values(majdim="COLUMNS", include_tailing_empty=False, include_tailing_empty_rows=False)[-1].index(f"{datetime.date.today().year}-{current_month}")))
        month_total_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][8])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][8])))
        month_others_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][7])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][7])))
        month_padhai_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][6])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][6])))
        month_travel_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][5])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][5])))
        month_food_expense = (int(wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[last_index][4])-int((wks.get_all_values(majdim="ROWS", include_tailing_empty=False, include_tailing_empty_rows=False)[first][4])))


    result = {"Food":month_food_expense, "Travel":month_travel_expense, "Padhai":month_padhai_expense, "Others":month_others_expense, "Total":month_total_expense}
    # import matplotlib.pyplot as plt
    # import matplotlib
    # matplotlib.use('SVG')
    # import numpy as np

    y = np.array([month_food_expense, month_travel_expense, month_padhai_expense, month_others_expense])
    mylabels = [f"Food = {round((month_food_expense*100/month_total_expense), 2)}%", f"Travel = {round((month_travel_expense*100/month_total_expense),2)}%", f"Padhai = {round((month_padhai_expense*100/month_total_expense),2)}%", f"Others = {round((month_others_expense*100/month_total_expense),2)}%"]
    img = io.BytesIO()
    plt.clf()
    plt.pie(y, labels = mylabels)
    plt.legend(title = "Expenses:",bbox_to_anchor=(1.2,1.05), loc="upper right", fontsize=10, bbox_transform=plt.gcf().transFigure)
    plt.savefig(img, format = 'png', bbox_inches="tight") 
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    return render_template('summary.html', result = result, image = { 'image': plot_url }, month = month_chosen)
#     except Exception as e:
#         return render_template('error.html', error = e)



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


app = create_app() # we initialize our flask app using the __init__.py function
if __name__ == '__main__':
    # db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode



