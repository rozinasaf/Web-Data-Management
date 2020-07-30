countries_ie.py:

The program create an ontology of countries over Wikipedia using Xpath.

After creating the ontology you can ask some questions in natural language:

(i) Who is the president of X?

(ii) Who is the prime minister of X?

(iii) What is the population of X?

(iv) What is the area of X?

(v) What is the government of X?

(vi) What is the capital of X?

(vii) When was the president of X born?

(viii) When was the prime minister of X born?

(ix) Who is X?

For example:

Who is the president of Italy?

Sergio Mattarella

Who is the prime minister of United Kingdom?

Boris Johnson

What is the population of Democratic Republic of the Congo?

101,780,263

What is the area of Fiji?

18,274 km2

What is the government of Eswatini?

Unitary parliamentary absolute monarchy

What is the capital of Canada?

Ottawa

When was the president of South Korea born?

1953-01-24

When was the prime minister of New Zealand born?

1980-07-26

Who is Donald Trump?

President of United States

Who is Kyriakos Mitsotakis?

Prime minister of Greece

Ontology: IE on all countries that are at the table on Wikipedia page: https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)

Answering natural language questions: Parsing the question and using SPARQL queries to answer.

RUNNING THE PROGRAM:

run this command to create an ontology: python <countries_ie.py path> create

run this command to ask a question: python <countries_ie.py path> question “”

ONTOLOGY CREATION CAN TAKE A WHILE - you can use the file ontology.nt, just put it in WD and ask a question.

