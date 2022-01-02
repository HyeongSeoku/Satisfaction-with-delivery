from flask import jsonify
from flask_restx import Resource, Namespace,fields
from models import deliveryfreq_by_time_area as d
from models import freqavg as fa, freqavg_by_area1 as fa1
from models import area1_for_exception as a1, area2_for_exception as a2
from models import freqavg_by_day1 as fd1, freqavg_by_day2 as fd2
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()
deliveryfreq = Namespace("delivery", description="deliveryfreq_by_time_area")
area = deliveryfreq.model('Area', {  # Model 객체 생성
    'area1': fields.String(description='area1_City_Do', required=True, example="서울특별시"),
    'area2': fields.String(description='area2_Si_Gun_Gu', required=True, example="강남구")
})

def exceptionForArea(area1,area2):
    area1_list = [row.area1 for row in a1.query.all()]
    area2_list = ["전체"] + [row.area2 for row in a2.query.filter_by(area1=area1).all()]
    if area1 not in area1_list:
        return {"message":"Unavailable area1"}, 400
    elif area2 not in area2_list:
        return {"message":"Unavailable area2"}, 400
    return 

# 시군구 입력 -> 시간대별 평균
# area1과 area2에 따라 0~23에 해당하는 배달건수 평균값 보내주기
# 시군구 전체 데이터를 보고 싶으면 area2에 '전체'를 보내주기
@deliveryfreq.route('/getFreq/<string:area1>/<string:area2>')
class getFreq(Resource):
    @deliveryfreq.expect(area)
    def get(self, area1, area2):
        '''해당 시군구와 일치하는 시간대별 배달건수 평균을 가져옵니다.''' 
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

@deliveryfreq.route('/getFreqByDay/<string:area1>/<string:area2>')
class getFreqByDay(Resource):
    @deliveryfreq.expect(area)
    def get(self, area1, area2):
        '''해당 시군구와 일치하는 요일별 배달건수 평균을 가져옵니다.''' 
        if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
        # dayLst = ['월', '화', '수', '목', '금', '토','일']
        # result = list({'day':i, 'freqavg': 0} for i in dayLst)
        if area2 == '전체':
            rows = fd1.query.filter_by(area1=area1).all()
        else:   
            rows = fd2.query.filter_by(area1=area1, area2=area2).all()
        items = [row.as_dict() for row in rows]
        # Lst = [row.day for row in rows]
        # print(f'items:{items}')
        # print(f'Lst:{Lst}')
        return jsonify(items)


@deliveryfreq.route('/getFreqByYear/<int:year>/<string:area1>/<string:area2>')
class getFreqByYear(Resource): 
    def get(self,year,area1,area2):
        '''해당 연도와 시군구와 일치하는 시간대별 배달건수 평균을 가져옵니다.'''
        if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)

        start = date(year=year, month=1, day=1)
        end = date(year=year, month=12, day=31)
        if area2 == '전체':
            rows = d.query.filter(d.date >= start, d.date <= end).filter_by(
                area1_City_Do=area1).all()
        else:
            rows = d.query.filter(d.date >= start, d.date <= end).filter_by(
                area1_City_Do=area1, area2_Si_Gun_Gu=area2).all()
        data = {}
        a = {}
        for row in rows:
            time = int(row.time)
            freq = int(row.delivery_freq)
            try:
                data[time] += freq
                a[time] += 1
            except KeyError:
                data[time] = freq
                a[time] = 1
        for key in data.keys():
            data[key] = round(data[key]/a[key])
        return jsonify(json_list=data)

# 시군구 입력 -> 시간대별 총합
# 시군구 전체 데이터를 보고 싶으면 area2에 '전체'를 보내주기


@deliveryfreq.route('/getSum/<int:year>/<string:area1>/<string:area2>')
class getSum(Resource):
    def get(self, year, area1, area2):
        if exceptionForArea(area1,area2): return exceptionForArea(area1,area2)
            
        '''해당 연도와 시군구와 일치하는 시간대별 배달건수 총합을 가져옵니다.'''
        start = date(year=year, month=1, day=1)
        end = date(year=year, month=12, day=31)
        if area2 == '전체':
            rows = d.query.filter(d.date >= start, d.date <= end).filter_by(
                area1_City_Do=area1).all()
        else:
            rows = d.query.filter(d.date >= start, d.date <= end).filter_by(
                area1_City_Do=area1, area2_Si_Gun_Gu=area2).all()
        data = {}
        for row in rows:
            time = int(row.time)
            freq = int(row.delivery_freq)
            try:
                data[time] += freq
            except KeyError:
                data[time] = freq
        return jsonify(json_list=data)


# 보류
# 시간대별 평균 배달건수 top 3 (2019,2020,2021 다 주기)
# 시군구 전체 데이터를 보고 싶으면 area2에 '전체'를 보내주기
# 점심:0, 저녁:1, 야식:2 - 나중에 회의 후 수정

# @deliveryfreq.route('/yearTop3/<string:area1>/<string:area2>/<int:peakTime>')
# @deliveryfreq.response(200, "Found")
# @deliveryfreq.response(404, "Not found")
# @deliveryfreq.response(500, "Internal Error")
# class yearTop3(Resource):
#     def get(self, area1, area2, peakTime):
#         '''2019~2021년에 해당하는 시간대별 top3 동을 가져옵니다. '''
#         data = {}
#         test = d.query.first()
#         print(type(test.date.year))
#         # years = [2019,2020,2021]
#         # peakTime_list = [(11,13), (17,20), (21,23)] # 점심(11~13) or 저녁(17~20) or 야식(21~23)
#         # s = peakTime_list[peakTime][0]
#         # e = peakTime_list[peakTime][1]
#         # for year in years:
#         #     if area2=='전체':
#         #         query  = .filter(d.date.year==year,d.time>=s,d.time<=e).filter_by(area1_City_Do=area1)
#         #     else:
#         #         query  = d.query.filter(d.date.year==year,d.time>=s,d.time<=e).filter_by(area1_City_Do=area1,area2_Si_Gun_Gu=area2)
#         #     df = pd.read_sql(query.statement, query.session.bind)
#         #     print(f'---{year}---')
#         #     print(df.groupby('area3_Dong')['delivery_freq'].mean().sort_values(by='delivery_freq',ascending=False).reset_index().head(3))
#         return jsonify(json_list=test.date.year)
