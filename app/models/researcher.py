import psycopg
from .db import get_connection

class ResearcherModel:
    @staticmethod
    def get_all():
        """Отримує всіх дослідників з бази даних."""
        conn = get_connection()
        if not conn:
            return None
        
        try:
            with conn.cursor() as cur:
                cur.execute("SELECT researcher_id, full_name, academic_degree, email FROM researchers ORDER BY researcher_id;")
                return cur.fetchall()
        except psycopg.Error as e:
            print(f"Помилка БД: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def add(full_name, academic_degree, email):
        """Додає нового дослідника."""
        conn = get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO researchers (full_name, academic_degree, email) VALUES (%s, %s, %s)",
                    (full_name, academic_degree, email)
                )
                conn.commit()
                return True
        except psycopg.IntegrityError as e:
            print("\n[Помилка] Порушення унікальності або цілісності даних (можливо, такий email вже існує).")
            conn.rollback()
            return False
        except psycopg.Error as e:
            print(f"\n[Помилка БД]: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @staticmethod
    def delete(researcher_id):
        """Видаляє дослідника за ID."""
        conn = get_connection()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM researchers WHERE researcher_id = %s", (researcher_id,))
                if cur.rowcount == 0:
                    print(f"\n[Помилка] Дослідника з ID {researcher_id} не знайдено.")
                    return False
                conn.commit()
                return True
        except psycopg.errors.ForeignKeyViolation:
            print("\n[Помилка] Неможливо видалити дослідника, оскільки він керує існуючими експериментами.")
            conn.rollback()
            return False
        except psycopg.Error as e:
            print(f"\n[Помилка БД]: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()