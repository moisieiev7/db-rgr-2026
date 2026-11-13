import psycopg
import time
from .db import get_connection

class SearchModel:
    @staticmethod
    def search_experiments_by_researcher(name_pattern, start_date_from):
        """Пошук експериментів за ім'ям керівника (LIKE) та датою (діапазон)."""
        conn = get_connection()
        if not conn:
            return None, 0
        
        query = """
            SELECT r.full_name, e.title, e.start_date, e.status
            FROM researchers r
            JOIN experiments e ON r.researcher_id = e.lead_researcher_id
            WHERE r.full_name LIKE %s AND e.start_date >= %s
            ORDER BY e.start_date DESC;
        """
        try:
            with conn.cursor() as cur:
                start_time = time.perf_counter()
                
                cur.execute(query, (f"%{name_pattern}%", start_date_from))
                results = cur.fetchall()
                
                end_time = time.perf_counter()
                
                exec_time_ms = (end_time - start_time) * 1000
                return results, exec_time_ms
                
        except psycopg.Error as e:
            print(f"\n[Помилка БД під час пошуку]: {e}")
            return None, 0
        finally:
            conn.close()

    @staticmethod
    def search_hours_grouped(min_hours, max_hours):
        """Пошук сумарного часу обладнання за експериментами (GROUP BY + числовий діапазон)."""
        conn = get_connection()
        if not conn:
            return None, 0
            
        query = """
            SELECT e.title, SUM(ee.usage_hours) as total_hours
            FROM experiments e
            JOIN experiment_equipment ee ON e.experiment_id = ee.experiment_id
            GROUP BY e.experiment_id, e.title
            HAVING SUM(ee.usage_hours) BETWEEN %s AND %s
            ORDER BY total_hours DESC;
        """
        try:
            with conn.cursor() as cur:
                start_time = time.perf_counter()
                cur.execute(query, (min_hours, max_hours))
                results = cur.fetchall()
                exec_time_ms = (time.perf_counter() - start_time) * 1000
                return results, exec_time_ms
        except psycopg.Error as e:
            print(f"\n[Помилка БД]: {e}")
            return None, 0
        finally:
            conn.close()

    @staticmethod
    def search_equipment_by_status(manufacturer, is_completed):
        """Пошук обладнання за виробником (LIKE) та логічним статусом (True/False)."""
        conn = get_connection()
        if not conn:
            return None, 0
            
        status_filter = 'Завершений' if is_completed else 'У процесі'
        
        query = """
            SELECT eq.name, eq.manufacturer, e.title, e.status
            FROM equipment eq
            JOIN experiment_equipment ee ON eq.equipment_id = ee.equipment_id
            JOIN experiments e ON ee.experiment_id = e.experiment_id
            WHERE eq.manufacturer ILIKE %s AND e.status = %s;
        """
        try:
            with conn.cursor() as cur:
                start_time = time.perf_counter()
                cur.execute(query, (f"%{manufacturer}%", status_filter))
                results = cur.fetchall()
                exec_time_ms = (time.perf_counter() - start_time) * 1000
                return results, exec_time_ms
        except psycopg.Error as e:
            print(f"\n[Помилка БД]: {e}")
            return None, 0
        finally:
            conn.close()