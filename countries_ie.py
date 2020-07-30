import rdflib, sys
from rdflib import Literal, XSD
import requests
import lxml.html
import re

def get_birth_date_info(url,g,entity):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    row = doc.xpath("//table//tr//th[contains(text(), 'Date of birth') or contains(text(), 'Born')]")
    if len(row) != 0:
        if len(row[0].xpath("./../td//span[@class='bday']//text()")) != 0:
            dob = Literal(row[0].xpath("./../td//span[@class='bday']//text()")[0])
            birthDate = rdflib.URIRef('http://en.wikipedia.org/wiki/birthDate')
            date = Literal(dob, datatype=XSD.date)
            g.add((entity, birthDate, date))

def get_prime_minister_info(table,g,countryName):
    wikiPrefix = "https://en.wikipedia.org"
    row = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]")
    if len(row) != 0:
        primeName = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//a/text()")
        if len(primeName) != 0:
            primeMinisterEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/' + primeName[0].replace(" ", "_").replace("\n", "").replace("\t", "").lower())
            isPrimeMinisterOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPrimeMinisterOf')
            g.add((primeMinisterEntity, isPrimeMinisterOf, countryName))
            primeLink = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//a/@href")
            get_birth_date_info(wikiPrefix + primeLink[0],g,primeMinisterEntity)
            
        else:
            primeName = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Prime Minister') and not(contains(th//a//text(), 'Deputy'))]//td//text()")
            if primeName[0] != "Vacant":
                primeMinisterEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/' + primeName[0].replace(" ", "_").replace("\n", "").replace("\t", "").lower())
                isPrimeMinisterOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPrimeMinisterOf')
                g.add((primeMinisterEntity, isPrimeMinisterOf, countryName))

