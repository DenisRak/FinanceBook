import json
from datetime import datetime

class FinanceManager:
    def __init__(self, filename):
        """Инициализация объекта FinanceManager."""
        self.filename = filename
        self.records = self.load_records()

    def load_records(self):
        """Загрузка данных из файла."""
        try:
            with open(self.filename, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            self.save_records([])  # Если файл не найден, создаем его
            return []

    def save_records(self, data: list):
        """Сохранение данных в файл."""
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def add_record(self, date: str, category: str, amount: float, description: str):
        """Добавление новой записи."""
        record = {'Дата': date, 'Категория': category, 'Сумма': amount, 'Описание': description}
        self.records.append(record)
        self.save_records(self.records)

    @staticmethod
    def display_record_details(record: dict):
        """Вывод подробной информации."""
        for key, value in record.items():
            print(f"{key}: {value}")
        print()

    def edit_record(self, index: int, date: str, category: str, amount: float, description: str):
        """Изменение существующей записи."""
        new_category = category if category else self.records[index]['Категория']
        new_amount = amount if amount else self.records[index]['Сумма']
        new_description = description if description else self.records[index]['Описание']
        new_record = {'Категория': new_category, 'Сумма': new_amount, 'Описание': new_description, 'Изменен': date}
        self.records[index].update(new_record)
        self.save_records(self.records)

    def search_records(self, category: str ='', date: str ='', amount: str ='') -> list:
        """Метод возвращает список записей по заданным критериям.
        Если критерии не заданы, то возвращает все записи."""
        results = []
        for record in self.records:
            if (category == '' or record['Категория'] == category) and \
               (date == '' or record['Дата'] == date) and \
               (amount == '' or record['Сумма'] == float(amount)):
                results.append(record)
        return results

    def calculate_balance(self, index: int) -> float:
        income = sum(record['Сумма'] for record in self.records if record['Категория'] == 'Доход')
        expenses = sum(record['Сумма'] for record in self.records if record['Категория'] == 'Расход')
        balance = income - expenses
        result = [balance, income, expenses]
        return result[index]

def main():
    finance_manager = FinanceManager('records.json')

    def get_data():
        """Пользовательский ввод новой записи."""
        try:
            date = datetime.now().strftime('%Y-%m-%d')
            category = {"+": "Доход", "-": "Расход"}.get(input("Введите категорию (Доход - '+'/Расход - '-'): "))
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            if category is not None:
                return date, category, amount, description
        except ValueError:
            print("Сумма должна быть числом")

    while True:
        print("\n1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")
        print("5. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            while True:
                print("\n1. Вывод баланса")
                print("2. Вывод дохода")
                print("3. Вывод расхода")
                print("4. Возврат в главное меню")
                subchoice = int(input("Выберите действие: ")) - 1
                if 0 <= subchoice < 3:
                    balance = finance_manager.calculate_balance(subchoice)
                    action = ("баланс", "доход", "расход")
                    print(f"Текущий {action[subchoice]}: {balance}")
                    input("Нажмите Enter для продолжения...")
                elif subchoice == 3:
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")

        elif choice == '2':
            try:
                data = get_data()
                finance_manager.add_record(*data)
                print("Запись успешно добавлена")
                input("Нажмите Enter для продолжения...")
            except Exception:
                print("Неверный выбор. Попробуйте снова.")


        elif choice == '3':
            records_list = finance_manager.search_records()
            for i, dct in enumerate(records_list, 1):
                print(f"Номер записи {i}")
                print(", ".join([f"{k}: {v}" for k, v in dct.items()]))
            try:
                index = int(input("Введите номер записи для редактирования: ")) - 1
                print("Введите изменения. Если критерий не важен, то просто нажмите Enter.")
                date = datetime.now().strftime('%Y-%m-%d')
                category = {"+": "Доход", "-": "Расход"}.get(input("Введите категорию (Доход - '+'/Расход - '-'): "))
                amount = float(input("Введите новую сумму, если сумму менять не нужно, нажмите 0: "))
                description = input("Введите новое описание: ")
                finance_manager.edit_record(index, date, category, amount, description)
                print("Запись успешно изменена.")
            except (ValueError, IndexError):
                print(f"Сумма должна быть числом, индекс не больше {len(records_list)}")

        elif choice == '4':
            try:
                print("Выберите критерии поиска. Если критерий не важен, то просто нажмите Enter.")
                category = input("Введите категорию (Доход/Расход): ")
                date = input("Введите дату (ГГГГ-ММ-ДД): ")
                amount = input("Введите сумму: ")
                results = finance_manager.search_records(category, date, amount)
                if results:
                    print("Найденные записи:")
                    for result in results:
                        finance_manager.display_record_details(result)
                    input("Нажмите Enter для продолжения...")
                else:
                    print("Записи не найдены.")
            except ValueError:
                print("Сумма должна быть числом")

        elif choice == '5':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()
