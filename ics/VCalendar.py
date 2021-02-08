from ics.VTimezone import VTimezone


class VCalendar:
    def __init__(self, **kwargs):
        if "prodid" in kwargs.keys():
            self.prodid = kwargs['prodid']
        else:
            self.prodid = '-//he.cn//iCalendar Event//EN'
        if "version" in kwargs.keys():
            self.version = kwargs['version']
        else:
            self.version = '2.0'
        if 'calscale' in kwargs.keys():
            self.calscale = kwargs['calscale']
        else:
            self.calscale = 'GREGORIAN'
        if 'method' in kwargs.keys():
            self.method = kwargs['method']
        else:
            self.method = 'PUBLISH'
        if '_class' in kwargs.keys():
            self._class = kwargs['_class']
        else:
            self._class = 'PUBLIC'
        if "v_timezone" in kwargs.keys():
            self.v_timezone = kwargs['v_timezone']
        else:
            self.v_timezone = VTimezone().to_string()
        if "events" in kwargs.keys():
            self.v_events = kwargs['events']
        else:
            self.v_events = []

    def to_string(self):
        v_calendar = f'BEGIN:VCALENDAR\n' \
                     f'PRODID:{self.prodid}\n' \
                     f'VERSION:{self.version}\n' \
                     f'CALSCALE:{self.calscale}\n' \
                     f'METHOD:{self.method}\n' \
                     f'CLASS:{self._class}\n' \
                     f'{self.v_timezone}\n'
        for event in self.v_events:
            v_calendar = v_calendar + event.to_string() + '\n'
        v_calendar += f'END:VCALENDAR'
        return v_calendar

    def write(self, **kwargs):
        if "path" in kwargs.keys():
            path = kwargs['path']
        else:
            path = "./classes.ics"
        with open(path, "wt",encoding="utf-8") as f:
            f.write(self.to_string())


if __name__ == '__main__':
    vcalender = VCalendar()
    # print(vcalender.to_string())
    vcalender.write()