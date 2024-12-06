from decimal import Decimal

from flask import Flask, jsonify, request
from flask_cors import CORS  # 解决跨域问题
from sqlalchemy import func
import pandas as pd

from backend.models import db, StationData, CityAQI, CheckpointData

# （1）呈现城区气象属性的时变过程，挖掘气象属性间关联关系，尝试短期气象参数预测；
# （2）分析各检测站点的气象污染分布情况与污染差异性；
# （3）对比呈现道路卡口车流量变化的时空分布情况；
# （4）尝试分析监测站点空气质量变化与卡口流量迁移、风场轨迹的关联性，提出面向气象污染的城市交通整治方案：如货车限行、卡口流量管控等；
# （5）其他与主题吻合的扩展功能。

app = Flask(__name__)

# 配置 MySQL 数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/pollution'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

with app.app_context():
    db.create_all()
# 启用跨域
CORS(app)


@app.route('/chart1', methods=['GET'])
def chart1():
    """查询指定区域和年份的数据，并按月份分组计算每个月的污染物平均值"""
    area = request.args.get('area', '东昌府区')
    years = request.args.getlist('year')
    if not years:
        years = ['2020']

    # 使用一次查询，减少多次查询的开销
    data = db.session.query(
        StationData.month,
        func.avg(StationData.so2).label('avg_so2'),
        func.avg(StationData.no2).label('avg_no2'),
        func.avg(StationData.co).label('avg_co'),
        func.avg(StationData.o3).label('avg_o3'),
        func.avg(StationData.pm10).label('avg_pm10'),
        func.avg(StationData.pm25).label('avg_pm25')
    ).filter(
        StationData.area == area,
        StationData.year.in_(years)
    ).group_by(StationData.month).all()

    # 格式化返回数据
    months = [f"{years[0]}-{row.month:02d}" for row in data]
    pollution_data = {
        'so2': [],
        'no2': [],
        'co': [],
        'o3': [],
        'pm10': [],
        'pm25': []
    }

    # 使用循环和字典映射来减少代码重复
    for row in data:
        for key in pollution_data:
            pollution_data[key].append(round(getattr(row, f'avg_{key}', 0), 2))

    # 返回格式化后的数据
    return {
        'months': months,
        'so2': pollution_data['so2'],
        'no2': pollution_data['no2'],
        'co': pollution_data['co'],
        'o3': pollution_data['o3'],
        'pm10': pollution_data['pm10'],
        'pm25': pollution_data['pm25']
    }


@app.route('/chart2', methods=['GET'])
def chart2():
    """污染物与气象变量的相关性"""
    area = request.args.get('area', '东昌府区')
    years = request.args.getlist('year')
    if not years:
        years = ['2020']

    # 获取所有需要的数据一次性查询
    data = db.session.query(
        StationData.so2,
        StationData.no2,
        StationData.co,
        StationData.o3,
        StationData.pm10,
        StationData.pm25
    ).filter(
        StationData.area == area,
        StationData.year.in_(years)
    ).all()

    # 使用 pandas DataFrame 来计算相关性
    df = pd.DataFrame(data, columns=['so2', 'no2', 'co', 'o3', 'pm10', 'pm25'])
    correlation_matrix = df.corr(method='pearson')  # 计算相关性矩阵
    formatted_correlation_matrix = correlation_matrix.applymap(lambda x: round(Decimal(x), 2))

    return {
        'columns': formatted_correlation_matrix.columns.tolist(),
        'data': formatted_correlation_matrix.values.tolist()
    }


@app.route('/chart3', methods=['GET'])
def chart3():
    """查询指定区域所有年份的数据，并按年份计算每个污染物的平均值"""
    area = request.args.get('area', '东昌府区')

    # 获取所有年份的污染物数据
    data = db.session.query(
        StationData.year,
        func.avg(StationData.so2).label('avg_so2'),
        func.avg(StationData.no2).label('avg_no2'),
        func.avg(StationData.co).label('avg_co'),
        func.avg(StationData.o3).label('avg_o3'),
        func.avg(StationData.pm10).label('avg_pm10'),
        func.avg(StationData.pm25).label('avg_pm25')
    ).filter(StationData.area == area).group_by(StationData.year).all()

    # 格式化返回的数据
    years = [str(row.year) for row in data]
    pollution_data = {
        'so2': [],
        'no2': [],
        'co': [],
        'o3': [],
        'pm10': [],
        'pm25': []
    }

    for row in data:
        for key in pollution_data:
            pollution_data[key].append(round(getattr(row, f'avg_{key}', 0), 2))

    return {
        'years': years,
        'so2': pollution_data['so2'],
        'no2': pollution_data['no2'],
        'co': pollution_data['co'],
        'o3': pollution_data['o3'],
        'pm10': pollution_data['pm10'],
        'pm25': pollution_data['pm25']
    }


