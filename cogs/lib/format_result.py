from datetime import timedelta, datetime
import time


def format_result(value, event, format):
    if value == -1:
        return 'DNF'
    elif value == -2:
        return 'DNS'
    elif value == '' or value == 0:
        return ''
    elif event == '333mbf' and format == 's':
        return mbld_decode(value)
    elif event == '333fm' and format == 's':
        return str(value)
    elif event == '333fm' and format == 'a':
        return str('%.2f' % (value / 100))
    else:
        value /= 100
        if value >= 3600:
            return str(datetime.utcfromtimestamp(value).strftime("%H:%M:%S.%f")[:-4])
        if value >= 60:
            return str(datetime.utcfromtimestamp(value).strftime("%M:%S.%f").lstrip("0").replace(" ","0")[:-4])
        if value >= 1:
            return str(datetime.utcfromtimestamp(value).strftime("%S.%f").lstrip("0").replace(" ","0")[:-4])
        else:
            return "0" + str(datetime.utcfromtimestamp(value).strftime("%S.%f").lstrip("0").replace(" ","0")[:-4])
        return ''


def mbld_decode(value):
    valarr = []
    for i in range(len(str(value))):
        valarr.append(str(value % 10))
        value = value // 10
    difference = 99 - int(valarr[8]+valarr[7])
    secs = int(valarr[6] + valarr[5] + valarr[4] + valarr[3] + valarr[2])
    missed = int(valarr[1] + valarr[0])
    solved = difference + missed
    attempted = solved + missed
    if secs >= 3600:
        timer = datetime.utcfromtimestamp(secs).strftime("%H:%M:%S").lstrip("0").replace(" ","0")
    else:
        timer = datetime.utcfromtimestamp(secs).strftime("%M:%S").lstrip("0").replace(" ","0")
    return str(solved) + "/" + str(attempted) + " " + timer
