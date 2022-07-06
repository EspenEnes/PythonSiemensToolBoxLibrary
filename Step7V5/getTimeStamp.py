from datetime import datetime, timedelta

def GetTimeStamp(strTime):
    try:
        time = bytes(strTime, "ISO-8859-1")
        delta = timedelta(milliseconds=time[0] * 0x1000000 + time[1] * 0x10000 + time[2] * 0x100 + time[3])
        delta += timedelta(days=time[4] * 0x100 + time[5])

        dt = datetime(1984, 1, 1, 0, 0, 0, 0)
        dt += delta
        return dt
    except:
        dt = datetime(1984, 1, 1, 0, 0, 0, 0)
        return dt