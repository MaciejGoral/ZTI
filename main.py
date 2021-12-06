from rdflib import Graph,Literal, RDF,URIRef
from rdflib.namespace import FOAF, XSD
g=Graph()
g.parse("SWC_2019_Train.nt",format="turtle")
tab=[]

for index,(sub,pred,obj) in enumerate(g):
    #print(sub,pred,obj)
    tab.append((sub,pred,obj))
tab=sorted(tab, key=lambda x: x[0])
tabScore=[]
statements={}
for (sub,pred,obj) in tab:
    if pred==(URIRef("http://swc2017.aksw.org/hasTruthValue")):
        # print(sub,obj)
        tabScore.append((sub,float(obj)))
        statements[sub]={}

for (s,p,o) in tab:
        if p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#subject")):
            statements[s]["subject"]=o
        elif p == (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate")):
            statements[s]["predicate"]=o
        elif p== (URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#object")):
            statements[s]["object"]=o
for k,v in statements.items():
    print(k,v)
