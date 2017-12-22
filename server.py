import atexit
import os
from flask import Flask
from flask import request
from flask import render_template
from flask import abort
from flask import url_for
from flask import flash
from sns_sender import send_sms
from spreadsheet_reader import SpreadsheetReader
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from itsdangerous import URLSafeSerializer, BadSignature

app = Flask(__name__)


def get_serializer(secret_key=None):
    if secret_key is None:
        secret_key = app.secret_key
    return URLSafeSerializer(secret_key)


def get_activation_link(employeeIdx):
    s = get_serializer()
    payload = s.dumps(employeeIdx)
    with app.app_context():
        url = url_for('shifts', payload=payload, _external=True)
    return url


def contact_next_employee():
    print('Scheduled send sms job initiated')
    employees = SpreadsheetReader.getEmployees()
    print(employees)
    cur_employee = None
    signed_url = None
    for index, row in employees.iterrows():
        is_last_employee = index == employees.shape[0] - 1
        if not is_last_employee:
            nextRow = employees.iloc[index+1]

        shifts_not_full = row['Assigned'] < row['NumShifts']

        # TODO: refactor
        lowestAssigned = 100
        for index2, row2 in employees.copy().iterrows():
            if int(row2['Assigned']) < lowestAssigned:
                lowestAssigned = int(row2['Assigned'])
        # TODO: is is_last_employee check necessary?
        if shifts_not_full and (is_last_employee
                                or int(row['Assigned']) <= lowestAssigned):
            cur_employee = row
            signed_url = str(index)
            idx = index
            break

    if cur_employee['Current'] == 'FALSE':
        SpreadsheetReader.updateEmployeesCell(idx, 5, True)
        link = get_activation_link(signed_url)
        message = ('Hi {}, please click on the provided link '
                   'to choose your call shift: {}')
        message = message.format(cur_employee['Name'], link)
        print(message)
        send_sms(cur_employee['PhoneNumber'], message)


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'GET':
        return render_template('admin.html')
    else:
        action = request.form.get('action')
        if action == 'pause':
            scheduler.pause()
        elif action == 'resume':
            scheduler.resume()
        return render_template('admin.html')


@app.route("/shifts/<payload>", methods=['GET', 'POST'])
def shifts(payload):
    s = get_serializer()
    shifts = SpreadsheetReader.getAvailableShifts()
    employees = SpreadsheetReader.getEmployees()
    if request.method == 'GET':
        try:
            employeeNum = s.loads(payload)
        except BadSignature:
            abort(404)
        return render_template('shifts.html',
                               shifts=shifts,
                               employeeNum=employeeNum,
                               employees=employees)
    else:
        employeeNum = int(payload)
        employeeRow = employees.iloc[employeeNum]
        if employeeRow['Current'] == 'TRUE':
            row = int(request.form.get('row'))
            employeeName = employeeRow['Name']
            assigned = int(employeeRow['Assigned']) + 1
            if employeeRow['GiveTo'] != '':
                employeeName = '{} ({})'.format(employeeRow['GiveTo'], employeeName)
            SpreadsheetReader.updateAvailableShiftsCell(row, 4, employeeName)
            SpreadsheetReader.updateEmployeesCell(employeeNum, 3, assigned)
            SpreadsheetReader.updateEmployeesCell(employeeNum, 5, False)
            SpreadsheetReader.updateEmployeesCell(employeeNum, 6, '')
            shifts.iloc[row]['OnCall'] = employeeName
            flash('Thank you, {}!'.format(employeeName))
            return render_template('shifts.html',
                                   shifts=shifts,
                                   employeeNum=employeeNum,
                                   employees=employees)
        else:
            flash('Please wait until it is your turn.')
            return render_template('shifts.html',
                                   shifts=shifts,
                                   employeeNum=employeeNum,
                                   employees=employees)


@app.route("/give/<payload>", methods=['POST'])
def give(payload):
    shifts = SpreadsheetReader.getAvailableShifts()
    employee_num = int(payload)
    employees = SpreadsheetReader.getEmployees()
    give_to_row = employees.iloc[int(request.form.get('row'))]
    employee_row = employees.iloc[employee_num]
    SpreadsheetReader.updateEmployeesCell(employee_num, 6, give_to_row['Name'])
    message = ('Hi {}, {} would like you to take their call shift. '
               'Please click on the provided link: {}')
    link = get_activation_link(employee_num)
    message = message.format(give_to_row['Name'], employee_row['Name'], link)
    print(message)
    send_sms(give_to_row['PhoneNumber'], message)
    flash("Thank you, {}!".format(employee_row['Name']))
    return render_template('shifts.html',
                           shifts=shifts,
                           employeeNum=employee_num,
                           employees=employees)


if __name__ == '__main__':
    app.config['SERVER_NAME'] = 'still-hamlet-15049.herokuapp.com'
    #app.config['SERVER_NAME'] = 'localhost:5000'
    app.secret_key = os.environ['APP_SECRET_KEY']
    with app.app_context():
        scheduler = BackgroundScheduler()
        scheduler.start()
        scheduler.add_job(
            func=contact_next_employee,
            trigger=IntervalTrigger(seconds=10),
            id='sms_job',
            name='Send sms to next in queue',
            replace_existing=True
        )
    atexit.register(lambda: scheduler.shutdown())
    print('Port = {}'.format(os.environ.get("PORT", 5000)))
    print(type(os.environ.get("PORT", 5000)))
    app.run(debug=False, port=os.environ.get("PORT", 5000), host='0.0.0.0')
