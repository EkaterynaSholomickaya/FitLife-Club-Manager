from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import date, datetime


Base = declarative_base()
engine = create_engine("postgresql+psycopg2://postgres:12345@localhost:5432/fitlife_db?client_encoding=utf8")
Session = sessionmaker(bind=engine)
session = Session()


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    membership_end = Column(Date)

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True)
    type = Column(String(100))
    duration = Column(Integer)

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    att_date = Column(Date, default=date.today())


Base.metadata.create_all(engine)
# workouts = session.query(Workouts).all()
# for workout in workouts:
#     print(f"{workout.type}: {workout.duration}")
#
