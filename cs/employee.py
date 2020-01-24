class Employee:

    def __init__(self, seniority, name, num_shifts, assigned_shifts, phone_number, current, give_to):
        self.seniority = seniority
        self.name = name
        self.num_shifts = num_shifts
        self.assigned_shifts = assigned_shifts
        self.phone_number = phone_number
        self.current = current
        self.give_to = give_to

    def assign_shift(self):
        self.assigned_shifts += 1
        self.current = 'FALSE'
        self.give_to = ''

    def __eq__(self, other):
        return (self.seniority == other.seniority and
                self.name == other.name and
                self.num_shifts == other.num_shifts and
                self.assigned_shifts == other.assigned_shifts and
                self.phone_number == other.phone_number and
                self.current == other.current and
                self.give_to == other.give_to)