@app.route('/chart4')
def chart4():
    """查询指定年份的数据，返回气温、风向、风速、降水量等数据，适配多Y轴折线图"""
    # year = request.args.get('year', 2020)
    years = request.args.getlist('year')
    if not years:
        years = ['2020']
    query = db.session.query(
        CityAQI.year,
        CityAQI.month,
        CityAQI.day,
        CityAQI.hour,
        func.avg(CityAQI.temperature).label('avg_temperature'),
        func.avg(CityAQI.wind_direction).label('avg_wind_direction'),
        func.avg(CityAQI.wind_speed).label('avg_wind_speed'),
        func.avg(CityAQI.precipitation).label('avg_precipitation')
    ).filter(CityAQI.year.in_(years))  # 根据年份筛选数据

    # 进行分组，按小时获取各项数据的平均值
    data = query.group_by(CityAQI.year, CityAQI.month, CityAQI.day, CityAQI.hour).all()

    # 格式化返回的数据，适配前端echarts格式
    hours = []
    temperature_data = []
    wind_direction_data = []
    wind_speed_data = []
    precipitation_data = []

    for row in data:
        # 格式化日期为 "YYYY-MM-DD HH:00"
        hours.append(f"{years[0]}-{row.month:02d}-{row.day:02d} {row.hour:02d}:00")
        # 保证返回的小数点后两位
        temperature_data.append(round(Decimal(row.avg_temperature) if row.avg_temperature is not None else 0, 2))
        wind_direction_data.append(
            round(Decimal(row.avg_wind_direction) if row.avg_wind_direction is not None else 0, 2))
        wind_speed_data.append(round(Decimal(row.avg_wind_speed) if row.avg_wind_speed is not None else 0, 2))
        precipitation_data.append(round(Decimal(row.avg_precipitation) if row.avg_precipitation is not None else 0, 2))

    # 返回的数据结构
    return {
        'hours': hours,
        'temperature': temperature_data,
        'wind_direction': wind_direction_data,
        'wind_speed': wind_speed_data,
        'precipitation': precipitation_data
    }


@app.route('/chart5', methods=['GET'])
def chart5():
    """指定年份的空气质量等级分布数据"""
    # year = request.args.get('year', type=int, default=2020)  # 默认年份为2020
    years = request.args.getlist('year')
    if not years:
        years = ['2020']

    # 查询指定年份的空气质量等级分布
    data = db.session.query(
        CityAQI.air_quality_level,
        func.count(CityAQI.air_quality_level).label('count')
    ).filter(CityAQI.year.in_(years)) \
        .group_by(CityAQI.air_quality_level) \
        .all()

    # 格式化返回数据
    result = []
    for row in data:
        result.append({
            'name': row.air_quality_level,
            'value': row.count
        })

    return jsonify(result)


@app.route('/chart6', methods=['GET'])
def chart6():
    """获取所有车辆类型的数量分布以及总数"""
    checkpoint_name = request.args.get('checkPoint', '黄河10')

    # 查询指定站点的车辆类型分布
    data = db.session.query(
        CheckpointData.vehicle_type,
        func.sum(CheckpointData.vehicle_count).label('total_count')
    ).filter(CheckpointData.checkpoint_name == checkpoint_name) \
        .filter(CheckpointData.vehicle_type.isnot(None)) \
        .group_by(CheckpointData.vehicle_type) \
        .all()

    # 计算指定站点的所有车辆总数
    total_vehicles = db.session.query(func.sum(CheckpointData.vehicle_count)) \
        .filter(CheckpointData.checkpoint_name == checkpoint_name) \
        .scalar() or 0

    # 格式化返回数据
    result = []
    for row in data:
        result.append({
            'name': row.vehicle_type,
            'value': row.total_count
        })

    # 将总车辆数添加到结果中
    result.append({
        'name': '总数',
        'value': total_vehicles
    })

    return jsonify(result)


@app.route('/chart7', methods=['GET'])
def chart7():
    """pm2.5变化"""
    result = db.session.query(
        CityAQI.year,
        func.avg(CityAQI.pm25).label('avg_pm25')
    ).group_by(CityAQI.year).all()

    # 格式化返回数据，保留小数点后两位
    data = [{'year': row.year, 'avg_pm25': round(row.avg_pm25, 2)} for row in result]

    return jsonify(data)


@app.route('/map', methods=['GET'])
def get_map_data():
    """查询每个站点的名称、经度、纬度以及过车数量，按过车数量降序排列并返回前10个站点"""
    result = db.session.query(
        CheckpointData.checkpoint_name,
        CheckpointData.jd,
        CheckpointData.wd,
        func.sum(CheckpointData.vehicle_count).label('total_vehicle_count')
    ).group_by(CheckpointData.checkpoint_name, CheckpointData.jd, CheckpointData.wd) \
        .order_by(func.sum(CheckpointData.vehicle_count).desc()) \
        .limit(50).all()  # 返回前10个站点

    data = [{
        'checkpoint_name': row.checkpoint_name,
        'longitude': row.jd,
        'latitude': row.wd,
        'total_vehicle_count': row.total_vehicle_count
    } for row in result]

    return jsonify(data)


@app.route('/timeline', methods=['get'])
def get_timeline():
    years = db.session.query(CityAQI.year).distinct(CityAQI.year).order_by(CityAQI.year).all()

    # 格式化返回年份列表
    years = [year[0] for year in years]

    return jsonify({
        "years": years
    })


@app.route('/areas', methods=['get'])
def get_areas():
    areas = db.session.query(StationData.area).distinct(StationData.area).order_by(StationData.area).all()
    return jsonify({
        "areas": [area[0] for area in areas]
    })


if __name__ == '__main__':
    app.run(debug=True)
