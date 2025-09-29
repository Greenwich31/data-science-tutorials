import streamlit as st
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# Charger le dataset
df = pd.read_csv("introduction-to-python/train.csv")
df['generation'] = pd.cut(np.array(df['Age'], 8))

# Titre
st.title("Statistiques de la catastrophe du Titanic")

st.write("### Distribution des survivants et décédés")

# Menu déroulant pour choisir la variable de croisement
option = st.selectbox(
    "Sélectionnez une variable à croiser avec le statut de survie :",
    ("Aucune", "Sexe", "Classe","Generation"),
    index=0
)

# Mapping pour correspondre aux noms de colonnes
mapping = {
    "Aucune": None,
    "Sexe": "Sex",
    "Classe": "Pclass",
    "Génération": "generation"
}

var = mapping[option]

# Création du graphique
fig, ax = plt.subplots()

if var is None:
    # Histogramme simple
    df["Survived"].value_counts().sort_index().plot(
        kind="bar",
        ax=ax,
        color=["red", "green"],
        alpha=0.7
    )
    ax.set_xlabel("Statut de survie")
    ax.set_xticklabels(["Décédés", "Survivants"], rotation=0)
    ax.set_ylabel("Nombre de passagers")
    ax.set_title("Histogramme des survivants et décédés")
else:
    # Histogramme groupé par variable choisie
    cross = pd.crosstab(df[var], df["Survived"])
    cross.plot(
        kind="bar",
        ax=ax,
        color=["red", "green"],
        alpha=0.7
    )
    ax.set_xlabel(option)
    ax.set_ylabel("Nombre de passagers")
    ax.set_title(f"Survivants vs Décédés selon {option.lower()}")
    ax.legend(["Décédés", "Survivants"])

# Afficher le graphique
st.pyplot(fig)

st.write("### Distribution des survivants par âge")

min_age, max_age = st.slider(
    "Sélectionnez l'intervalle d'âge des passagers :",
    min_value=0,
    max_value=100,
    value=(0, 100)
)
filtered_df = df[(df["Age"] >= min_age) & (df["Age"] <= max_age)]
st.write(f"Nombre de passagers sélectionnés : {len(filtered_df)}")

fig2, ax = plt.subplots()

filtered_df["Survived"].value_counts().sort_index().plot(
    kind="bar",
    ax=ax,
    color=["red", "green"],
    alpha=0.7
)
ax.set_xlabel("Statut de survie")
ax.set_xticklabels(["Décédés", "Survivants"], rotation=0)
ax.set_ylabel("Nombre de passagers")
ax.set_title("Histogramme des survivants et décédés")

st.pyplot(fig2)

st.write("Vous trouverez ci-dessous le dataset complet")
st.write(df)

#Pour lancer l'application mettre ça dans le terminal :
#python -m streamlit run introduction-to-python/app_streamlit.py
