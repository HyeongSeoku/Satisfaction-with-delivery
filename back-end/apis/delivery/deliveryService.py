from flask import jsonify
from flask_restx.fields import String
from models.exception  import area1_for_exception as a1, area2_for_exception as a2
from models.delivery  import freqavg_by_area2 as fa, freqavg_by_area1 as fa1
from models.delivery  import freqavg_by_day1 as fd1, freqavg_by_day2 as fd2
from models.delivery  import freqavg_by_mealtime1 as fm1, freqavg_by_mealtime2 as fm2
from models.delivery  import freqavg_by_holiday1 as fh1, freqavg_by_holiday2 as fh2
from models.delivery  import delta_sum_by_area1 as ds1
from models.delivery  import freqavg_by_weather1 as fw1, freqavg_by_weather2 as fw2

def exceptionForArea1(area1: str):
    area1_list = [row.area1 for row in a1.query.all()]
    if area1 not in area1_list:
        return {"message":"Unavailable area1"}, 400
    return 

def exceptionForArea(area1: str,area2: str):
    area1_list = [row.area1 for row in a1.query.all()]
    area2_list = ["전체"] + [row.area2 for row in a2.query.filter_by(area1=area1).all()]
    if area1 not in area1_list:
        return {"message":"Unavailable area1"}, 400
    elif area2 not in area2_list or (area1 =="세종특별자치시" and area2 !="전체"):
        return {"message":"Unavailable area2"}, 400
    return 

def getFreq(area1: str, area2: str):
    if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
    result = list({'time':i, 'freqavg':0} for i in range(24))
    if area2 == '전체':
        rows = fa1.query.filter_by(area1=area1).all()
    else:   
        rows = fa.query.filter_by(area1=area1, area2=area2).all()
    items = [row.as_dict() for row in rows]
    timeLst = [row.time for row in rows]
    i=0
    for time in timeLst:
        result[time]["freqavg"] = items[i]["freqavg"]
        i+=1
    return jsonify(result)

# 초기화 처리하기
def getFreqByDay(area1: str, area2: str):
    if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
    if area2 == '전체':
        rows = fd1.query.filter_by(area1=area1).all()
    else:   
        rows = fd2.query.filter_by(area1=area1, area2=area2).all()
    items = [row.as_dict() for row in rows]
    return jsonify(items)

def getFreqByMealtime(area1: str, area2: str):
    if area1 == '세종특별자치시':   return {"message":"Unavailable area1"}, 400
    if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
    if area2 == '전체':
        rows = fm1.query.filter_by(area1=area1).all()
    else:   
        rows = fm2.query.filter_by(area1=area1, area2=area2).all()
    items = [row.as_dict() for row in rows]
    return jsonify(items)

def getFreqByHoliday(area1: str, area2: str):
    if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
    if area2 == '전체':
        rows = fh1.query.filter_by(area1=area1).all()
    else:   
        rows = fh2.query.filter_by(area1=area1, area2=area2).all()
    items = [row.as_dict() for row in rows]
    return jsonify(items)

def getDeltaSum(area1: str):
    if exceptionForArea1(area1): return exceptionForArea1(area1)
    rows = ds1.query.filter_by(area1=area1).all()
    items = [row.as_dict() for row in rows]
    return jsonify(items)

def getFreqByWeather(area1: str, area2: str):
    if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
    if area2 == '전체':
        rows = fw1.query.filter_by(area1=area1).all()
    else:   
        rows = fw2.query.filter_by(area1=area1, area2=area2).all()
    items = [row.as_dict() for row in rows]
    return jsonify(items)










