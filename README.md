# Web-Data-Management

IE and web crawler

countries_ie.py:

The program create an ontology of countries over wikipedia using Xpath.

After creating the ontology you can ask some questions in natural language:

(i) Who is the president of <country>?
(ii) Who is the prime minister of <country>?
(iii) What is the population of <country>?
(iv) What is the area of <country>?
(v) What is the government of <country>?
(vi) What is the capital of <country>?
(vii) When was the president of <country> born?
(viii) When was the prime minister of <country> born?
(ix) Who is <entity>?

For example:

1. Who is the president of Italy? Sergio Mattarella
2. Who is the prime minister of United Kingdom? Boris Johnson
3. What is the population of Democratic Republic of the Congo? 101,780,263
4. What is the area of Fiji? 18,274 km2
5. What is the government of Eswatini? Unitary parliamentary absolute monarchy
6. What is the capital of Canada? Ottawa
7. When was the president of South Korea born? 1953-01-24
8. When was the prime minister of New Zealand born? 1980-07-26
9. Who is Donald Trump? President of United States
10. Who is Kyriakos Mitsotakis? Prime minister of Greece

Ontology:
IE on all countries that are at the table on wikipedia page:
https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)

Answering natural languanges questions:
Parsing the question and using SPARQL queries to answer.

RUNNING THE PROGRAM:

run this command to create an ontology:
python countries_ie.py create

run this command to ask a question:
python countries.py question “<natural language question string>”

ONTOLOGY CREATION CAN TAKE A WHILE - you can use the file ontology.nt, just put it in WD and ask a question.
