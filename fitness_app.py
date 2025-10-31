from models import session, Client, Workout, Attendance
from datetime import date
from sqlalchemy import func, desc


class FitnessApp:
    def __init__(self):
        self.session = session

    def show_menu(self):
        """Главное меню приложения"""
        while True:
            print("\n" + "=" * 50)
            print("🏋️ ФИТНЕС-КЛУБ - МЕНЮ")
            print("=" * 50)
            print("1. Зарегистрировать посещение")
            print("2. Топ посетителей")
            print("3. Проверка абонементов")
            print("4. Показать всех клиентов")
            print("5. Показать все тренировки")
            print("6. Выход")
            print("=" * 50)

            choice = input("Выберите пункты (1-6): ").strip()

            if choice == '1':
                self.register_attendance()
            elif choice == '2':
                self.top_visitors()
            elif choice == '3':
                self.check_memberships()
            elif choice == '4':
                self.show_all_clients()
            elif choice == '5':
                self.show_all_workouts()
            elif choice == '6':
                print("До свидания!")
                break
            else:
                print("Вы можете выбрать только пункты 1-6")

    def register_attendance(self):
        """1) Зарегистрировать посещение (триггер сработает автоматически при кол-ве тренировок кратным 10)"""
        print("\n" + "=" * 40)
        print("РЕГИСТРАЦИЯ ПОСЕЩЕНИЯ")
        print("=" * 40)

        clients = self.session.query(Client).all()
        print("ДОСТУПНЫЕ КЛИЕНТЫ:")
        for client in clients:
            print(f"   {client.id}. {client.name}")

        workouts = self.session.query(Workout).all()
        print("\nДОСТУПНЫЕ ТРЕНИРОВКИ:")
        for workout in workouts:
            print(f"   {workout.id}. {workout.type} -  {workout.duration} минут ")

        try:
            client_id = int(input("\nВведите ID клиента: "))
            workout_id = int(input("Введите ID тренировки: "))

            client = self.session.query(Client).get(client_id)
            if not client:
                print("Клиент с таким ID не найден!")
                return

            workout = self.session.query(Workout).get(workout_id)
            if not workout:
                print("Тренировка с таким ID не найдена!")
                return

            new_attendance = Attendance(
                client_id=client_id,
                workout_id=workout_id
            )

            self.session.add(new_attendance)
            self.session.commit()

            print(f"✅ Посещение зарегистрировано!")
            print(f"   Клиент: {client.name}, Тренировка: {workout.type}, Дата: {new_attendance.att_date}")
            print("   💡 Триггер автоматически продлит абонемент при 10 посещениях!")

        except ValueError:
            print("Введите корректное ID")
        except Exception as e:
            self.session.rollback()
            print(f"Ошибка: {e}")

    def top_visitors(self):
        """2) Топ посетителей (order_by desc, limit)"""
        print("\n" + "=" * 40)
        print("ТОП 5 ПОСЕТИТЕЛЕЙ")
        print("=" * 40)


        top_visitors = (self.session.query(
            Client.name,
            func.count(Attendance.id).label('visit_count')
        )
                        .join(Attendance, Client.id == Attendance.client_id)
                        .group_by(Client.id, Client.name)
                        .order_by(desc('visit_count'))
                        .limit(5)
                        .all())

        if not top_visitors:
            print("Нет данных о посещениях")
            return

        print("Топ 5 клиентов:")
        for i, (name, visits) in enumerate(top_visitors, 1):
            print(f"   {i}. {name}: {visits} посещений")

    def check_memberships(self):
        """3) Проверка абонементов (filter membership_end < date)"""
        print("\n" + "=" * 40)
        print("ПРОВЕРКА АБОНЕМЕНТОВ")
        print("=" * 40)

        today = date.today()

        expired_memberships = (self.session.query(Client)
                               .filter(Client.membership_end < today)
                               .all())

        active_memberships = (self.session.query(Client)
                              .filter(Client.membership_end >= today)
                              .all())

        print("ПРОСРОЧЕННЫЕ АБОНЕМЕНТЫ:")
        if expired_memberships:
            for client in expired_memberships:
                print(f" {client.name} - истек {client.membership_end}")
        else:
            print("   ✅ Нет просроченных абонементов")

        print(f"\nАКТИВНЫЕ АБОНЕМЕНТЫ:")
        for client in active_memberships:
            print(f" {client.name} - действует до {client.membership_end}")

    def show_all_clients(self):
        """Всех клиенты"""
        print("\n" + "=" * 40)
        print("ВСЕ КЛИЕНТЫ")
        print("=" * 40)

        clients = self.session.query(Client).all()
        if not clients:
            print("Нет клиентов в базе")
            return

        for client in clients:
            print(f"   {client.id}. {client.name} Абонемент до: {client.membership_end}")


    def show_all_workouts(self):
        """Все тренировки"""
        print("\n" + "=" * 40)
        print("ВСЕ ТРЕНИРОВКИ")
        print("=" * 40)

        workouts = self.session.query(Workout).all()
        if not workouts:
            print("📭 Нет тренировок в базе")
            return

        for workout in workouts:
            print(f"   {workout.id}. {workout.type} продолжительность: {workout.duration} мин")



# Запуск приложения
if __name__ == "__main__":
    app = FitnessApp()
    app.show_menu()