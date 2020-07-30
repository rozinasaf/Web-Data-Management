import rdflib, sys
from rdflib import Literal, XSD
import requests
import lxml.html
import re

def get_country_info(url,g):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    wiki_prefix = "https://en.wikipedia.org"
    table = doc.xpath("//table[contains(@class, 'infobox')]")
    world = rdflib.URIRef('http://en.wikipedia.org/wiki/world')
    isCountry = rdflib.URIRef('http://en.wikipedia.org/wiki/isCountry')
    countryName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + doc.xpath("//h1//text()")[0].replace(" ", "_").replace("\n", "").replace("\t", "").lower())
    g.add((countryName, isCountry, world))

    bPrime = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]")
    if len(bPrime) != 0:
        cPrime = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//a//text()")
        if len(cPrime) != 0:
            primeMinisterName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + cPrime[0].replace(" ", "_").replace("\n", "").replace("\t", "").lower())
            isPrimeMinisterOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPrimeMinisterOf')
            g.add((primeMinisterName, isPrimeMinisterOf, countryName))
            cPrimeLink = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//a/@href")[0]

            res1 = requests.get(wiki_prefix + cPrimeLink)
            doc1 = lxml.html.fromstring(res1.content)
            cPrimeDate = doc1.xpath("//table//tr//th[contains(text(), 'Date of birth') or contains(text(), 'Born')]")
            if len(cPrimeDate) != 0:
                if len(cPrimeDate[0].xpath("./../td//span[@class='bday']//text()")) != 0:
                    dob = Literal(cPrimeDate[0].xpath("./../td//span[@class='bday']//text()")[0])
                    birthDate = rdflib.URIRef('http://en.wikipedia.org/wiki/birthDate')
                    date = Literal(dob, datatype=XSD.date)
                    g.add((primeMinisterName, birthDate, date))
        else:
            cPrime = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//text()")
            if cPrime[0] != "Vacant":
                primeMinisterName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + cPrime[0].replace(" ", "_").replace("\n", "").replace("\t", "").lower())
                isPrimeMinisterOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPrimeMinisterOf')
                g.add((primeMinisterName, isPrimeMinisterOf, countryName))


    bPres = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]")
    if len(bPres) != 0:
        cPres = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]//td//a//text()")
        if len(cPres) != 0:
            presidentName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + cPres[0].replace(" ", "_").replace("\n", "").lower())
            isPresidentOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPresidentOf')
            g.add((presidentName, isPresidentOf, countryName))
            cPresidentLink = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]//td//a/@href")[0]

            res2 = requests.get(wiki_prefix + cPresidentLink)
            doc2 = lxml.html.fromstring(res2.content)
            cPresidentDate = doc2.xpath("//table//tr//th[contains(text(), 'Date of birth') or contains(text(), 'Born')]")
            if len(cPresidentDate) != 0:
                if len(cPresidentDate[0].xpath("./../td//span[@class='bday']//text()")) != 0:
                    dob = Literal(cPresidentDate[0].xpath("./../td//span[@class='bday']//text()")[0])
                    birthDate = rdflib.URIRef('http://en.wikipedia.org/wiki/birthDate')
                    date = Literal(dob, datatype=XSD.date)
                    g.add((presidentName, birthDate, date))
        else:
            cPres = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//text()")
            if cPres[0] != "Vacant":
                presidentName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + cPres[0].replace(" ", "_").replace("\n", "").lower())
                isPresidentOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPresidentOf')
                g.add((presidentName, isPresidentOf, countryName))
    
    bGover = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Government') or contains(th//text(), 'Government')]")
    if len(bGover) != 0:
        cGover = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//a//text(), 'Government') or contains(th//text(), 'Government')]//td//a//text()")

        if len(cGover) != 0:
            for c in cGover:
                if c.find("[") != -1:
                    cGover.remove(c)
            gov = '_'.join(cGover)
            goverName = rdflib.URIRef('http://en.wikipedia.org/wiki/'+gov.replace(" ","_").lower())
            isGovernmentOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isGovernmentOf')
            g.add((goverName, isGovernmentOf, countryName))

       
    bpopul = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Population') or contains(th//text(), 'Population')]/following-sibling::tr[1]//td//text()")
    for b in bpopul:
        if b.find("km") != -1:
            bpopul = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Population') or contains(th//text(), 'Population')]//td//text()")
            break
        else:
            break
    dpopul = ""
    for b in bpopul:
        temp = b
        if b.find('(') != -1:
            b = b[0:b.find('(')].replace(" ", "").replace(",", "").replace("(", "").replace(")", "").replace("\n", "").replace("\t", "")
        else:
            b = b.replace(" ", "").replace(",", "").replace("(", "").replace(")", "").replace("\n", "").replace("\t", "")
        if len(b) != 0 and b.isdigit():
            if temp.find('(') != -1:
                dpopul = temp[0:temp.find('(')].replace(" ", "").replace("\n", "").replace("\t", "")
            else:
                dpopul = temp.replace(" ", "").replace("\n", "").replace("\t", "")
            break
    populationNum = rdflib.URIRef('http://en.wikipedia.org/wiki/'+dpopul)
    isPopulationOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPopulationOf')
    g.add((populationNum, isPopulationOf, countryName))

    barea = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Area') or contains(th//text(), 'Area')]/following-sibling::tr[1]//td//text()")
    c = 0
    for b in barea:
        if b.find("km") != -1:
            c+=1
    if c == 0:
        barea = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Area') or contains(th//text(), 'Area')]//td//text()")
        
    darea = ""
    for b in barea:
        if b.find('km') != -1 and b.find('mi') != -1:
            if b.find('km') > b.find('mi'):
                b = b[b.find('mi')+2:b.find('km')-1].replace(" ", "").replace("km", "").replace("(", "").replace("\n", "").replace("\t", "")
            else:
                b = b[0:b.find('km')-1].replace(" ", "").replace("km", "").replace("(", "").replace("\n", "").replace("\t", "")
        else:
            if b.find('km') != -1:
                b = b[0:b.find('km')-1].replace(" ", "").replace("km", "").replace("(", "").replace("\n", "").replace("\t", "")
            else:
                b = b.replace(" ", "").replace("(", "").replace(")", "").replace("\n", "").replace("\t", "")
        temp = b
        if len(b) != 0 and b.replace(",","").replace(".","").replace("–","").isdigit():
            darea = b
            break
    areaNum = rdflib.URIRef('http://en.wikipedia.org/wiki/'+darea)
    isAreaOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isAreaOf')
    g.add((areaNum, isAreaOf, countryName))

    bCapital = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//text(), 'Capital')]")
    if len(bCapital) != 0:
        cCapital = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//text(), 'Capital')]/td//a/text()")
        if len(cCapital) != 0 and len(cCapital[0].replace('[','').replace(']',''))>1:
            capitalName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + cCapital[0].replace(" ", "_").replace("\n", "").lower())
            isCapitalOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isCapitalOf')
            g.add((capitalName, isCapitalOf, countryName))
        else:
            cCapital = doc.xpath("//table[contains(@class, 'infobox')]//tbody//tr[contains(th//text(), 'Capital')]/td/text()")
            if cCapital[0].replace(" ", "_").replace("\n", "") != "None":
                capitalName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + cCapital[0].replace(" ", "_").replace("\n", "").lower())
                isCapitalOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isCapitalOf')
                g.add((capitalName, isCapitalOf, countryName))

