

from app import db

class deliveryfreq_by_time_area(db.Model):
    __tablename__ = "deliveryfreq_by_time_area"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    delivery_freq = db.Column(db.Integer, nullable=False)
    area1_City_Do = db.Column(db.String(45), nullable=False)
    area2_Si_Gun_Gu = db.Column(db.String(45), nullable=False)
    area3_Dong = db.Column(db.String(45), nullable=False)


class freqavg_by_day1(db.Model):
    __tablename__ = "freqavg_by_day1"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    area1= db.Column(db.String(45), nullable=False)
    day = db.Column(db.String(1), nullable=False)
    freqavg = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['day','freqavg']}


class freqavg_by_day2(db.Model):
    __tablename__ = "freqavg_by_day2"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    area1= db.Column(db.String(45), nullable=False)
    area2= db.Column(db.String(45), nullable=False)
    day = db.Column(db.String(1), nullable=False)
    freqavg = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['day','freqavg']}

    
    

class user(db.Model):
    __tablename__ = "user"

    id = db.Column(db.String(126), primary_key=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    name = db.Column(db.String(256), nullable=False)
    
class freqavg (db.Model):
    __tablename__ = "freqavg"

    id = db.Column(db.String(10), primary_key=True, nullable=False)
    area1= db.Column(db.String(45), nullable=False)
    area2= db.Column(db.String(45), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    freqavg = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['time','freqavg']}



class freqavg_by_area1 (db.Model):
    __tablename__ = "freqavg_by_area1"

    id = db.Column(db.String(10), primary_key=True, nullable=False)
    area1= db.Column(db.String(45), nullable=False)
    time = db.Column(db.Integer, nullable=False)
    freqavg = db.Column(db.Integer, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['time','freqavg']}

                

class area1_for_exception (db.Model):
    __tablename__ = "area1_for_exception"
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.String(10), primary_key=True, nullable=False)
    area1= db.Column(db.String(45), nullable=False)
    
    

class area2_for_exception (db.Model):
    __tablename__ = "area2_for_exception"
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    area1= db.Column(db.String(45), nullable=False)
    area2= db.Column(db.String(45), nullable=False)


class weather(db.Model):
    __tablename__ = "weather"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    area1_City_Do = db.Column(db.String(45), nullable=False)
    area2_Si_Gun_Gu = db.Column(db.String(45), nullable=False)
    area3_Dong = db.Column(db.String(45), nullable=False)

    temperature = db.Column(db.Integer, nullable=True)
    rain = db.Column(db.Float)
    snow = db.Column(db.Float)
    dust = db.Column(db.Float)
    weather_alert = db.Column(db.String(45))

    

class Corona_info(db.Model):
    __tablename__ = 'Corona_info'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    date = db.Column(db.Date, nullable=False)
    area1_City_Do = db.Column(db.String(45), nullable=False)
    area2_Si_Gun_Gu = db.Column(db.String(45))
    area3_Dong = db.Column(db.String(45))

    distancing_level = db.Column(db.Integer)
    restrict_time = db.Column(db.Integer)
    restrict_headcount = db.Column(db.Integer)

class lon_lat_level1(db.Model):
    __tablename__ = 'lon_lat_level1'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    area1 = db.Column(db.String(45), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['longitude','latitude']}

    
class lon_lat_level2(db.Model):
    __tablename__ = 'lon_lat_level2'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    area1 = db.Column(db.String(45), nullable=False)
    area2 = db.Column(db.String(45), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    
    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['longitude','latitude']}

    
class lon_lat_level3(db.Model):
    __tablename__ = 'lon_lat_level3'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False)
    area1 = db.Column(db.String(45), nullable=False)
    area2 = db.Column(db.String(45), nullable=False)
    area3 = db.Column(db.String(45), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {x.name: getattr(self, x.name) for x in self.__table__.columns if x.name in ['longitude','latitude']}

 


