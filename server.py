import os
import atexit

from flask import Flask, request, render_template, abort, url_for, flash
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from itsdangerous import URLSafeSerializer, BadSignature

import sns
from spreadsheet_reader import SpreadsheetReader

APP = Flask(__name__)

SPREADSHEET = SpreadsheetReader('CallSchedule')
#SPREADSHEET = SpreadsheetReader('CallScheduleDev')

def get_activation_link(employee_idx):
    serializer = URLSafeSerializer(APP.secret_key)
    payload = serializer.dumps(employee_idx)

    with APP.app_context():
        url = url_for('shifts', payload=payload, _external=True)

    return url


def contact_next_employee():
    print('Scheduled send sms job initiated')
    employees = SPREADSHEET.get_employees()
    print(employees)
    cur_employee = None
    signed_url = None
    for index, row in employees.iterrows():
        shifts_not_full = row['Assigned'] < row['NumShifts']
        lowest_assigned = 100
        for index2, row2 in employees.copy().iterrows():
            has_least_shifts = int(row2['Assigned']) < lowest_assigned
            has_open_shifts = int(row2['Assigned']) < int(row2['NumShifts'])
            if has_least_shifts and has_open_shifts:
                lowest_assigned = int(row2['Assigned'])

        if shifts_not_full and int(row['Assigned']) <= lowest_assigned:
            cur_employee = row
            signed_url = str(index)
            idx = index
            break

    if cur_employee is None:
        print('Done scheduling')
        return

    if cur_employee['Current'] == 'FALSE':
        SPREADSHEET.update_employees_cell(idx, 5, True)
        link = get_activation_link(signed_url)
        message = ('Hi {}, please click on the provided link '
                   'to choose your call shift: {}')
        message = message.format(cur_employee['Name'], link)
        print(message)
        sns.send_sms(cur_employee['PhoneNumber'], message)


@APP.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'pause':
            SCHEDULER.pause()
        elif action == 'resume':
            SCHEDULER.resume()

    return render_template('admin.html')


@APP.route("/shifts/<payload>", methods=['GET', 'POST'])
def shifts(payload):
    serializer = URLSafeSerializer(APP.secret_key)
    available_shifts = SPREADSHEET.get_available_shifts()
    employees = SPREADSHEET.get_employees()
    if request.method == 'GET':
        try:
            employee_num = serializer.loads(payload)
        except BadSignature:
            abort(404)
    else:
        employee_num = int(payload)
        employee_row = employees.iloc[employee_num]
        if employee_row['Current'] == 'TRUE':
            row = int(request.form.get('row'))
            employee_name = employee_row['Name']
            assigned = int(employee_row['Assigned']) + 1

            if employee_row['GiveTo'] != '':
                employee_name = '{} ({})'.format(employee_row['GiveTo'],
                                                 employee_name)

            SPREADSHEET.update_available_shifts_cell(row, 4, employee_name)
            SPREADSHEET.update_employees_cell(employee_num, 3, assigned)
            SPREADSHEET.update_employees_cell(employee_num, 5, False)
            SPREADSHEET.update_employees_cell(employee_num, 6, '')
            available_shifts.iloc[row]['OnCall'] = employee_name
            flash('Thank you, {}!'.format(employee_name))

        else:
            flash('Please wait until it is your turn.')

    return render_template('shifts.html',
                           shifts=available_shifts,
                           employeeNum=employee_num,
                           employees=employees)


@APP.route("/give/<payload>", methods=['POST'])
def give(payload):
    employee_num = int(payload)
    employees = SPREADSHEET.get_employees()
    give_to_row = employees.iloc[int(request.form.get('row'))]
    employee_row = employees.iloc[employee_num]

    SPREADSHEET.update_employees_cell(employee_num, 6, give_to_row['Name'])

    template = ('Hi {}, {} would like you to take their call shift. '
                'Please click on the provided link: {}')

    message = template.format(give_to_row['Name'],
                              employee_row['Name'],
                              get_activation_link(employee_num))
    print(message)
    sns.send_sms(give_to_row['PhoneNumber'], message)
    flash("Thank you, {}!".format(employee_row['Name']))
    return render_template('shifts.html',
                           shifts=SPREADSHEET.get_available_shifts(),
                           employeeNum=employee_num,
                           employees=employees)


if __name__ == '__main__':
    APP.config['SERVER_NAME'] = 'still-hamlet-15049.herokuapp.com'
    #APP.config['SERVER_NAME'] = 'localhost:5000'
    APP.secret_key = os.environ['APP_SECRET_KEY']
    with APP.app_context():
        SCHEDULER = BackgroundScheduler()
        SCHEDULER.start()
        SCHEDULER.add_job(
            func=contact_next_employee,
            trigger=IntervalTrigger(seconds=600),
            #trigger=IntervalTrigger(seconds=10),
            id='sms_job',
            name='Send sms to next in queue',
            replace_existing=True
        )
    atexit.register(lambda: SCHEDULER.shutdown())
    APP.run(debug=False, port=int(os.environ.get("PORT", 5000)), host='0.0.0.0')
