import streamlit as st
import pandas as pd
from database.data_loader import load_all_data

st.set_page_config(page_title="Espace Étudiant", layout="wide")
st.title("🔎 Espace Consultation")

if 'data' not in st.session_state or st.session_state.data is None:
    st.session_state.data = load_all_data()
data = st.session_state.data

if data is None:
    st.stop()

st.markdown("""
Ici, un étudiant ou un enseignant peut consulter son planning personnalisé.
Les données sont extraites via des requêtes SQL (Jointures).
""")

search_query = st.text_input("🔍 Rechercher un étudiant par nom (ex: Bernard, Thomas...)", "")

if search_query:
    # البحث عن الطالب
    df_students = data['students']
    results = df_students[df_students['nom'].str.contains(search_query, case=False, na=False)]
    
    if not results.empty:
        selected_student_id = st.selectbox("Résultats trouvés :", results['id'], format_func=lambda x: f"{results[results['id']==x]['nom'].values[0]} {results[results['id']==x]['prenom'].values[0]}")
        
        # عرض جدول الطالب المحدد
        if 'schedule' in data and not data['schedule'].empty:
            # هنا يجب منطقياً جلب المواد التي يدرسها الطالب فقط
            # للتبسيط في العرض، سنعرض الجدول الخاص بتخصص الطالب
            student_info = results[results['id'] == selected_student_id].iloc[0]
            formation_id = student_info['formation_id']
            
            # جلب اسم التخصص
            formation_name = data['formations'][data['formations']['id'] == formation_id]['name'].values[0]
            
            st.success(f"📅 Emploi du temps pour : {student_info['nom']} {student_info['prenom']} ({formation_name})")
            
            # تصفية الجدول (هذا يحاكي استعلام SQL: WHERE formation_id = ...)
            df_schedule = data['schedule']
            
            # ملاحظة: في النسخة الكاملة نربط عبر جدول inscriptions، هنا نعرض جدول التخصص
            if 'formation_name' in df_schedule.columns:
                 my_schedule = df_schedule[df_schedule['formation_name'] == formation_name]
                 if not my_schedule.empty:
                     st.dataframe(my_schedule[['day', 'time', 'module_name', 'room_name']], use_container_width=True)
                 else:
                     st.info("Aucun examen planifié pour votre formation pour l'instant.")
        else:
            st.warning("Le planning global n'a pas encore été généré.")
    else:
        st.warning("Aucun étudiant trouvé.")