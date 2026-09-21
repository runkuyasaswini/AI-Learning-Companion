from datetime import date, timedelta


def render_streak_calendar(active_dates):

    active = {
        d.strftime("%Y-%m-%d")
        for d in active_dates
    }

    today = date.today()

    start = today - timedelta(days=83)

    days = []

    current = start

    while current <= today:

        days.append(current)

        current += timedelta(days=1)

    month_labels = []

    last_month = ""

    for d in days[::7]:

        month = d.strftime("%b")

        if month != last_month:

            month_labels.append(month)

            last_month = month

        else:

            month_labels.append("")

    html = """
    <style>

    .streak-card{

        border:1px solid #e5e7eb;

        border-radius:16px;

        padding:20px;

        margin-bottom:25px;

    }

    .streak-header{

        display:flex;

        justify-content:space-between;

        margin-bottom:20px;

    }

    .metric{

        text-align:center;

    }

    .metric-title{

        font-size:14px;

        color:#6b7280;

    }

    .metric-value{

        font-size:28px;

        font-weight:bold;

    }

    .months{

        display:grid;

        grid-template-columns:35px repeat(12,1fr);

        margin-left:5px;

        font-size:12px;

        color:#666;

        margin-bottom:8px;

    }

    .calendar{

        display:grid;

        grid-template-columns:35px repeat(12,1fr);

        gap:6px;

        align-items:center;

    }

    .week{

        display:grid;

        grid-template-rows:repeat(7,18px);

        gap:5px;

    }

    .day{

        width:18px;

        height:18px;

        border-radius:4px;

        background:#ebedf0;

    }

    .active{

        background:#22c55e;

    }

    .weekday{

        font-size:12px;

        color:#666;

        height:18px;

    }

    </style>
    """

    html += """
    <div class="streak-card">
    """

    html += """
    <div class="months">
    <div></div>
    """

    for month in month_labels:

        html += f"<div>{month}</div>"

    html += "</div>"

    weekdays = [
        "Mon",
        "Tue",
        "Wed",
        "Thu",
        "Fri",
        "Sat",
        "Sun",
    ]

    html += '<div class="calendar">'

    html += '<div>'

    for day in weekdays:

        html += f'<div class="weekday">{day}</div>'

    html += "</div>"

    for week in range(12):

        html += '<div class="week">'

        for day in range(7):

            idx = week * 7 + day

            if idx >= len(days):

                continue

            current = days[idx]

            css = "day"

            if current.strftime("%Y-%m-%d") in active:

                css += " active"

            html += f"""
            <div
                class="{css}"
                title="{current.strftime('%d %b %Y')}"
            ></div>
            """

        html += "</div>"

    html += "</div></div>"

    return html