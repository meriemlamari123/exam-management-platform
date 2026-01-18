import streamlit as st
import pandas as pd
from database.data_loader import load_all_data

st.set_page_config(page_title="Départements", layout="wide")

if 'data' not in st.session_state or st.session_state.data is None:
    st.session_state.data = load_all_data()
data = st.session_state.data

if data is None:
    st.stop()

df_depts = data['departments']
df_formations = data['formations']
df_profs = data['profs']

st.title("🏛️ Vue par Département")

# قائمة منسدلة لاختيار القسم
selected_dept = st.selectbox("Sélectionnez un département :", df_depts['name'].unique())

# تصفية البيانات
dept_id = df_depts[df_depts['name'] == selected_dept].iloc[0]['id']
formations_dept = df_formations[df_formations['dept_id'] == dept_id]
profs_dept = df_profs[df_profs['dept_id'] == dept_id]

c1, c2 = st.columns(2)
with c1:
    st.metric("Formations", len(formations_dept))
    st.dataframe(formations_dept[['name']], use_container_width=True)

with c2:
    st.metric("Professeurs", len(profs_dept))
    st.dataframe(profs_dept[['nom', 'prenom']], use_container_width=True)