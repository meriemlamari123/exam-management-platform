import streamlit as st
from logic.scheduler import schedule_exams
from database.data_loader import load_all_data

st.set_page_config(page_title="Administration", layout="wide")
st.title("⚙️ Génération des Emplois du Temps")

# التحقق من البيانات
if 'data' not in st.session_state or st.session_state.data is None:
    st.session_state.data = load_all_data()
data = st.session_state.data

if data is None:
    st.error("🚨 Données SQL manquantes.")
    st.stop()

tab1, tab2 = st.tabs(["🚀 Lancer l'Algorithme", "💾 Base de Données"])

with tab1:
    st.info("Cet algorithme récupère les contraintes depuis SQL, calcule le planning, et sauvegarde le résultat dans la table 'exams'.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("#### Paramètres")
        st.caption("Algorithm: Constraints Satisfaction Problem (CSP)")
        if st.button("⚡ GÉNÉRER LE PLANNING", type="primary", use_container_width=True):
            with st.status("Traitement en cours...", expanded=True):
                st.write("📥 Lecture des données SQL...")
                st.write("⚙️ Exécution de l'heuristique...")
                
                # استدعاء الخوارزمية
                df_schedule, unscheduled = schedule_exams(data)
                
                st.write("💾 Insertion des résultats (INSERT INTO exams)...")
                
                # تحديث البيانات في الذاكرة لرؤية النتيجة فوراً
                st.session_state.data = load_all_data()
                
            st.success(f"✅ Succès ! {len(df_schedule)} examens planifiés et sauvegardés.")
            st.rerun()

    with col2:
        # عرض النتيجة إن وجدت
        if 'schedule' in data and not data['schedule'].empty:
            st.success("Planning actuel en base de données :")
            st.dataframe(data['schedule'], use_container_width=True)
        else:
            st.warning("⚠️ Aucun planning n'est enregistré actuellement.")

with tab2:
    st.write("Aperçu des tables brutes (Debug Mode):")
    st.write("Table: Modules")
    st.dataframe(data['modules'].head(), use_container_width=True)