def get_countries_info(url):
    g = rdflib.Graph()
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    wiki_prefix = "https://en.wikipedia.org"
    countries = doc.xpath("//table[contains(@class, 'sortable')]/tbody/tr/td[1]")
    for i in range(0,len(countries)):
        country = countries[i].xpath("./..//span//a//@href")
        if len(country) == 0:
            country = countries[i].xpath("./..//i[1]//a[1]//@href")
        get_country_info(wiki_prefix + country[0],g)
    g.serialize("ontology.nt", format="nt")
   
def q_1(quest):
    q = '_'.join(quest.split(" ")[5:len(quest.split(" "))])
    q1 = "select ?p where { ?p <http://en.wikipedia.org/wiki/isPresidentOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+">}"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str[str.find("wiki/")+5:len(str)].replace("_"," ").title()) 

def q_2(quest):
    q = '_'.join(quest.split(" ")[6:len(quest.split(" "))])
    q1 = "select ?p where { ?p <http://en.wikipedia.org/wiki/isPrimeMinisterOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+">}"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str[str.find("wiki/")+5:len(str)].replace("_"," ").title())

def q_3(quest):
    q = '_'.join(quest.split(" ")[5:len(quest.split(" "))])
    q1 = "select ?p where { ?p <http://en.wikipedia.org/wiki/isPopulationOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+">}"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str[str.find("wiki/")+5:len(str)].replace("_"," ").title())

