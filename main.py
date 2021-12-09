from rdflib import Graph,Literal, RDF,URIRef
from rdflib.namespace import FOAF, XSD
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
def train_file():
    g=Graph()
    g.parse("SWC_2019_Train.nt",format="turtle")
    tab=[]

    for index,(sub,pred,obj) in enumerate(g):
        #print(sub,pred,obj)
        tab.append((sub,pred,obj))
    tab=sorted(tab, key=lambda x: x[0])
    statements={}
    for (sub,pred,obj) in tab:
        if pred==(URIRef("http://swc2017.aksw.org/hasTruthValue")):
            # print(sub,obj)
            statements[sub]={}
            statements[sub]["score"]=float(obj)

    for (s,p,o) in tab:
            if p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")):
                statements[s]["subject"]=o
            elif p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")):
                statements[s]["predicate"]=o
            elif p== (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")):
                statements[s]["object"]=o
    listp=[]
    for k,v in statements.items():
        listp.append(v)
    df=pd.DataFrame(listp)
    df.to_csv('train.csv')

def test_file():
    g = Graph()
    g.parse("SWC_2019_Train.nt", format="turtle")
    tab = []
    for index, (sub, pred, obj) in enumerate(g):
        # print(sub,pred,obj)
        tab.append((sub, pred, obj))
    tab = sorted(tab, key=lambda x: x[0])
    statements = {}
    for (sub, pred, obj) in tab:
        if obj == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement")):
            # print(sub,obj)
            statements[sub] = {}

    for (s, p, o) in tab:
        if p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")):
            statements[s]["subject"] = o
        elif p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")):
            statements[s]["predicate"] = o
        elif p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")):
            statements[s]["object"] = o
    listp = []
    for k, v in statements.items():
        listp.append(v)
    df = pd.DataFrame(listp)
    df.to_csv('test.csv')

# train_file()
# test_file()

df_train=pd.read_csv("train.csv")
df_test=pd.read_csv("test.csv")
le = LabelEncoder()
le.fit(np.unique(df_train.astype(str)))
X = np.array([le.transform(samp.astype(str)) for samp in df_train.values])
print(X)
df1=pd.DataFrame(X,columns=["id","score","predicate","subject","object"])
df1 = df1.iloc[: , 1:]
df1.to_csv("train1.csv")


# X_train=df_train.drop('score',axis=1)
# X_test=df_test
# Y_train=df_train['score']
#
# clf =RandomForestClassifier(random_state=0)
# clf.fit(X_train,Y_train)
# clf.predict(X_test)