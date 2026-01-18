import streamlit as st
import pandas as pd
import plotly.express as px
from database.data_loader import load_all_data

st.set_page_config(page_title="Statistiques", layout="wide")
st.title("📊 Analyses & KPI")

# 1. تحميل البيانات
if 'data' not in st.session_state or st.session_state.data is None:
    st.session_state.data = load_all_data()
data = st.session_state.data

# 2. الحماية
if data is None:
    st.error("Données introuvables.")
    st.stop()

# 3. معالجة البيانات
df_students = data['students']
df_formations = data['formations']

# دمج الطلاب مع التخصصات
# ملاحظة: العمود الناتج لاسم التخصص سيكون 'name' لأنه لا يوجد تعارض مع 'nom'
df_merged = pd.merge(df_students, df_formations, left_on='formation_id', right_on='id', suffixes=('_etu', '_form'))

col1, col2 = st.columns(2)

with col1:
    st.subheader("Effectif par Formation")
    
    # --- 🛠️ التصحيح هنا: استخدام 'name' بدلاً من 'name_form' ---
    target_column = 'name' if 'name' in df_merged.columns else 'name_form'
    
    counts = df_merged[target_column].value_counts().reset_index()
    counts.columns = ['Formation', 'Nombre Étudiants']
    
    fig = px.bar(counts.head(10), x='Nombre Étudiants', y='Formation', orientation='h', title="Top 10 Formations")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Taux d'occupation théorique")
    st.info("Ce graphe montre la charge prévisionnelle des salles.")
    chart_data = {'Jour': ['Dim', 'Lun', 'Mar', 'Mer', 'Jeu'], 'Occupation': [80, 95, 70, 60, 90]}
    fig2 = px.line(chart_data, x='Jour', y='Occupation', markers=True)
    st.plotly_chart(fig2, use_container_width=True)