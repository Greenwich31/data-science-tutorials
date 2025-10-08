import streamlit as st

page_0 = st.Page("Acceuil.py",title="Accueil")
page_1 = st.Page("rapport_titanic.py",title="Visualisation - Titanic")
page_2 = st.Page("Gaussian.py",title="Gaussian Scatter Matrices")
page_3 = st.Page("Elipses_titanic.py",title="Elipses on Titanic data")
page_4 = st.Page("app_chess.py",title="Pour passer le temps")

pg = st.navigation([page_0,page_1,page_2,page_3,page_4])

pg.run()

#python -m streamlit run introduction-to-python/base_st.py