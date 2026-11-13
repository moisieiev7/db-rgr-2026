from app.models.researcher import ResearcherModel
from app.views.console_view import ConsoleView
from app.models.generator import DataGenerator
from app.models.search import SearchModel

class MainController:
    def __init__(self):
        self.model = ResearcherModel()
        self.view = ConsoleView()
        self.generator = DataGenerator()
        self.generator = DataGenerator()
        self.search = SearchModel()

    def run(self):
        while True:
            choice = self.view.show_menu()
            
            if choice == '1':
                self.show_researchers()
            elif choice == '2':
                self.add_researcher()
            elif choice == '3':
                self.delete_researcher()
            elif choice == '4':
                self.generate_data()
            elif choice == '5':
                self.run_search_1()
            elif choice == '6':
                self.run_search_2()
            elif choice == '7':
                self.run_search_3()
            elif choice == '0':
                self.view.show_message("Вихід з програми. До побачення!")
                break
            else:
                self.view.show_message("[Помилка] Невідома команда. Спробуйте ще раз.")

    def show_researchers(self):
        data = self.model.get_all()
        if data is not None:
            self.view.show_researchers(data)

    def add_researcher(self):
        full_name, degree, email = self.view.get_researcher_data()
        if not full_name or not degree or not email:
            self.view.show_message("[Помилка] Усі поля є обов'язковими!")
            return
            
        if self.model.add(full_name, degree, email):
            self.view.show_message("[Успіх] Дослідника успішно додано!")

    def delete_researcher(self):
        r_id = self.view.get_id("Введіть ID дослідника для видалення: ")
        if not r_id.isdigit():
            self.view.show_message("[Помилка] ID має бути числом!")
            return
            
        if self.model.delete(r_id):
            self.view.show_message("[Успіх] Дослідника успішно видалено.")

    def generate_data(self):
        count_str = self.view.get_generation_count()
        if not count_str.isdigit() or int(count_str) <= 0:
            self.view.show_message("[Помилка] Введіть коректне додатне число!")
            return

        count = int(count_str)
        self.view.show_message(f"Генерація {count} записів... Зачекайте.")

        if self.generator.generate_researchers(count):
            self.view.show_message(f"[Успіх] {count} записів успішно додано до таблиці researchers!")

    def run_search_1(self):
        name, date_from = self.view.get_search_params_1()
        if not name or not date_from:
            self.view.show_message("[Помилка] Параметри не можуть бути порожніми.")
            return
            
        results, exec_time = self.search.search_experiments_by_researcher(name, date_from)
        if results is not None:
            self.view.show_search_results(results, exec_time)

    def run_search_2(self):
        min_h, max_h = self.view.get_search_params_2()
        if not min_h.isdigit() or not max_h.isdigit():
            self.view.show_message("[Помилка] Введіть коректні числа.")
            return
            
        results, exec_time = self.search.search_hours_grouped(min_h, max_h)
        if results is not None:
            self.view.show_search_results_2(results, exec_time)

    def run_search_3(self):
        manufacturer, is_completed = self.view.get_search_params_3()
        results, exec_time = self.search.search_equipment_by_status(manufacturer, is_completed)
        if results is not None:
            self.view.show_search_results_3(results, exec_time)