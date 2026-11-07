import os

#Определяем корень проекта
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))

#Настройки путей к директориям
DATA_DIR = os.path.join(BASE_DIR, 'data')
REPORTS_DIR = os.path.join(BASE_DIR, 'reports')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

#Создаём папки, если их нет
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

#Пути к конкретным файлам отчёта и логов
REPORT_FILE = os.path.join(REPORTS_DIR, 'summary_report.csv')
LOG_FILE = os.path.join(LOGS_DIR, 'errors.log')

#Параметры для фильтрации и расчёта данных
STATUS_COLUMN = 'status'
STATUS_TARGET = 'Delivered'
AMOUNT_COLUMN = 'total_amount'