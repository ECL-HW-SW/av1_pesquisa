#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import time
import warnings

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Perceptron

from sklearn.neural_network import MLPClassifier

from fixed import Singleton as glob
import ml_av1


# In[2]:


warnings.filterwarnings("ignore")

arquivo = pd.read_csv('out_based_split.csv', sep=';')

y = arquivo['particionado ']
x = arquivo.drop('particionado ', axis = 1)

x_treino, x_teste, y_treino, y_teste = train_test_split(x, y, test_size = 0.3)


# In[3]:


# MODELOS #

# Decision Tree Classifier #
tempo1begin = time.perf_counter()

modelo1 = DecisionTreeClassifier()
print("\n", modelo1.fit(x_treino,y_treino))

tempo1end = time.perf_counter()

# Extra Trees Classifier #
tempo2begin = time.perf_counter()

modelo2 = ExtraTreesClassifier()
print("\n", modelo2.fit(x_treino,y_treino))

tempo2end = time.perf_counter()

# Logistic Regression #
tempo3begin = time.perf_counter()

modelo3 = LogisticRegression()
print("\n", modelo3.fit(x_treino, y_treino))

tempo3end = time.perf_counter()

# Random Forest Classifier #
tempo4begin = time.perf_counter()

modelo4 = RandomForestClassifier()
print("\n", modelo4.fit(x_treino, y_treino))

tempo4end = time.perf_counter()

# Perceptron #
tempo5begin = time.perf_counter()

modelo5 = StandardScaler()
print("\n", modelo5.fit(x_treino))
x_treino_scaled = modelo5.transform(x_treino.values)
ppn = Perceptron(max_iter=1000, eta0=0.1, random_state=0)
print("\n", ppn.fit(x_treino, y_treino.values.ravel()))

tempo5end = time.perf_counter()


# In[4]:


# AV1 MultiLayer #
tempo6begin = time.perf_counter()

modelo6 = MLPClassifier(random_state=1, max_iter=300)
print("\n", modelo6.fit(x_treino, y_treino))

tempo6end = time.perf_counter()

cols = list(x_treino)
nodes=[]

split_only_thresh = [1.40402595879,
                     4.72845183649,
                     1.86517797783,
                     1.58715223005,
                     7.22695596987]

no_split_thresh = [-100.000000,
                   -4.100921,
                   -4.564202,
                   -5.695176,
                   -1.483546]

n=0
for row_sc, row in zip(x_treino_scaled, x_treino.values):
    
    if n<5:
        n=+1
        
    nodes =  row_sc

    bsize = row[-1]
    
    if bsize == 15:
        bsize_idx = 0
    elif bsize == 12:
        bsize_idx = 1
    elif bsize == 9:
        bsize_idx = 2
    elif bsize == 6:
        bsize_idx = 3
    elif bsize == 3:
        bsize_idx = 4
        
    score = ml_av1.av1_nn_predict_c(nodes,n,glob)
    print(score)
    nodes = []
    
    if (score > split_only_thresh[bsize_idx]):
        partition_none_allowed = 0;
        partition_horz_allowed = 0;
        partition_vert_allowed = 0;
        do_rectangular_split = 0;
        
    simple_motion_search_split = 2
    if ((simple_motion_search_split >= 2) and (score < no_split_thresh[bsize_idx])):
        do_square_split = 0;
    


# In[6]:


# RESULTADOS #

resultado1 = modelo1.score(x_teste, y_teste)
resultado2 = modelo2.score(x_teste, y_teste)
resultado3 = modelo3.score(x_teste, y_teste)
resultado4 = modelo4.score(x_teste, y_teste)

resultado5 = ppn.score(x_teste, y_teste)

resultado6 = ppn.score(x_teste, y_teste)

tempo1 = tempo1end - tempo1begin
tempo2 = tempo2end - tempo2begin
tempo3 = tempo3end - tempo3begin
tempo4 = tempo4end - tempo4begin

tempo5 = tempo5end - tempo5begin

tempo6 = tempo6end - tempo6begin

print("\nAcurácia Extra Trees Classifier: %.3f Tempo: %.2fs"%(resultado1*100, tempo1))
print("\nAcurácia Decision Trees Classifier: %.3f Tempo: %.2fs"%(resultado2*100, tempo2))
print("\nAcurácia Regressão Logistica: %.3f Tempo: %.2fs"%(resultado3*100, tempo3))
print("\nAcurácia Floresta Aleatória: %.3f Tempo: %.2fs"%(resultado4*100, tempo4))

print("\nPerceptron: %.3f Tempo: %.2fs"%(resultado5*100, tempo5))

print("\nAV1 MultiLayer: %.3f Tempo: %.2fs"%(resultado6*100, tempo6))


# In[ ]:




