from flask import Flask, jsonify, request,session
from flask_restx import Resource, Namespace,fields
from models.user import user
from flask_sqlalchemy import SQLAlchemy
import jwt #pip install PyJWT (암, 복호화 확인)
import bcrypt #pip install bcrypt (암호화, 암호일치 확인)
# import pandas as pd 
import sqlite3
import string 
import random
db = SQLAlchemy()

Auth = Namespace(name="auth", description="사용자 인증")
user_fields = Auth.model('User', {  # Model 객체 생성
    'id': fields.String(description='a User Id', required=True, example="CCH@naver.com")
})
user_fields_auth1 = Auth.inherit('User Auth', user_fields, {
    'name': fields.String(description='name', required=True, example="CCH")
})

user_fields_auth2 = Auth.inherit('User Auth', user_fields, {
    'password': fields.String(description='Password', required=True, example="password")
})
# user_fields_auth = Auth.inherit('User Auth', user_fields, {
#     'area': fields.String(description='area', required=True, example="경기도 용인시")
# })
# users = []

# 회원가입 유효성
@Auth.route('/register/<string:id>')
class AuthRegisterCheckId(Resource):
    @Auth.response(200, "Available id")
    @Auth.response(404, "Not found")
    @Auth.response(500, "Unavailable id")
    def get(self,id):
        '''회원가입시 ID유효성 검사'''
        new_user = user.query.filter_by(id=id).first() # id 가 동일한 유저의 정보 저장
        if new_user: return {"message":"Unavailable id"},500 #결과값이 있다면 = 등록된 유저
        else: return {"message":"Available id"},200

#회원가입 요청
@Auth.route('/register')
class AuthRegister(Resource):
    @Auth.expect(user_fields_auth1)
    @Auth.response(200, "Available id")
    @Auth.response(500, "Unavailable id")
    def post(self):
        '''회원가입 성공시 DB에 저장'''
        id = request.json['id']
        name = request.json['name']
        password = request.json['password']
        # area = request.json['area']
        encrypted_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())

        new_user = user(id=id, name=name, password=encrypted_pw) #area도 추후 추가
        db.session.add(new_user)
        db.session.commit()
        return {"message":"User Information saved"},200 #성공
# 로그인
@Auth.route('/login')
class AuthLogin(Resource):
    @Auth.expect(user_fields_auth2)
    @Auth.response(200, "login Success")
    @Auth.response(404, "Not found")
    @Auth.response(500, "login Failed")
    def post(self):
        '''로그인 기능'''
        id = request.json['id']
        password = request.json['password']
        saved_user = user.query.filter_by(id=id).first()
        # saved_user_area = saved_user.area
        #유효하지 않은 ID
        if not saved_user: return{
                "message": "User Not Found"
            }, 404
        # 비밀번호 미일치
        elif not bcrypt.checkpw(password.encode("utf-8"),saved_user.password ):
            return {
                "message": "Auth Failed"
            }, 500
        # 모두 일치
        else: 
            session['login'] = saved_user.id
            return {
                # "message": "login Success ",
                # "area" : saved_user_area,
                "name":saved_user.name
            },200
# #비밀번호 찾기
# @Auth.route('/findpw')
# class AuthFindpw(Resource):
#     @Auth.expect(user_fields_auth1)
#     @Auth.response(200, "Find password")
#     @Auth.response(404, "Not found")
#     @Auth.response(500, "Can't find password")
#     def post(self):
#         '''유저 비밀번호 찾기'''
#         id = request.json['id']
#         name = request.json['name']
#         new_password = request.json['password']
#         saved_user = user.query.filter_by(id=id).first()
#         # encrypted_pw = bcrypt.hashpw(new_password.encode('utf8'),bcrypt.gensalt())
#         if not saved_user: 
#             return{
#                 "message":"User Not Found"
#             },404
#         elif name != saved_user.name:
#             return{
#                 "message":"Wrong user Information"
#             },500
#         else: 
#             saved_user.password = new_password
#             db.session.commit()
#             return {
#                 "message":"password changed"
#             },200
#비밀번호 변경
@Auth.route('/changepw')
class AuthChangepw(Resource):
    @Auth.expect(user_fields_auth1)
    @Auth.response(200, "password Changed")
    @Auth.response(404, "Not found")
    @Auth.response(500, "password change fail")
    def post(self):
        '''유저 비밀번호 변경하기'''
        conn = sqlite3.connect('NaplessRabbit.db')
        cur = conn.cursor()
        id = request.json['id']
        name = request.json['name']
        new_password = request.json['password']
        saved_user = user.query.filter_by(id=id).first()
        sql = "UPDATE user SET password =? WHERE name =?"
        encrypted_pw = bcrypt.hashpw(new_password.encode('utf8'),bcrypt.gensalt())
        if not saved_user: 
            return{
                "message":"User Not Found"
            },404
        elif name != saved_user.name:
            return{
                "message":"Wrong user Information"
            },500
        else: 
            cur.execute(sql, (encrypted_pw, saved_user.name))
            conn.commit()
            return {
                "message":"password changed"
            },200
# 이메일 인증
@Auth.route('/findpw')
class AuthFindpw(Resource):
    @Auth.expect(user_fields_auth1)
    @Auth.response(200, "Find password")
    @Auth.response(404, "Not found")
    @Auth.response(500, "Can't find password")
    def post(self):
        _LENGTH = 6 
        string_pool = string.digits # "0123456789" 
        randNum = "" # 결과 값 
        for i in range(_LENGTH) : # 랜덤한 하나의 숫자를 뽑아서, 문자열 결합. 
            randNum += random.choice(string_pool) 
        randNum = int(randNum) #랜덤 숫자 생성
        # pip install flask flask-mail python-dotenvpip flask-mail-sendgrid




# 로그아웃
@Auth.route('/logout')
class AuthLogout(Resource):
    def post(self):
        '''로그아웃 기능'''
        session.clear()
        return {"message":"logout success"},200


# #회원가입 요청

# @Auth.route('/register/<string:id>/<string:name>/<string:password>/<string:password2>')
# class AuthRegisterSignup(Resource):
#     @Auth.response(200, "Available id")
#     @Auth.response(500, "Unavailable id")
#     def post(self, id, name, password,password2):
#         '''회원가입 성공시 DB에 저장'''
#         # 1차, 2차 비밀번호 검증
#         if password == password2:
#             encrypted_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
#             new_user = user(id=id, name=name, password=encrypted_pw)
#             db.session.add(new_user)
#             db.session.commit()
#             return {"message":"User Information saved"},200 #성공
#         else: return{"message":"2차 비밀번호를 다시 입력해주십시오"},500 #실패
# 
# 로그인
# @Auth.route('/login/<string:id>/<string:password>')
# class AuthLogin(Resource):
#     @Auth.response(200, "login Success")
#     @Auth.response(404, "Not found")
#     @Auth.response(500, "login Failed")
#     def post(self,id,password):
#         '''로그인 기능'''
#         saved_user = user.query.filter_by(id=id).first()
#         saved_user_pw = saved_user.password
#         # encrypted_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
#         #유효하지 않은 ID
#         if not user: return{
#                 "message": "User Not Found"
#             }, 404
#         # 비밀번호 미일치
#         elif not bcrypt.checkpw(password.encode("utf-8"),saved_user_pw):
#             return {
#                 "message": "Auth Failed"
#             }, 500
#         # 모두 일치
#         else: return {
#                 "message": "login Success"
#             }, 200
