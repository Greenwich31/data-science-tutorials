import streamlit as st
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("🚢 Visualisation - Titanic")

# Charger le dataset
df = pd.read_csv("introduction-to-python/train.csv")

# Créer la colonne 'generation'
bins = [0, 18, 35, 60, float('inf')]
labels = ['-18', '18-35', '35-60', '+60']
df['generation'] = pd.cut(df['Age'], bins=bins, labels=labels, right=False)

    # ------------------- Section 1 : Survivants vs Décédés -------------------
st.header("Distribution des survivants et décédés")

option = st.sidebar.selectbox(
        "Sélectionnez une variable à croiser avec le statut de survie :",
        ("Aucune", "Sexe", "Classe", "Generation")
    )

mapping = {
        "Aucune": None,
        "Sexe": "Sex",
        "Classe": "Pclass",
        "Generation": "generation"
    }
var = mapping[option]

fig, ax = plt.subplots()
if var is None:
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
        cross = pd.crosstab(df[var], df["Survived"])
        cross.plot(kind="bar", ax=ax, color=["red", "green"], alpha=0.7)
        ax.set_xlabel(option)
        ax.set_ylabel("Nombre de passagers")
        ax.set_title(f"Survivants vs Décédés selon {option.lower()}")
        ax.legend(["Décédés", "Survivants"])

st.pyplot(fig)

    # ------------------- Section 2 : Distribution par âge -------------------
st.header("Distribution des survivants par âge")

min_age, max_age = st.sidebar.slider(
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

    # ------------------- Section 3 : Dataset complet -------------------
st.header("Dataset complet")
st.write(df)




#python -m streamlit run introduction-to-python/rapport_titanic.py