def q_4(quest):
    q = '_'.join(quest.split(" ")[5:len(quest.split(" "))])
    q1 = "select ?p where { ?p <http://en.wikipedia.org/wiki/isAreaOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+">}"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str[str.find("wiki/")+5:len(str)].replace("_"," ") + " km2")

def q_5(quest):
    q = '_'.join(quest.split(" ")[5:len(quest.split(" "))])
    q1 = "select ?p where { ?p <http://en.wikipedia.org/wiki/isGovernmentOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+">}"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str[str.find("wiki/")+5:len(str)].replace("_"," ").replace("["," ").replace("]"," "))

def q_6(quest):
    q = '_'.join(quest.split(" ")[5:len(quest.split(" "))])
    q1 = "select ?p where { ?p <http://en.wikipedia.org/wiki/isCapitalOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+">}"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str[str.find("wiki/")+5:len(str)].replace("_"," ").title())

def q_7(quest):
    q = '_'.join(quest.split(" ")[5:len(quest.split(" "))-1])
    q1 = "select ?d where { ?p <http://en.wikipedia.org/wiki/birthDate> ?d . ?p <http://en.wikipedia.org/wiki/isPresidentOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+"> }"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str.replace("_"," ").title())

def q_8(quest):
    q = '_'.join(quest.split(" ")[6:len(quest.split(" "))-1])
    q1 = "select ?d where { ?p <http://en.wikipedia.org/wiki/birthDate> ?d . ?p <http://en.wikipedia.org/wiki/isPrimeMinisterOf> <http://en.wikipedia.org/wiki/"+q.replace("?","")+"> }"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if len(list(x1)) == 0:
        print("None")
    else:
        str = list(x1)[0][0]
        print(str.replace("_"," ").title())

def q_9(quest):
    q = '_'.join(quest.split(" ")[2:len(quest.split(" "))])
    q1 = "select ?c where { <http://en.wikipedia.org/wiki/"+q.replace("?","")+"> <http://en.wikipedia.org/wiki/isPresidentOf> ?c }"
    g1 = rdflib.Graph()
    g1.parse("ontology.nt", format="nt")
    x1 = g1.query(q1)
    if(len(list(x1)) != 0):
        str = list(x1)[0][0]
        print("President of " + str[str.find("wiki/")+5:len(str)].replace("_"," ").title())
    q2 = "select ?c where { <http://en.wikipedia.org/wiki/"+q.replace("?","")+"> <http://en.wikipedia.org/wiki/isPrimeMinisterOf> ?c }"
    g2 = rdflib.Graph()
    g2.parse("ontology.nt", format="nt")
    x2 = g2.query(q2)
    if(len(list(x2)) != 0):
        str = list(x2)[0][0]
        print("Prime minister of " + str[str.find("wiki/")+5:len(str)].replace("_"," ").title())

def question(q):
    quest = q.lower()
    if quest.find("who is the president of") != -1:
        q_1(quest)
    elif quest.find("who is the prime minister of") != -1:
        q_2(quest)
    elif quest.find("what is the population of") != -1:
        q_3(quest)
    elif quest.find("what is the area of") != -1:
        q_4(quest)
    elif quest.find("what is the government of") != -1:
        q_5(quest)
    elif quest.find("what is the capital of") != -1:
        q_6(quest)
    elif quest.find("when was the president of") != -1:
        q_7(quest)
    elif quest.find("when was the prime minister of") != -1:
        q_8(quest)
    elif quest.find("who is") != -1:
        q_9(quest)
    else:
        print("Wrong question")

def main():
    if len(sys.argv) < 2:
        print("not enough arguments")
        return
    if sys.argv[1] == "create":
        get_countries_info("https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)")
        print("ontology created")
        return
    elif sys.argv[1] != "question":
        print("Error: wrong arguments")
        return
    else:
        question(sys.argv[2])
    


if __name__ == '__main__':
    main()