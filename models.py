from sqlalchemy import Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# DailySummary table: stores daily weather summary data
class DailySummary(Base):
    __tablename__ = 'daily_summaries'
    
    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    avg_temp = Column(Float, nullable=False)
    max_temp = Column(Float, nullable=False)
    min_temp = Column(Float, nullable=False)
    dominant_condition = Column(String, nullable=False)

# Alert table: logs alerts when temperature exceeds threshold
class Alert(Base):
    __tablename__ = 'alerts'
    
    id = Column(Integer, primary_key=True)
    city = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    condition = Column(String, nullable=False)
