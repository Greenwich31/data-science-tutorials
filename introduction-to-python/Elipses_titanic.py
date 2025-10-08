import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.covariance import EmpiricalCovariance
from matplotlib.patches import Ellipse
import streamlit as st

def generate_gaussian(mean, cov, n=100):
    return np.random.multivariate_normal(mean, cov, n)

def plot_cov_ellipse(cov, pos, nstd=2, ax=None, **kwargs):
    """
    Plot an ellipse representing the covariance matrix.
    cov : 2x2 covariance matrix
    pos : [x0, y0] position of the mean
    nstd : number of standard deviations
    """
    if ax is None:
        ax = plt.gca()
    
    # Eigenvalues and eigenvectors
    vals, vecs = np.linalg.eigh(cov)
    # Sort eigenvalues
    order = vals.argsort()[::-1]
    vals = vals[order]
    vecs = vecs[:, order]

    theta = np.degrees(np.arctan2(*vecs[:,0][::-1]))
    width, height = 2 * nstd * np.sqrt(vals)
    ellipse = Ellipse(xy=pos, width=width, height=height, angle=theta, **kwargs)
    
    ax.add_patch(ellipse)
    return ax

# --- Titre ---
st.title("⚪🚢 Ellipses sur le jeu de données Titanic")

# --- Charger le dataset ---
titanic = pd.read_csv("introduction-to-python/train.csv")

# --- Sélection de colonnes numériques ---
numeric_cols = titanic.select_dtypes(include=np.number).columns.tolist()

col_x = st.sidebar.selectbox("Sélectionnez la première variable :", numeric_cols, index=0)
col_y = st.sidebar.selectbox("Sélectionnez la seconde variable :", numeric_cols, index=1)

# --- Nettoyage : suppression des valeurs manquantes ---
data = titanic[[col_x, col_y]].dropna()
n_deleted = len(titanic) - len(data)
if n_deleted > 0:
    st.warning(f"⚠️ {n_deleted} lignes supprimées à cause de valeurs manquantes dans {col_x} ou {col_y}.")

X = data[[col_x, col_y]].values

# --- Ajustement EmpiricalCovariance ---
cov_estimator = EmpiricalCovariance().fit(X)
mean = cov_estimator.location_
cov_matrix = cov_estimator.covariance_

# --- Affichage de la matrice de covariance ---
st.subheader("Matrice de covariance estimée :")
st.dataframe(pd.DataFrame(cov_matrix, index=[col_x, col_y], columns=[col_x, col_y]))

# --- Tracé du nuage de points + ellipse ---
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter(X[:, 0], X[:, 1], s=20, alpha=0.5, label='Données')
plot_cov_ellipse(cov_matrix, mean, nstd=2, ax=ax, edgecolor='red', facecolor='none', lw=2)

ax.set_xlabel(col_x)
ax.set_ylabel(col_y)
ax.set_title(f"Ellipse de covariance empirique ({col_x} vs {col_y})")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.subheader("Aperçu du jeu de données")
st.dataframe(data)
