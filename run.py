import os
import sys
import config

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

from src.analyzer import OrderAnalyzer

def main():
        print("----------- Запуска пакетного анализа заказов -----------")

        #Инициируем анализатор
        analyzer = OrderAnalyzer()

        #Запускаем пакетную обработку файлов в data/
        success, errors = analyzer.process_all_files()

        print("\n--- Обработка завершена ---")
        print(f"Успешно обработано файлов: {success}")
        print(f"Файлов с ошибками: {errors}")

        if success > 0:
                print("Сводный отчёт сохранён в: reports/summary_report.csv")
        if errors > 0: 
                print("Внимание! Были ошибки. Подробности указаны в: logs/errors.log")

if __name__ == "__main__":
        main()
    
        