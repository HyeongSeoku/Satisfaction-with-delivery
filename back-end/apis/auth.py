from flask import jsonify, request
from flask_restx import Resource, Namespace
from models import user
from flask_sqlalchemy import SQLAlchemy
# import pandas as pd 
import jwt #pip install PyJWT (암, 복호화 확인)
import bcrypt #pip install bcrypt (암호화, 암호일치 확인)

db = SQLAlchemy()

Auth = Namespace(name="auth", description="사용자 인증")


users = []

# 회원가입 유효성
@Auth.route('/register/<string:id>')
class AuthRegisterCheckId(Resource):
    @Auth.response(200, "Available id")
    @Auth.response(404, "Not found")
    @Auth.response(500, "Unavailable id")
    
    def get(self,id):
        '''회원가입시 ID유효성 검사'''
        new_user = user.query.filter_by(id=id).first()
        if new_user: return {"message":"Unavailable id"},500
        else: return {"message":"Available id"},200
#회원가입 요청

@Auth.route('/register/<string:id>/<string:name>/<string:password>/<string:password2>')
class AuthRegisterSignup(Resource):
    @Auth.response(200, "Available id")
    @Auth.response(500, "Unavailable id")
    def post(self, id, name, password,password2):
        '''회원가입 성공시 DB에 저장'''
        if password == password2:
            encrypted_pw = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
            new_user = user(id=id, name=name, password=encrypted_pw)
            db.session.add(new_user)
            db.session.commit()
            return {"message":"User Information saved"},200
        else: return{"message":"2차 비밀번호를 다시 입력해주십시오"},500


# 로그인
@Auth.route('/login/<string:id>/<string:password>')
class AuthLogin(Resource):
    @Auth.response(200, "login Success")
    @Auth.response(404, "Not found")
    @Auth.response(500, "login Failed")
    def post(self,id,password):
        '''로그인 기능'''
        saved_user = user.query.filter_by(id=id).first()
        saved_user_pw = saved_user.password
        # encrypted_pw = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
        #유효하지 않은 ID
        if not user: return{
                "message": "User Not Found"
            }, 404
        # 비밀번호 미일치
        elif not bcrypt.checkpw(password.encode("utf-8"),saved_user_pw):
            return {
                "message": "Auth Failed"
            }, 500
        # 모두 일치
        else: return {
                "message": "login Success"
            }, 200
# 로그아웃
@Auth.route('/logout/<string:id>')
class AuthLogout(Resource):
    def get(self):

# #확인
# @Auth.route('/get')
# class AuthGet(Resource):
#     @Auth.doc(responses={200: 'Success'})
#     @Auth.doc(responses={404: 'Login Failed'})
#     def get(self):