from models import session, Client, Workout, Attendance
from datetime import date, timedelta

def initialize_data():
    """Заполнение БД"""
    session.query(Attendance).delete()
    session.query(Workout).delete()
    session.query(Client).delete()

    clients = [
        Client(name="Иван", membership_end=date(2025,11,10)),
        Client(name="Анна", membership_end=date(2025,11,8)),
        Client(name="Егор", membership_end=date(2025,11,9)),
        Client(name="Екатерина", membership_end=date(2025,11,7))
    ]

    workouts = [
        Workout(type='йога', duration=45),
        Workout(type='бокс', duration=90),
        Workout(type='растяжка', duration=60)
    ]

    session.add_all(workouts)
    session.add_all(clients)
    session.commit()

    if __name__ == "__main__":
        initialize_data()