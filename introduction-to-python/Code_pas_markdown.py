import pandas as pd
import matplotlib as plt
import numpy as np

#Charger le dataframe train 
df = pd.read_csv('introduction-to-python/train.csv')

#On affiche les première lignes
df.head()

#On affiche le nombre de cellule nulle par colonne
df.isnull().sum() 

#On compte le nombre de personnes ayant survecu 
df.groupby('Survived')['PassengerId'].agg(['count'])

#On l'affiche dans un graphique en bar 
df.groupby('Survived')['PassengerId'].agg(
    ['count']
).reset_index().plot(x='Survived', y='count', kind = 'bar', figsize = (10, 10))

plt.pyplot.show()

#Nombre de personne ayant survecu par sexe
df.groupby(
    ['Survived', 'Sex']
)['PassengerId'].agg(['count'])

#Permet de l'afficher de manière plus claire
df.groupby(
    ['Survived', 'Sex']
)['PassengerId'].agg(['count']).unstack()

#On l'affiche dans un graphique en bar
df.groupby(
    ['Survived', 'Sex']
)['PassengerId'].count().unstack().plot(kind ='bar', figsize = (10, 10))

plt.pyplot.show()

#Nombre de survivant par classe
df.groupby(['Survived', 'Pclass'])['PassengerId'].agg(
    ['count']
)

#On l'affiche de manière plus claire 
df.groupby(['Survived', 'Pclass'])['PassengerId'].count().unstack()

#On le plot dans un graphique à bar 
df.groupby(
    ['Survived', 'Pclass']
)['PassengerId'].count().unstack().plot(kind ='bar', figsize = (10, 10))

plt.pyplot.show()

print(type(df)) 

#Taux de survie par âge 
df['generation'] = pd.cut(np.array(df['Age'], 8))

pd.cut(np.array(df['Age']), 8)

df.head()

#Survivant par génération
df.groupby(
    ['Survived', 'generation']
)['PassengerId'].count().unstack().plot(kind ='bar', figsize = (10, 10))

plt.pyplot.show()

#Survivant par tarif 
df['fare_category'] = pd.cut(df['Fare'], 12)

pd.cut(df['Fare'], 10)

#On l'affiche en graphique par bar 
df.groupby(
    ['Survived', 'fare_category']
)['PassengerId'].count().unstack().plot(kind ='bar', figsize = (10, 10))

plt.pyplot.show()

#On regarde les corrélation 
df[['Survived', 'Pclass', 'Age', 'Fare', 'SibSp', 'Parch']].corr()

#Corrélation map
df[['Survived', 'Pclass', 'Age', 'Fare', 'SibSp', 'Parch']].corr().style.background_gradient(cmap='coolwarm')

