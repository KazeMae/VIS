from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class CityAQI(db.Model):
    __tablename__ = 'city_aqi'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    year = db.Column(db.Integer, nullable=False)  # 年
    month = db.Column(db.Integer, nullable=False)  # 月
    day = db.Column(db.Integer, nullable=False)  # 日
    hour = db.Column(db.Integer, nullable=False)  # 时
    temperature = db.Column(db.Float, nullable=True)  # 气温
    wind_direction = db.Column(db.Integer, nullable=True)  # 风向
    wind_speed = db.Column(db.Float, nullable=True)  # 风速
    precipitation = db.Column(db.Float, nullable=True)  # 降水量
    weather_condition = db.Column(db.String(50), nullable=True)  # 天气现象
    date = db.Column(db.Date, nullable=False)  # 日期
    aqi = db.Column(db.Integer, nullable=False)  # AQI
    air_quality_level = db.Column(db.String(20), nullable=True)  # 质量等级
    pm25 = db.Column(db.Float, nullable=True)  # PM2.5
    pm10 = db.Column(db.Float, nullable=True)  # PM10
    co = db.Column(db.Float, nullable=True)  # CO
    no2 = db.Column(db.Float, nullable=True)  # NO2
    so2 = db.Column(db.Float, nullable=True)  # SO2
    o3 = db.Column(db.Float, nullable=True)  # O3

    def __repr__(self):
        return f'<CityAQI {self.year}-{self.month}-{self.day} {self.hour}:00 AQI={self.aqi}>'


class CheckpointData(db.Model):
    __tablename__ = 'checkpoint_data'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    checkpoint_name = db.Column(db.String(100), nullable=False)  # 卡口名称
    jd = db.Column(db.Float, nullable=False)  # 经度
    wd = db.Column(db.Float, nullable=False)  # 纬度
    period = db.Column(db.String(20), nullable=True)  # 时段
    vehicle_type = db.Column(db.String(50), nullable=True)  # 车辆类型
    vehicle_count = db.Column(db.Integer, nullable=False)  # 过车数量
    year = db.Column(db.Integer, nullable=False)  # 年
    month = db.Column(db.Integer, nullable=False)  # 月
    day = db.Column(db.Integer, nullable=False)  # 日

    def __repr__(self):
        return f'<CheckpointData {self.checkpoint_name} {self.year}-{self.month}-{self.day} {self.period}>'


class StationData(db.Model):
    __tablename__ = 'station_data'

    id = db.Column(db.Integer, primary_key=True)  # 主键
    city = db.Column(db.String(100), nullable=False)  # 城市
    area = db.Column(db.String(100), nullable=False)  # 区域
    station_name = db.Column(db.String(100), nullable=False)  # 站点名称
    station_id = db.Column(db.String(50), nullable=False)  # 站点编号
    year = db.Column(db.Integer, nullable=False)  # 年
    month = db.Column(db.Integer, nullable=False)  # 月
    day = db.Column(db.Integer, nullable=False)  # 日
    hour = db.Column(db.Integer, nullable=False)  # 时
    so2 = db.Column(db.Float, nullable=True)  # SO2
    no2 = db.Column(db.Float, nullable=True)  # NO2
    co = db.Column(db.Float, nullable=True)  # CO
    o3 = db.Column(db.Float, nullable=True)  # O3
    pm10 = db.Column(db.Float, nullable=True)  # PM10
    pm25 = db.Column(db.Float, nullable=True)  # PM2.5
    longitude = db.Column(db.Float, nullable=False)  # 经度
    latitude = db.Column(db.Float, nullable=False)  # 纬度

    def __repr__(self):
        return f'<StationData {self.city} {self.station_name} {self.year}-{self.month}-{self.day} {self.hour}:00>'
