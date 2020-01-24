class Shift:

    def __init__(self, date, day, time, on_call):
        self.date = date
        self.day = day
        self.time = time
        self.on_call = on_call

    def __eq__(self, other):
        return (self.date == other.date and
                self.day == other.day and
                self.time == other.time and
                self.on_call == other.on_call)
