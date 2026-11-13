class ConsoleView:
    @staticmethod
    def show_menu():
        print("\n--- ГОЛОВНЕ МЕНЮ ---")
        print("1. Переглянути всіх дослідників")
        print("2. Додати нового дослідника")
        print("3. Видалити дослідника")
        print("4. Згенерувати тестові дані (Дослідники)")
        print("5. Пошук 1: Експерименти за дослідником (Дата >=)")
        print("6. Пошук 2: Сумарний час обладнання (GROUP BY + Діапазон)")
        print("7. Пошук 3: Обладнання за статусом експерименту (True/False)")
        print("0. Вийти")
        return input("Оберіть дію (0-7): ")
        
    @staticmethod
    def get_generation_count():
        return input("\nВведіть кількість записів для генерації (наприклад, 100000): ")

    @staticmethod
    def show_researchers(researchers):
        if not researchers:
            print("\n[Інфо] Список дослідників порожній.")
            return
        
        print("\nID | ПІБ | Науковий ступінь | Email")
        print("-" * 60)
        for r in researchers:
            print(f"{r[0]:>2} | {r[1]:<20} | {r[2]:<15} | {r[3]}")

    @staticmethod
    def get_researcher_data():
        print("\n--- Додавання дослідника ---")
        full_name = input("Введіть ПІБ: ")
        degree = input("Введіть науковий ступінь: ")
        email = input("Введіть email: ")
        return full_name, degree, email

    @staticmethod
    def get_id(prompt="Введіть ID: "):
        return input(f"\n{prompt}")
    
    @staticmethod
    def show_message(msg):
        print(f"\n{msg}")

    @staticmethod
    def get_search_params_1():
        print("\n--- Пошук експериментів ---")
        name = input("Введіть частину ПІБ дослідника (наприклад, 'Іван'): ")
        date_from = input("Введіть початкову дату (РРРР-ММ-ДД, наприклад '2026-01-01'): ")
        return name, date_from

    @staticmethod
    def show_search_results(results, exec_time_ms):
        if not results:
            print(f"\n[Інфо] Нічого не знайдено. (Час виконання: {exec_time_ms:.2f} мс)")
            return
            
        print(f"\nЗнайдено записів: {len(results)}. Час виконання: {exec_time_ms:.2f} мс")
        print("Дослідник | Експеримент | Дата | Статус")
        print("-" * 70)
        for r in results:
            print(f"{r[0][:20]:<20} | {r[1][:25]:<25} | {r[2]} | {r[3]}")

    @staticmethod
    def get_search_params_2():
        print("\n--- Пошук 2 (Сумарний час використання) ---")
        min_h = input("Мінімальна кількість годин: ")
        max_h = input("Максимальна кількість годин: ")
        return min_h, max_h

    @staticmethod
    def show_search_results_2(results, exec_time_ms):
        if not results:
            print(f"\n[Інфо] Нічого не знайдено. (Час: {exec_time_ms:.2f} мс)")
            return
        print(f"\nЗнайдено записів: {len(results)}. Час: {exec_time_ms:.2f} мс")
        print("Експеримент | Сумарні години")
        print("-" * 50)
        for r in results:
            print(f"{r[0][:30]:<30} | {r[1]}")

    @staticmethod
    def get_search_params_3():
        print("\n--- Пошук 3 (Обладнання за статусом) ---")
        manufacturer = input("Виробник (наприклад, 'FLIR' або залишіть порожнім): ")
        status_input = input("Експеримент завершено? (1 - Так/True, 0 - Ні/False): ")
        return manufacturer, status_input == '1'

    @staticmethod
    def show_search_results_3(results, exec_time_ms):
        if not results:
            print(f"\n[Інфо] Нічого не знайдено. (Час: {exec_time_ms:.2f} мс)")
            return
        print(f"\nЗнайдено записів: {len(results)}. Час: {exec_time_ms:.2f} мс")
        print("Прилад | Виробник | Експеримент | Статус")
        print("-" * 75)
        for r in results:
            print(f"{r[0][:20]:<20} | {r[1][:15]:<15} | {r[2][:20]:<20} | {r[3]}")