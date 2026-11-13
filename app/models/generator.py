import psycopg
from .db import get_connection

class DataGenerator:
    @staticmethod
    def generate_researchers(count):
        """Генерує задану кількість псевдовипадкових дослідників."""
        conn = get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                query = """
                INSERT INTO researchers (full_name, academic_degree, email)
                SELECT 
                    'Дослідник ' || id || ' ' || chr(trunc(65+random()*25)::int) || chr(trunc(65+random()*25)::int),
                    (ARRAY['Магістр', 'Кандидат наук', 'Доктор наук', 'PhD'])[floor(random()*4 + 1)],
                    'researcher_' || id || '_' || trunc(random()*100000) || '@lab.kpi.ua'
                FROM generate_series(1, %s) AS id;
                """
                cur.execute(query, (count,))
                conn.commit()
                return True
        except psycopg.Error as e:
            print(f"\n[Помилка генерації БД]: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()