from rdflib import Graph,URIRef
from sklearn.metrics import average_precision_score
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
def train_file():
    g=Graph()
    g.parse("SWC_2019_Train.nt",format="turtle")
    tab=[]

    for index,(sub,pred,obj) in enumerate(g):
        tab.append((sub,pred,obj))
    tab=sorted(tab, key=lambda x: x[0])
    statements={}
    for (sub,pred,obj) in tab:
        if pred==(URIRef("http://swc2017.aksw.org/hasTruthValue")):
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
    g.parse("SWC_2019_Test.nt", format="turtle")
    tab = []
    for index, (sub, pred, obj) in enumerate(g):
        tab.append((sub, pred, obj))
    tab = sorted(tab, key=lambda x: x[0])
    statements = {}
    for (sub, pred, obj) in tab:
        if obj == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement")):
            statements[sub] = {}

    for (s, p, o) in tab:
        if p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")):
            statements[s]["subject"] = o
        elif p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")):
            statements[s]["predicate"] = o
        elif p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")):
            statements[s]["object"] = o
    listp = []
    listk=[]
    for k, v in statements.items():
        listk.append(k)
        listp.append(v)
    df = pd.DataFrame(listp)
    df.to_csv('test.csv')
    df2=pd.DataFrame(listk)
    df2.to_csv('facts.csv')

train_file()
test_file()

df_train=pd.read_csv("train.csv")
df_test=pd.read_csv("test.csv")

df_train_1=df_train.drop('score',axis=1)
df_test_1=df_test.rename(columns={"subject": "sub", "predicate": "pred","object":"obj"})
result = pd.concat([df_train_1, df_test_1], axis=1, join='inner')
result=result.drop('Unnamed: 0',axis=1)
result.to_csv("result.csv")
le = LabelEncoder()
le.fit(np.unique(result.astype(str)))
X = np.array([le.transform(samp.astype(str)) for samp in result.values])
df1=pd.DataFrame(X,columns=["predicate","subject","object","sub","pred","obj"])
df1.to_csv("result.csv")
df_fin=pd.read_csv("result.csv")
df1 = df_fin[['predicate', 'subject','object']]
df2 = df_fin[['sub', 'pred','obj']]

df_pom1=df2['sub']
df_pom2=df2['pred']
df_pom3=df2['obj']
df_pom4=pd.concat([df_pom2, df_pom1], axis=1, join='inner')
df2=pd.concat([df_pom4, df_pom3], axis=1, join='inner')

df3=pd.concat([df1, df_train["score"]], axis=1, join='inner')
df4=df2.rename(columns={"pred": "predicate","sub": "subject","obj":"object"})
df4.to_csv("test_en.csv")
df3.to_csv("train_en.csv")

X_train=df1
X_test=df4
Y_train=df3['score']

# clf =RandomForestClassifier(random_state=0)
# clf.fit(X_train,Y_train)
# pred=clf.predict(X_test)
# res=pd.DataFrame(pred)
#
# print(classification_report(Y_train,pred))

# clf2=svm.SVC()
# clf2.fit(X_train,Y_train)
# pred2=clf2.predict(X_test)
# print(pred2)
# print(classification_report(Y_train,pred2))
tab=[]
precision=[]
for i in range(100):
    mlpc=MLPClassifier(hidden_layer_sizes=(11,11,11),max_iter=500)
    mlpc.fit(X_train,Y_train)
    pred_mlpc=mlpc.predict(X_test)
    tab.append(pred_mlpc)
    print(pred_mlpc)
    precision.append(average_precision_score(Y_train,pred_mlpc))

df_pom_10=pd.DataFrame(tab)
df_pom_11=pd.read_csv("facts.csv")
pom=df_pom_10.mean()
print(pom)
df_pom_12=pd.concat([df_pom_11, pom], axis=1, join='inner')
df_pom_12=df_pom_12.drop('Unnamed: 0',axis=1)
df_pom_12 = df_pom_12.set_axis([ 'statement', 'predicted_score'], axis=1, inplace=False)
df_pom_12.to_csv("final_res.csv")
print("Precision",sum(precision) / len(precision))
