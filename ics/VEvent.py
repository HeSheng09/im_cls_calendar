import datetime
import json
from ics.VAlarm import VAlarm


class VEvent:
    def __init__(self, **kwargs):
        if "class_time" in kwargs.keys():
            self.class_time = kwargs['class_time']
        else:
            self.class_time = ''
        if "day_term_start" in kwargs.keys():
            self.day_term_start = kwargs['day_term_start']
        else:
            self.day_term_start = ' '
        # 当前时间戳
        if "dt_stamp" in kwargs.keys():
            self.dt_stamp = kwargs['dt_stamp']
        else:
            self.dt_stamp = datetime.datetime.now().strftime('%Y%m%dT%H%M%SZ')
        # event开始时间
        if "dt_start" in kwargs.keys():
            self.dt_start = kwargs['dt_start']
        else:
            self.dt_start = ''
        # event结束时间
        if "dt_end" in kwargs.keys():
            self.dt_end = kwargs['dt_end']
        else:
            self.dt_end = ""
        # 摘要
        if "summary" in kwargs.keys():
            self.summary = kwargs['summary']
        else:
            self.summary = ""
        # 事件规则
        if "rrule" in kwargs.keys():
            self.rrule = kwargs['rrule']
        else:
            self.rrule = ""
        if "uid" in kwargs.keys():
            self.uid = kwargs['uid']
        else:
            self.uid = ""
        if "tzid" in kwargs.keys():
            self.tzid = kwargs['tzid']
        else:
            self.tzid = "Asia/Shanghai"
        # 事件描述
        if "description" in kwargs.keys():
            self.description = kwargs['description']
        else:
            self.description = ""
        # 事件地点
        if "location" in kwargs.keys():
            self.location = kwargs['location']
        else:
            self.location = ""
        # 提醒方式
        if "alarm" in kwargs.keys():
            self.alarm = kwargs['alarm']
        else:
            self.alarm = VAlarm().to_string()

    def day_class_start(self, **kwargs):
        if 'start_week' in kwargs.keys():
            start_week = int(kwargs['start_week'])
        else:
            start_week = 1
        if 'week_day' in kwargs.keys():
            week_day = int(kwargs['week_day'])
        else:
            week_day = 0
        delta_days = (start_week - 1) * 7 + week_day
        return (datetime.datetime.strptime(self.day_term_start, "%Y%m%d") + datetime.timedelta(delta_days)).strftime(
            "%Y%m%d")

    def set_dt_start(self, **kwargs):
        if 'start_lesson' in kwargs.keys():
            start_lesson = int(kwargs['start_lesson'])
        else:
            start_lesson = 1
        if 'delta_tz' in kwargs.keys():
            delta_tz = int(kwargs['delta_tz'])
        else:
            delta_tz = 0
        hms = (datetime.datetime.strptime(self.class_time[start_lesson - 1]['startTime'], "%H%M%S") + datetime.timedelta(
            hours=delta_tz)).strftime("%H%M%S")
        self.dt_start = self.day_class_start(**kwargs) + "T" + hms

    def set_dt_end(self, **kwargs):
        if 'end_lesson' in kwargs.keys():
            end_lesson = int(kwargs['end_lesson'])
        else:
            end_lesson = 1
        if 'delta_tz' in kwargs.keys():
            delta_tz = int(kwargs['delta_tz'])
        else:
            delta_tz = 0
        hms = (datetime.datetime.strptime(self.class_time[end_lesson - 1]['endTime'], "%H%M%S") + datetime.timedelta(
            hours=delta_tz)).strftime("%H%M%S")
        self.dt_end = self.day_class_start(**kwargs) + "T" + hms

    def set_rrule(self, **kwargs):
        if 'end_week' in kwargs:
            end_week = int(kwargs['end_week'])
        else:
            end_week = 1
        if 'week_day' in kwargs.keys():
            week_day = int(kwargs['week_day'])
        else:
            week_day = 0
        if 'interval' in kwargs.keys():
            interval = kwargs['interval']
        else:
            interval = 1
        delta_days = (end_week - 1) * 7 + week_day + 1
        ddl = (datetime.datetime.strptime(self.day_term_start, "%Y%m%d") + datetime.timedelta(delta_days)).strftime(
            "%Y%m%d") + "T000000"
        week_titles = ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA']
        self.rrule = Rrule(until=ddl, byday=week_titles[week_day], interval=interval).to_string()

    def set_time_attr(self, **kwargs):
        self.set_dt_start(**kwargs)
        self.set_dt_end(**kwargs)
        self.set_rrule(**kwargs)

    def to_string(self):
        return f'BEGIN:VEVENT\n' \
               f'DTSTAMP:{self.dt_stamp}\n' \
               f'DTSTART;TZID=Asia/Shanghai:{self.dt_start}\n' \
               f'DTEND;TZID=Asia/Shanghai:{self.dt_end}\n' \
               f'SUMMARY:{self.summary}\n' \
               f'{self.rrule}\n' \
               f'UID:{self.uid}\n' \
               f'TZID:{self.tzid}\n' \
               f'DESCRIPTION:{self.description}\n' \
               f'LOCATION:{self.location}\n' \
               f'{self.alarm}\n' \
               f'END:VEVENT'


class Rrule:
    def __init__(self, **kwargs):
        if "freq" in kwargs.keys():
            self.freq = kwargs['freq']
        else:
            self.freq = 'WEEKLY'
        if "wkst" in kwargs.keys():
            self.wkst = kwargs['wkst']
        else:
            self.wkst = 'SU'
        if "until" in kwargs.keys():
            self.until = kwargs['until']
        else:
            self.until = ''
        if "interval" in kwargs.keys():
            self.interval = kwargs['interval']
        else:
            self.interval = 1
        if "byday" in kwargs.keys():
            self.byday = kwargs['byday']
        else:
            self.byday = 'SU'

    def to_string(self):
        return f'RRULE:FREQ={self.freq};WKST={self.wkst};UNTIL={self.until};INTERVAL={self.interval};BYDAY={self.byday}'


if __name__ == '__main__':
    with open("../config/config.json", "rt", encoding="utf-8") as f:
        jsonInfo = json.load(f)
    v_event = VEvent(uid="hesheng", class_time=jsonInfo['classTime'], day_term_start=jsonInfo['day_term_start'])
    # v_event.set_dt_start(start_week=1, start_lesson=3, week_day=1)
    # v_event.set_dt_end(start_week=1, end_lesson=5, week_day=1)
    # v_event.set_rrule(end_week=2,week_day=1)
    v_event.set_time_attr(start_week=1, end_week=2, start_lesson=3, end_lesson=5, week_day=1)
    print(v_event.to_string())
