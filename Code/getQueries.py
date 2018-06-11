import re

#open the file the queries are being grabbed from
file = open('topics.51-100', 'r')
#file = open('topics.101-150', 'r')
#file = open('topics.151-200', 'r')

#read the file
rFile = file.read()

#filter out special characters and format document
#to simplify Regex retrieval
rFile = rFile.replace("/", " ")
rFile = rFile.replace("-", " ")
rFile = rFile.replace('.', '')
rFile = re.sub("\t", " ", rFile)
rFile = re.sub('(', '', rFile)
rFile = re.sub(')', '', rFile)
rFile = rFile.replace("Topic:  ", "Topic: ")
rFile = re.sub("[^a-zA-Z (<title>)]"," ", rFile)
rFile = re.sub(" +"," ", rFile)
rFile = re.sub("<desc>", "<desc>\n", rFile)
rFile = rFile.lstrip()

#initialise variable to contain regex string
regex = '<title> Topic (.*)<'

#initialise variable to contain TREC formating
Qformat = '<top>\n<num>{}</num><title>\n{}\n</title>\n</top>'

#get all queries and store in array
theQueries = re.findall(regex, rFile)

#switch out based on the query file
i = 51
#i = 101
#i = 151

#format previously initialised TREC format string
#to contain queries then print to python shell
##Results copied into notepad file
for query in theQueries:
    print(Qformat.format(str(i), query))
    i = i + 1

