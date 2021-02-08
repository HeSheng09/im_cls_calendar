class VTimezone:
    def __init__(self, **kwargs):
        if "tzid" in kwargs.keys():
            self.tzid = kwargs['tzid']
        else:
            self.tzid = "Asia/Shanghai"
        if "tzurl" in kwargs.keys():
            self.tzurl = kwargs['tzurl']
        else:
            self.tzurl = "http://tzurl.org/zoneinfo-outlook/Asia/Shanghai"
        if "x_lic_location" in kwargs.keys():
            self.x_lic_location = kwargs['x_lic_location']
        else:
            self.x_lic_location = "Asia/Shanghai"
        if "standard" in kwargs.keys():
            self.standard = kwargs['standard']
        else:
            self.standard = Standard().to_string()

    def to_string(self):
        return f'BEGIN:VTIMEZONE\n' \
               f'TZID:{self.tzid}\n' \
               f'TZURL:{self.tzurl}\n' \
               f'X-LIC-LOCATION:{self.x_lic_location}\n' \
               f'{self.standard}\n' \
               f'END:VTIMEZONE'


class Standard:
    def __init__(self, **kwargs):
        if "tz_offset_from" in kwargs.keys():
            self.tz_offset_from = kwargs['tz_offset_from']
        else:
            self.tz_offset_from = "+0800"
        if "tz_offset_to" in kwargs.keys():
            self.tz_offset_to = kwargs['tz_offset_to']
        else:
            self.tz_offset_to = "+0800"
        if "tz_name" in kwargs.keys():
            self.tz_name = kwargs['tz_name']
        else:
            self.tz_name = "CST"
        if "dt_start" in kwargs.keys():
            self.dt_start = kwargs['dt_start']
        else:
            self.dt_start = "19700101T000000"

    def to_string(self):
        return f"BEGIN:STANDARD\n" \
               f"TZOFFSETFROM:{self.tz_offset_from}\n" \
               f"TZOFFSETTO:{self.tz_offset_to}\n" \
               f"TZNAME:{self.tz_name}\n" \
               f"DTSTART:{self.dt_start}\n" \
               f"END:STANDARD"


if __name__ == '__main__':
    standard = Standard()
    print(standard.to_string())
    v_timezone = VTimezone()
    print(v_timezone.to_string())
