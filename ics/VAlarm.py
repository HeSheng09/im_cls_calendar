class VAlarm:
    def __init__(self):
        self.trigger = "-PT5M"
        self.action = "DISPLAY"
        self.description = "Reminder"

    def to_string(self):
        return f'BEGIN:VALARM\n' \
               f'TRIGGER:{self.trigger}\n' \
               f'ACTION:{self.action}\n' \
               f'DESCRIPTION:{self.description}\n' \
               f'END:VALARM'


if __name__ == '__main__':
    valarm = VAlarm()
    print(valarm.to_string())
