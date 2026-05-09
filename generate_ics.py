import uuid

events = []

# 固定日期节日: (月日, 名称, 描述)
fixed_holidays = [
    ("0214", "情人节", "每年2月14日"),
    ("0308", "妇女节", "每年3月8日"),
    ("0312", "植树节", "每年3月12日"),
    ("0401", "愚人节", "每年4月1日"),
    ("0504", "青年节", "每年5月4日"),
    ("0601", "儿童节", "每年6月1日"),
    ("0701", "建党节", "每年7月1日"),
    ("0801", "建军节", "每年8月1日"),
    ("0910", "教师节", "每年9月10日"),
    ("1031", "万圣节", "每年10月31日"),
    ("1224", "平安夜", "每年12月24日"),
    ("1225", "圣诞节", "每年12月25日"),
]

for date_str, name, desc in fixed_holidays:
    uid = str(uuid.uuid4())
    # DTEND 是次日（全天事件的结束时间，不包含）
    start = f"2025{date_str}"
    # 简单计算次日
    month = int(date_str[:2])
    day = int(date_str[2:])
    from datetime import datetime, timedelta
    d = datetime(2025, month, day) + timedelta(days=1)
    end = d.strftime("%Y%m%d")
    events.append(f"""BEGIN:VEVENT
UID:{uid}
DTSTART;VALUE=DATE:{start}
DTEND;VALUE=DATE:{end}
RRULE:FREQ=YEARLY
SUMMARY:{name}
DESCRIPTION:{desc}
TRANSP:TRANSPARENT
END:VEVENT""")

# 浮动日期节日: (名称, 描述, RRULE, 起始日期)
floating_holidays = [
    ("母亲节", "每年5月第二个星期日", "FREQ=YEARLY;BYMONTH=5;BYDAY=2SU", "20250511"),
    ("父亲节", "每年6月第三个星期日", "FREQ=YEARLY;BYMONTH=6;BYDAY=3SU", "20250615"),
    ("感恩节", "每年11月第四个星期四", "FREQ=YEARLY;BYMONTH=11;BYDAY=4TH", "20251127"),
]

for name, desc, rrule, dtstart in floating_holidays:
    uid = str(uuid.uuid4())
    from datetime import datetime, timedelta
    d = datetime.strptime(dtstart, "%Y%m%d") + timedelta(days=1)
    end = d.strftime("%Y%m%d")
    events.append(f"""BEGIN:VEVENT
UID:{uid}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{end}
RRULE:{rrule}
SUMMARY:{name}
DESCRIPTION:{desc}
TRANSP:TRANSPARENT
END:VEVENT""")

# 生成ics内容
ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//china-holidays-extra//CN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:中国节假日补充
X-WR-TIMEZONE:Asia/Shanghai
X-WR-CALDESC:补充iOS系统日历中缺少的中国公共节日，包括母亲节、父亲节、感恩节、情人节、圣诞节等
"""

for event in events:
    ics_content += "\n" + event + "\n"

ics_content += "END:VCALENDAR\n"

with open("china-holidays-extra.ics", "w", encoding="utf-8", newline="\r\n") as f:
    f.write(ics_content)

print("ics文件已生成")
