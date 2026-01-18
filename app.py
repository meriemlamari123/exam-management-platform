import streamlit as st
import pandas as pd
import plotly.express as px
from database.data_loader import load_all_data
import os

# Configuration de la page (DOIT être en premier)
st.set_page_config(
    page_title="Système de Gestion des Examens",
    page_icon="🎓",
    layout="wide"
)

# Vérifier et initialiser la base de données si nécessaire
from database.db_config import database_exists, get_db_path

if not database_exists():
    st.info("🔄 Première initialisation : génération de la base de données...")
    st.info("⏳ Cela peut prendre 30-60 secondes. Veuillez patienter...")
    
    # Vérifier si le fichier de base existe
    db_path = get_db_path()
    if not os.path.exists(db_path):
        from database.init_db import init_database
        with st.spinner("📊 Génération de 13,000 étudiants, 1,000 professeurs, 400 modules..."):
            init_database()
        st.success("✅ Base de données créée avec succès !")
        st.balloons()
        st.rerun()


with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2997/2997287.png", width=100)
    st.title("Admin Tools")
    if st.button("🔄 Force Refresh Data"):
        st.cache_data.clear()
        st.rerun()

st.title("🎓 Plateforme Universitaire - Gestion des Examens")
st.markdown("### Architecture: Python + SQL (SQLite) + Streamlit")
st.markdown("---")


if 'data' not in st.session_state or st.session_state.data is None:
    with st.spinner("🔌 Connexion à la base de données SQL..."):
        st.session_state.data = load_all_data()

data = st.session_state.data


if data is None:
    st.error("🚨 Erreur Critique : Base de données introuvable !")
    st.warning("Veuillez exécuter le script de génération : python database/init_db.py")
    st.stop()


df_students = data['students']
df_profs = data['profs']
df_modules = data['modules']
df_rooms = data['rooms']

col1, col2, col3, col4 = st.columns(4)
col1.metric("Étudiants Inscrits", f"{len(df_students):,}")
col2.metric("Professeurs", len(df_profs))
col3.metric("Modules", len(df_modules))
col4.metric("Salles Disponibles", len(df_rooms))

st.markdown("---")

c1, c2 = st.columns(2)

with c1:
    st.subheader("📊 Répartition par Type de Salle")
    fig1 = px.pie(df_rooms, names='type', hole=0.4, title="Amphi vs Salle")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("👨‍🏫 Corps Enseignant")
   
    df_prof_dept = pd.merge(df_profs, data['departments'], left_on='dept_id', right_on='id')
    counts = df_prof_dept['name'].value_counts().reset_index()
    counts.columns = ['Département', 'Nombre Profs']
    fig2 = px.bar(counts, x='Département', y='Nombre Profs', color='Nombre Profs')
    st.plotly_chart(fig2, use_container_width=True)