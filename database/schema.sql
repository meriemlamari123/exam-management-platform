-- تصميم قاعدة البيانات (Relational Schema)

-- 1. الأقسام
CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- 2. الأساتذة (مرتبطون بالأقسام)
CREATE TABLE IF NOT EXISTS professors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    dept_id INTEGER NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE CASCADE
);

-- 3. التخصصات (مرتبطة بالأقسام)
CREATE TABLE IF NOT EXISTS formations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    dept_id INTEGER NOT NULL,
    FOREIGN KEY (dept_id) REFERENCES departments(id) ON DELETE CASCADE
);

-- 4. القاعات (مع تحديد النوع: مدرج أو قاعة)
CREATE TABLE IF NOT EXISTS rooms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    capacity INTEGER NOT NULL CHECK (capacity > 0),
    type TEXT CHECK(type IN ('Amphi', 'Salle')) NOT NULL
);

-- 5. المواد (مرتبطة بالتخصص والأستاذ)
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    formation_id INTEGER NOT NULL,
    prof_responsable_id INTEGER,
    FOREIGN KEY (formation_id) REFERENCES formations(id) ON DELETE CASCADE,
    FOREIGN KEY (prof_responsable_id) REFERENCES professors(id) ON DELETE SET NULL
);

-- 6. الطلاب (مرتبطون بالتخصص)
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    prenom TEXT NOT NULL,
    formation_id INTEGER,
    email TEXT UNIQUE,
    FOREIGN KEY (formation_id) REFERENCES formations(id) ON DELETE SET NULL
);

-- 7. التسجيلات (جدول الربط بين الطالب والمادة)
CREATE TABLE IF NOT EXISTS inscriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    module_id INTEGER NOT NULL,
    note REAL DEFAULT NULL,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE,
    UNIQUE(student_id, module_id)
);

-- 8. الامتحانات (النتيجة النهائية - الجدول الزمني)
CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    exam_date DATE NOT NULL,
    start_time TEXT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES modules(id),
    FOREIGN KEY (room_id) REFERENCES rooms(id)
);