import pandas as pd
import sqlite3
import os

# تحديد المسار الديناميكي لقاعدة البيانات
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "university.db")

def load_all_data():
    """
    يقوم هذا التابع بالاتصال بقاعدة البيانات SQL وجلب الجداول
    """
    if not os.path.exists(DB_PATH):
        # في حالة عدم وجود القاعدة، نرجع None ليتم التعامل معه في الواجهة
        return None

    try:
        conn = sqlite3.connect(DB_PATH)
        
        # قراءة الجداول الأساسية
        data = {
            "students": pd.read_sql("SELECT * FROM students", conn),
            "profs": pd.read_sql("SELECT * FROM professors", conn),
            "modules": pd.read_sql("SELECT * FROM modules", conn),
            "rooms": pd.read_sql("SELECT * FROM rooms", conn),
            "formations": pd.read_sql("SELECT * FROM formations", conn),
            "departments": pd.read_sql("SELECT * FROM departments", conn),
            # جلب الجدول الزمني (النتائج) مع دمج الأسماء للعرض
            "schedule": pd.read_sql("""
                SELECT e.id, m.name as module_name, r.name as room_name, 
                       e.exam_date as day, e.start_time as time, 
                       f.name as formation_name
                FROM exams e
                JOIN modules m ON e.module_id = m.id
                JOIN rooms r ON e.room_id = r.id
                JOIN formations f ON m.formation_id = f.id
            """, conn)
        }
        
        conn.close()
        return data

    except Exception as e:
        print(f"❌ Erreur SQL lors du chargement: {e}")
        return None