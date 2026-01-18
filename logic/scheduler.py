import pandas as pd
import sqlite3
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "university.db")

def save_schedule_to_db(scheduled_exams_list):
    """
    وظيفة لحفظ النتائج في جدول 'exams' داخل قاعدة البيانات
    """
    print("💾 Sauvegarde en cours vers SQL...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # تنظيف الجدول القديم
    cursor.execute("DELETE FROM exams")
    
    # تحضير البيانات للإدخال
    exams_data = []
    for exam in scheduled_exams_list:
        exams_data.append((
            exam['module_id'],
            exam['room_id'],
            exam['day'],
            exam['time']
        ))
        
    # إدخال سريع (Bulk Insert)
    cursor.executemany("""
        INSERT INTO exams (module_id, room_id, exam_date, start_time)
        VALUES (?, ?, ?, ?)
    """, exams_data)
    
    conn.commit()
    conn.close()
    print("✅ Sauvegarde terminée.")

def schedule_exams(data):
    """
    خوارزمية التوزيع (نسخة مبسطة وسريعة للعرض)
    """
    df_modules = data['modules']
    df_rooms = data['rooms']
    
    # دمج المعلومات لتسهيل التعامل
    df_modules = pd.merge(df_modules, data['formations'], left_on='formation_id', right_on='id', suffixes=('_mod', '_form'))
    
    # الفترات الزمنية المتاحة (أيام حقيقية للامتحانات)
    days = ['2026-01-20', '2026-01-21', '2026-01-22', '2026-01-23', '2026-01-24']
    times = ['08:30', '11:00', '13:30', '16:00']
    all_slots = [(d, t) for d in days for t in times]
    
    scheduled_exams = []
    unscheduled = []
    
    # متغيرات لتتبع الحجز ومنع التعارض
    formation_busy = {}  # لمنع تخصص من اجتياز امتحانين في نفس الوقت
    room_busy = {}       # لمنع حجز قاعة مشغولة
    
    # خلط المواد عشوائياً لتنويع النتيجة كل مرة
    modules_list = df_modules.to_dict('records')
    random.shuffle(modules_list)

    for module in modules_list:
        placed = False
        form_id = module['formation_id']
        
        for slot in all_slots:
            if placed: break
            
            # 1. قيد التخصص: هل الطلاب في هذا التخصص مشغولون؟
            if slot in formation_busy.get(form_id, []):
                continue
                
            # 2. البحث عن قاعة فارغة
            selected_room = None
            # نخلط القاعات لنوزع الحمل
            available_rooms = df_rooms.sample(frac=1).to_dict('records')
            
            for room in available_rooms:
                room_id = room['id']
                if slot not in room_busy.get(room_id, []):
                    selected_room = room
                    break
            
            if selected_room:
                # تم إيجاد مكان وقاعة!
                scheduled_exams.append({
                    'module_id': module['id_mod'],
                    'room_id': selected_room['id'],
                    'day': slot[0],
                    'time': slot[1],
                    # بيانات إضافية للعرض المؤقت (قبل الحفظ)
                    'module_name': module['name_mod'],
                    'room_name': selected_room['name'],
                    'formation_name': module['name_form']
                })
                
                # تحديث المشغولية
                if form_id not in formation_busy: formation_busy[form_id] = []
                formation_busy[form_id].append(slot)
                
                if selected_room['id'] not in room_busy: room_busy[selected_room['id']] = []
                room_busy[selected_room['id']].append(slot)
                
                placed = True
        
        if not placed:
            unscheduled.append(module['name_mod'])

    # حفظ النتائج النهائية في SQL
    if scheduled_exams:
        save_schedule_to_db(scheduled_exams)
        
    return pd.DataFrame(scheduled_exams), unscheduled