def get_president_info(table,g,countryName):
    wikiPrefix = "https://en.wikipedia.org"
    row = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]")
    if len(row) != 0:
        presidentName = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]//td//a//text()")
        if len(presidentName) != 0:
            presidentEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/' + presidentName[0].replace(" ", "_").replace("\n", "").lower())
            isPresidentOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPresidentOf')
            g.add((presidentEntity, isPresidentOf, countryName))
            presidentLink = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]//td//a/@href")[0]
            get_birth_date_info(wikiPrefix + presidentLink,g,presidentEntity)

        else:
            presidentName = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'President') and not(contains(th//a//text(), 'Deputy'))]//td//text()")
            if presidentName[0] != "Vacant":
                presidentEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/' + presidentName[0].replace(" ", "_").replace("\n", "").lower())
                isPresidentOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPresidentOf')
                g.add((presidentEntity, isPresidentOf, countryName))
    
def get_goverment_info(table,g,countryName):
    row = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Government') or contains(th//text(), 'Government')]")
    if len(row) != 0:
        govermentType = table[0].xpath("//table//tbody//tr[contains(th//a//text(), 'Government') or contains(th//text(), 'Government')]//td//a//text()")
        if len(govermentType) != 0:
            for c in govermentType:
                if c.find("[") != -1: #removing [x] elements
                    govermentType.remove(c)
            goverment = '_'.join(govermentType)
            govermentEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/'+goverment.replace(" ","_").lower())
            isGovernmentOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isGovernmentOf')
            g.add((govermentEntity, isGovernmentOf, countryName))

def get_population_info(table,g,countryName): 
    population = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Population') or contains(th//text(), 'Population')]/following-sibling::tr[1]//td//text()")
    # usually population number is the next 
    # row after a row contains text 'Population'

    for p in population:
        if p.find("km") != -1: 
            # it means that population number is in the same 
            # row that contains 'Population' because the row after is area
            population = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Population') or contains(th//text(), 'Population')]//td//text()")
            break
        else:
            break
    for p in population:
        temp = p
        if p.find('(') != -1:
            p = p[0:p.find('(')].replace(" ", "").replace(",", "").replace("(", "").replace(")", "").replace("\n", "").replace("\t", "")
        else:
            p = p.replace(" ", "").replace(",", "").replace("(", "").replace(")", "").replace("\n", "").replace("\t", "")
        if len(p) != 0 and p.isdigit():
            if temp.find('(') != -1:
                populationNumber = temp[0:temp.find('(')].replace(" ", "").replace("\n", "").replace("\t", "")
            else:
                populationNumber = temp.replace(" ", "").replace("\n", "").replace("\t", "")
            break
    populationEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/'+populationNumber)
    isPopulationOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isPopulationOf')
    g.add((populationEntity, isPopulationOf, countryName))

def get_area_info(table,g,countryName):
    # in km
    area = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Area') or contains(th//text(), 'Area')]/following-sibling::tr[1]//td//text()")
    # usually area number is the next 
    # row after a row contains text 'Area'

    c = 0
    for a in area:
        if a.find("km") != -1:
            c+=1
    if c == 0:
        area = table[0].xpath("//tbody//tr[contains(th//a//text(), 'Area') or contains(th//text(), 'Area')]//td//text()")
        # it means that area number is in the same 
        # row that contains 'Area'

    # this loop searchs for the area in km   
    for a in area:
        if a.find('km') != -1 and a.find('mi') != -1:
            if a.find('km') > a.find('mi'):
                a = a[a.find('mi')+2:a.find('km')-1].replace(" ", "").replace("km", "").replace("(", "").replace("\n", "").replace("\t", "")
            else:
                a = a[0:a.find('km')-1].replace(" ", "").replace("km", "").replace("(", "").replace("\n", "").replace("\t", "")
        else:
            if a.find('km') != -1:
                a = a[0:a.find('km')-1].replace(" ", "").replace("km", "").replace("(", "").replace("\n", "").replace("\t", "")
            else:
                a = a.replace(" ", "").replace("(", "").replace(")", "").replace("\n", "").replace("\t", "")
        if len(a) != 0 and a.replace(",","").replace(".","").replace("–","").isdigit():
            areaNumber = a
            break
    areaEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/'+areaNumber)
    isAreaOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isAreaOf')
    g.add((areaEntity, isAreaOf, countryName))

def get_capital_info(table,g,countryName):
    row = table[0].xpath("//tbody//tr[contains(th//text(), 'Capital')]")
    if len(row) != 0:
        capitalName = table[0].xpath("//tbody//tr[contains(th//text(), 'Capital')]//td//a/text()")
        if len(capitalName) != 0 and len(capitalName[0].replace('[','').replace(']',''))>1:
            capitalEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/' + capitalName[0].replace(" ", "_").replace("\n", "").lower())
            isCapitalOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isCapitalOf')
            g.add((capitalEntity, isCapitalOf, countryName))
        else:
            capitalName = table[0].xpath("//tbody//tr[contains(th//text(), 'Capital')]/td/text()")
            if len(capitalName) != 0 and capitalName[0].replace(" ", "_").replace("\n", "") != "None":
                capitalEntity = rdflib.URIRef('http://en.wikipedia.org/wiki/' + capitalName[0].replace(" ", "_").replace("\n", "").lower())
                isCapitalOf = rdflib.URIRef('http://en.wikipedia.org/wiki/isCapitalOf')
                g.add((capitalEntity, isCapitalOf, countryName))

def get_country_info(url,g):
    res = requests.get(url)
    doc = lxml.html.fromstring(res.content)
    table = doc.xpath("//table[contains(@class, 'infobox')]")
    world = rdflib.URIRef('http://en.wikipedia.org/wiki/world')
    isCountry = rdflib.URIRef('http://en.wikipedia.org/wiki/isCountry')
    countryName = rdflib.URIRef('http://en.wikipedia.org/wiki/' + doc.xpath("//h1//text()")[0].replace(" ", "_").replace("\n", "").replace("\t", "").lower())
    g.add((countryName, isCountry, world))

    get_prime_minister_info(table,g,countryName)
    get_president_info(table,g,countryName)
    get_goverment_info(table,g,countryName)
    get_population_info(table,g,countryName)
    get_area_info(table,g,countryName)
    get_capital_info(table,g,countryName) 
    
    
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

# ********SPARQL QUERIES********

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

# Parsing the question

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