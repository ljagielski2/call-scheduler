from flask import request, render_template, abort, flash
from itsdangerous import URLSafeSerializer, BadSignature

from cs import APP
from cs import SCHEDULER
from cs import SPREADSHEET
from cs.sns import send_sms
from cs.spreadsheet_reader import SpreadsheetReader
from cs.activation_link import get_activation_link

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
    available_shifts = SPREADSHEET.get_available_shifts_list()
    employees = SPREADSHEET.get_employees_list()
    if request.method == 'GET':
        try:
            serializer = URLSafeSerializer(APP.secret_key)
            employee_num = serializer.loads(payload)
        except BadSignature:
            abort(404)
    else:
        employee_num = handle_post_shifts(available_shifts, employees, payload)

    return render_template('shifts.html',
                           shifts=available_shifts,
                           employeeNum=employee_num,
                           employees=employees)

def handle_post_shifts(available_shifts, employees, payload):
    employee_num = int(payload)
    employee = employees[employee_num]
    if employee.current == 'TRUE':
        shift_num = int(request.form.get('row'))
        assign_to = employee.name

        if employee.give_to != '':
            assign_to = '{} ({})'.format(employee.give_to, employee.name)

        available_shifts[shift_num].on_call = assign_to
        employee.assign_shift()
        SPREADSHEET.add_name_to_shift(shift_num, available_shifts[shift_num])
        SPREADSHEET.assign_shift(employee)

        flash('Thank you, {}!'.format(assign_to))

    else:
        flash('Please wait until it is your turn.')

    return employee_num

@APP.route("/give/<payload>", methods=['POST'])
def give(payload):
    employee_num = int(payload)
    employees = SPREADSHEET.get_employees_list()
    handle_post_give(employee_num, employees)
    return render_template('shifts.html',
                           shifts=SPREADSHEET.get_available_shifts_list(),
                           employeeNum=employee_num,
                           employees=employees)

def handle_post_give(employee_num, employees):
    give_to_employee = employees[int(request.form.get('row'))]
    employee = employees[employee_num]
    SPREADSHEET.update_employees_give_to(employee_num, give_to_employee.name)

    template = ('Hi {}, {} would like you to take their call shift. '
                'Please click on the provided link: {}')

    message = template.format(give_to_employee.name,
                              employee.name,
                              get_activation_link(employee_num))
    print(message)
    send_sms(give_to_employee.phone_number, message)
    flash("Thank you, {}!".format(employee.name))
