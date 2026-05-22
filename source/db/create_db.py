from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, DateTime, Float, PrimaryKeyConstraint

from db.connection import db_connect

engine = db_connect()
Base = declarative_base()

metrics = [
        "temperature_2m",
        "rain",
        "precipitation_probability",
        "relative_humidity_2m",
        "wind_speed_10m"
    ]

class HourlyData(Base):
    __tablename__ = 'hourly_data'

    forecast_time = Column(DateTime)
    consult_time = Column(DateTime)

    temperature_2m = Column(Float)
    rain = Column(Float)
    precipitation_probability = Column(Float)
    relative_humidity_2m = Column(Float)
    wind_speed_10m = Column(Float)

    temperature_2m_variance = Column(Float)
    rain_variance = Column(Float)
    precipitation_probability_variance = Column(Float)
    relative_humidity_2m_variance = Column(Float)
    wind_speed_10m_variance = Column(Float)

    __table_args__ = (PrimaryKeyConstraint('forecast_time', 'consult_time'),)

Base.metadata.create_all(engine)