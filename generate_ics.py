import uuid
from datetime import datetime, timedelta
from zhdate import ZhDate


def generate_ics():
    events = []

    # ========== 固定日期节日 ==========
    fixed_holidays = [
        ("0214", "情人节", "每年2月14日"),
        ("0308", "妇女节", "每年3月8日"),
        ("0312", "植树节", "每年3月12日"),
        ("0401", "愚人节", "每年4月1日"),
        ("0504", "青年节", "每年5月4日"),
        ("0910", "教师节", "每年9月10日"),
        ("1031", "万圣节", "每年10月31日"),
        ("1224", "平安夜", "每年12月24日"),
        ("1225", "圣诞节", "每年12月25日"),
    ]

    for date_str, name, desc in fixed_holidays:
        uid = str(uuid.uuid4())
        start = f"2025{date_str}"
        month = int(date_str[:2])
        day = int(date_str[2:])
        d = datetime(2025, month, day) + timedelta(days=1)
        end = d.strftime("%Y%m%d")
        events.append(
            f"""BEGIN:VEVENT
UID:{uid}
DTSTART;VALUE=DATE:{start}
DTEND;VALUE=DATE:{end}
RRULE:FREQ=YEARLY
SUMMARY:{name}
DESCRIPTION:{desc}
TRANSP:TRANSPARENT
END:VEVENT"""
        )

    # ========== 浮动日期节日 ==========
    floating_holidays = [
        ("母亲节", "每年5月第二个星期日", "FREQ=YEARLY;BYMONTH=5;BYDAY=2SU", "20250511"),
        ("父亲节", "每年6月第三个星期日", "FREQ=YEARLY;BYMONTH=6;BYDAY=3SU", "20250615"),
        ("感恩节", "每年11月第四个星期四", "FREQ=YEARLY;BYMONTH=11;BYDAY=4TH", "20251127"),
    ]

    for name, desc, rrule, dtstart in floating_holidays:
        uid = str(uuid.uuid4())
        d = datetime.strptime(dtstart, "%Y%m%d") + timedelta(days=1)
        end = d.strftime("%Y%m%d")
        events.append(
            f"""BEGIN:VEVENT
UID:{uid}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{end}
RRULE:{rrule}
SUMMARY:{name}
DESCRIPTION:{desc}
TRANSP:TRANSPARENT
END:VEVENT"""
        )

    # ========== 农历节日（预计算未来年份） ==========
    # 这些节日在 iOS 官方中国节假日订阅中通常缺失
    lunar_holidays = [
        (2, 2, "龙抬头", "农历二月初二"),
        (3, 3, "上巳节", "农历三月初三"),
        (7, 15, "中元节", "农历七月十五"),
        (12, 8, "腊八节", "农历腊月初八"),
        (12, 23, "小年", "农历腊月廿三"),
    ]

    start_year = 2025
    end_year = 2035

    for month, day, name, desc in lunar_holidays:
        uid = str(uuid.uuid4())
        rdates = []
        for year in range(start_year, end_year + 1):
            try:
                lunar = ZhDate(year, month, day)
                solar = lunar.to_datetime()
                rdates.append(solar.strftime("%Y%m%d"))
            except Exception:
                # 跳过无效日期（如某些年份腊月没有廿三）
                continue

        if not rdates:
            continue

        dtstart = rdates[0]
        d = datetime.strptime(dtstart, "%Y%m%d") + timedelta(days=1)
        dtend = d.strftime("%Y%m%d")
        rdate_str = ",".join(rdates)

        events.append(
            f"""BEGIN:VEVENT
UID:{uid}
DTSTART;VALUE=DATE:{dtstart}
DTEND;VALUE=DATE:{dtend}
RDATE;VALUE=DATE:{rdate_str}
SUMMARY:{name}
DESCRIPTION:{desc}
TRANSP:TRANSPARENT
END:VEVENT"""
        )

    # ========== 生成 ICS 内容 ==========
    ics_content = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//china-holidays-extra//CN
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:中国节假日补充
X-WR-TIMEZONE:Asia/Shanghai
X-WR-CALDESC:补充iOS系统日历中缺少的中国公共节日与传统节日，包括母亲节、父亲节、感恩节、情人节、圣诞节、龙抬头、中元节、腊八节等
"""

    for event in events:
        ics_content += "\n" + event + "\n"

    ics_content += "END:VCALENDAR\n"

    with open("china-holidays-extra.ics", "w", encoding="utf-8", newline="\r\n") as f:
        f.write(ics_content)

    print("ics 文件已生成")


if __name__ == "__main__":
    generate_ics()
