import os
import glob
import logging
import pandas as pd
import src.config as config

class OrderAnalyzer:
        def __init__(self):
            #Сразу настраиваем логгер ошибок
            self._setup_logging()
            self.results = [] #Список для хранения итоговых метрик по каждому файлу

        def _setup_logging(self):
            logging.basicConfig(
                filename=config.LOG_FILE,
                level=logging.ERROR,
                format='%(asctime)s - %(levelname)s - %(message)s',
                encoding='utf-8'
            )

        def process_single_file(self, file_path):
            #Обработка одного конкретного CSV
            try:
                #Читаем CSV с помощью pandas
                df = pd.read_csv(file_path)

                #Проверка 1: пустой ли файл?
                if df.empty:
                    raise ValueError("Файл не содержит данных")

                #Проверка 2: Есть ли нужные колонки?
                required_columns = [config.STATUS_COLUMN, config.AMOUNT_COLUMN]
                for col in required_columns:
                    if col not in df.columns:
                        raise ValueError(f"Отсутствует обязательная колонка: '{col}'")

                #Проверка 3: Устойчивость на неверные значения в total_amount
                df[config.AMOUNT_COLUMN] = pd.to_numeric(df[config.AMOUNT_COLUMN], errors='coerce')

                #Фильтруем: оставляем только заказы со статусом 'Delivered'
                filtred_df = df[df[config.STATUS_COLUMN] == config.STATUS_TARGET]

                #Считаем метрики
                total_orders = len(filtred_df)

                if total_orders > 0:
                    total_revenue = filtred_df[config.AMOUNT_COLUMN].sum()
                    avg_check = filtred_df[config.AMOUNT_COLUMN].mean()
                else:
                    total_revenue = 0.0
                    avg_check = 0.0

                #Возвращаем словарь с метриками для файла
                return {
                    'file_name': os.path.basename(file_path),
                    'total_revenue': round(float(total_revenue), 2),
                    'avg_check': round(float(avg_check), 2),
                    'total_orders': int(total_orders)
                }
            except Exception as e:
                #Если файл битый - складываем в лог
                logging.error(f"Ошибка при обработке файла {os.path.basename(file_path)}: {str(e)}")
                raise e



        def process_all_files(self):
            #Пакетный обход всех файлов в папке /data
            search_pattern = os.path.join(config.DATA_DIR, "*.csv")
            csv_files = glob.glob(search_pattern)

            success_count = 0
            error_count = 0

            for file_path in csv_files:
                if os.path.basename(file_path) == os.path.basename(config.REPORT_FILE):
                    continue

                try:
                    file_metrics = self.process_single_file(file_path)
                    self.results.append(file_metrics)
                    success_count += 1
                except Exception:
                    error_count += 1

            #Если есть успешные файлы - сохраняем отчёт
            if self.results:
                result_df = pd.DataFrame(self.results)
                result_df.to_csv(config.REPORT_FILE, index=False)

            return success_count, error_count
