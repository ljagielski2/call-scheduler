from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from cs import SPREADSHEET
from cs import CONFIG
from cs.sns import send_sms
from cs.activation_link import get_activation_link

class ContactScheduler:

    def __init__(self):
        self.scheduler = BackgroundScheduler()

    def start(self):
        self.scheduler.start()
        self.scheduler.add_job(
            func=self.contact_next_employee,
            trigger=IntervalTrigger(seconds=int(CONFIG['INTERVAL'])),
            id='sms_job',
            name='Send sms to next in queue',
            replace_existing=True
        )

    def shutdown(self):
        self.scheduler.shutdown()

    def pause(self):
        self.scheduler.pause()

    def resume(self):
        self.scheduler.resume()

    def contact_next_employee(self):
        print('Scheduled send sms job initiated')
        employees = SPREADSHEET.get_employees_list()
        print(employees)
        lowest_assigned = self.__get_lowest_assigned_shifts(employees)
        cur_employee = self.__get_next_employee(employees, lowest_assigned)

        if cur_employee is None:
            print('Done scheduling')
            return

        if cur_employee.current == 'FALSE':
            SPREADSHEET.update_employees_current(cur_employee.seniority, True)
            message = self.__create_contact_message(cur_employee)
            print(message)
            send_sms(cur_employee.phone_number, message)

    def __get_lowest_assigned_shifts(self, employees):
        lowest_assigned = 100
        for employee in employees:
            has_least_shifts = employee.assigned_shifts < lowest_assigned
            has_open_shifts = employee.assigned_shifts < employee.num_shifts
            if has_least_shifts and has_open_shifts:
                lowest_assigned = employee.assigned_shifts
        return lowest_assigned

    def __get_next_employee(self, employees, lowest_assigned):
        cur_employee = None
        for employee in employees:
            shifts_not_full = employee.assigned_shifts < employee.num_shifts

            if shifts_not_full and employee.assigned_shifts <= lowest_assigned:
                cur_employee = employee
                break

        return cur_employee

    def __create_contact_message(self, employee):
        link = get_activation_link(str(employee.seniority))
        template = ('Hi {}, please click on the provided link '
                    'to choose your call shift: {}')
        return template.format(employee.name, link)
