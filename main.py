from ics import VCalendar, VEvent, Rrule
import json
import re

week_titles = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']


def decode_lesson(lesson, other_info):
    # ['1', '11', '1', '11', '13', '3', '1', '302']
    # 周二:1-11周,每1周;11-13节,3区,1-302
    if lesson == '':
        return decode_practice_lesson(other_info)
    week_day = week_titles.index(lesson[0:2])
    data = re.findall(r"\d+\.?\d*", lesson)
    temp = lesson.split(',')
    if len(temp) == 2:
        location = other_info.split(';')[0].split(',')[-1]
    else:
        location = temp[-2] + ',' + temp[-1]
    return {'header': '【上课】', 'week_day': week_day, 'start_week': int(data[0]), 'end_week': int(data[1]),
            'interval': int(data[2]),
            'start_lesson': int(data[3]), 'end_lesson': int(data[4]), 'location': location}


def decode_practice_lesson(other_info):
    location = other_info.split(';')[0].split(',')[-1]
    data = re.findall(r"\d+\.?\d*", other_info.split(',')[0])
    if len(data) == 1:
        start_week = int(data[0])
        end_week = int(data[0])
    else:
        start_week = data[0]
        end_week = data[1]
    return {'header': '【实习】', 'week_day': 1, 'start_week': start_week, 'end_week': end_week, 'interval': 1,
            'start_lesson': 1,
            'end_lesson': 5, 'location': location}


if __name__ == '__main__':
    # 读取配置文件
    with open("./config/config.json", "rt", encoding="utf-8") as f:
        jsonInfo = json.load(f)
    # 读取课程信息
    with open("data/classes.txt", "rt", encoding="utf-8") as f:
        classes = f.readlines()
    # 构建events
    events = []
    # delta_tz = -8 # 由于联想平板时区出现异常错位，故对其进行修正
    delta_tz = 0
    for cls in classes:
        cls_info = cls[0:-1].split('$')
        for lesson in cls_info[9].split(' '):
            lesson_info = decode_lesson(lesson, cls_info[10])
            event = VEvent(summary=lesson_info['header'] + cls_info[1], uid='HESHENG2021',
                           class_time=jsonInfo['classTime'], day_term_start=jsonInfo['day_term_start'],
                           location=lesson_info['location'], description=cls_info)
            event.set_time_attr(start_week=lesson_info['start_week'], end_week=lesson_info['end_week'],
                                start_lesson=lesson_info['start_lesson'], end_lesson=lesson_info['end_lesson'],
                                week_day=lesson_info['week_day'], interval=lesson_info['interval'], delta_tz=delta_tz)
            events.append(event)

    # 构建iCalendar
    calendar = VCalendar(events=events)
    # 保存至ics文件中
    calendar.write(path='./result/classes.ics')
