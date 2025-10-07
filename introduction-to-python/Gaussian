import streamlit as st
import matplotlib as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from sklearn.covariance import EmpiricalCovariance


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

st.title("📊 Gaussian Scatter Matrices - Rapport")
st.sidebar.header("Gaussian Parameters")
mean_x = st.sidebar.slider("Mean X", -10.0, 10.0, 0.0)
mean_y = st.sidebar.slider("Mean Y", -10.0, 10.0, 0.0)

# Variances and covariance
var_x = st.sidebar.slider("Variance X", 0.1, 10.0, 1.0)
var_y = st.sidebar.slider("Variance Y", 0.1, 10.0, 1.0)
cov_xy = st.sidebar.slider("Covariance XY", -5.0, 5.0, 0.0)

    # Construct covariance matrix
cov_matrix = np.array([[var_x, cov_xy],
                       [cov_xy, var_y]])

    # Check positive-semidefinite
if np.any(np.linalg.eigvals(cov_matrix) < 0):
        st.warning("Covariance matrix is not positive-semidefinite!")

    # Generate Gaussian data
data = generate_gaussian([mean_x, mean_y], cov_matrix, n=200)

    # Optional outliers
add_outliers = st.sidebar.checkbox("Add Outliers?")
if add_outliers:
        outlier_mean_x = st.sidebar.slider("Outlier Mean X", -20.0, 20.0, 5.0)
        outlier_mean_y = st.sidebar.slider("Outlier Mean Y", -20.0, 20.0, 5.0)
        outliers = generate_gaussian([outlier_mean_x, outlier_mean_y], cov_matrix, n=10)
        data = np.vstack([data, outliers])

    # Fit EmpiricalCovariance
emp_cov = EmpiricalCovariance().fit(data)
    # Display covariance matrix
st.subheader("Covariance Matrix (EmpiricalCovariance)")
st.dataframe(pd.DataFrame(emp_cov.covariance_, columns=["X", "Y"], index=["X", "Y"]))

    # Scatter plot with ellipse
fig, ax = plt.subplots()
ax.scatter(data[:,0], data[:,1], alpha=0.6)
plot_cov_ellipse(emp_cov.covariance_, emp_cov.location_, ax=ax, edgecolor='red', lw=2, facecolor='none')
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_title("2D Gaussian with Covariance Ellipse")
st.pyplot(fig)