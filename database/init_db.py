import sqlite3
import os
import random
from faker import Faker

# إعداد المكتبة لتوليد أسماء فرنسية
fake = Faker('fr_FR')

# تحديد المسار الصحيح لقاعدة البيانات (مهم جداً!)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "university.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")

def init_database():
    print("🚀 DÉBUT DE LA GÉNÉRATION (SQL MODE)...")
    print(f"📂 Base de données cible : {DB_PATH}")
    
    # حذف القاعدة القديمة لبدء نظيف
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("🗑️ Ancienne base supprimée.")
        except PermissionError:
            print("⚠️ Erreur : Fermez le fichier DB ou l'application avant de régénérer.")
            return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. تنفيذ التصميم (Schema)
    print("🛠️ Création de la structure des tables...")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    # 2. توليد البيانات
    print("📥 Injection des données massives...")

    # الأقسام
    depts = ['Informatique', 'Mathématiques', 'Physique', 'Chimie', 'Biologie', 'Génie Civil', 'Économie']
    cursor.executemany("INSERT INTO departments (name) VALUES (?)", [(d,) for d in depts])
    
    # القاعات (150 قاعة)
    salles_data = []
    for i in range(150):
        t = 'Amphi' if i < 40 else 'Salle'
        c = 250 if t == 'Amphi' else 50
        salles_data.append((f"{t} {i+1}", c, t))
    cursor.executemany("INSERT INTO rooms (name, capacity, type) VALUES (?, ?, ?)", salles_data)

    # الأساتذة (1000)
    print("   -> Génération de 1000 Professeurs...")
    profs_data = [(fake.last_name(), fake.first_name(), random.randint(1, 7)) for _ in range(1000)]
    cursor.executemany("INSERT INTO professors (nom, prenom, dept_id) VALUES (?, ?, ?)", profs_data)

    # التخصصات (70)
    print("   -> Génération de 70 Formations...")
    formations_data = [(f"Specialité {fake.word().upper()} L{random.randint(1,3)}", random.randint(1, 7)) for _ in range(70)]
    cursor.executemany("INSERT INTO formations (name, dept_id) VALUES (?, ?)", formations_data)

    # المواد (400)
    print("   -> Génération de 400 Modules...")
    modules_data = [(f"Module {fake.word().capitalize()}", random.randint(1, 70), random.randint(1, 1000)) for _ in range(400)]
    cursor.executemany("INSERT INTO modules (name, formation_id, prof_responsable_id) VALUES (?, ?, ?)", modules_data)

    # الطلاب (13,000)
    print("   -> Génération de 13,000 Étudiants (Patientez)...")
    students_data = []
    for i in range(13000):
        # البريد الإلكتروني يجب أن يكون فريداً
        email = f"etu{i}_{random.randint(1000,9999)}@univ.dz"
        students_data.append((fake.last_name(), fake.first_name(), random.randint(1, 70), email))
    cursor.executemany("INSERT INTO students (nom, prenom, formation_id, email) VALUES (?, ?, ?, ?)", students_data)

    # التسجيلات (Inscriptions)
    print("   -> Création des liens (Inscriptions)...")
    cursor.execute("""
        INSERT INTO inscriptions (student_id, module_id)
        SELECT s.id, m.id 
        FROM students s
        JOIN modules m ON s.formation_id = m.formation_id
    """)

    conn.commit()
    conn.close()
    print("✅ TERMINÉ ! Base de données 'university.db' créée avec succès.")

if __name__ == "__main__":
    init_database()