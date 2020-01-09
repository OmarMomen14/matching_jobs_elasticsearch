# This code is just testing a query to match a candidate to a job posting
# It is better to test the function with real data in a large index in elasticesearch
# To test it on external index
	#1 change the host name and the port below
	#2 modify the job posting attributes in the query below
	#3 modify the index name based on the real data index in your server
	#4 Also you can change the candidate information to test the query

import json
from elasticsearch import Elasticsearch
import os
from datetime import date 
import math

host_name = 'localhost'
port = '9200'

es = Elasticsearch([{'host': host_name,'port':port}])



# Indexing data from json files in this directory to jobs_test index
jobs_data_files = []

files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
	if('.json' in f):
		jobs_data_files.append(f)

for f in jobs_data_files:
	with open(f) as infile:
		data = json.load(infile)
		es.index(index="jobs_test", body=data)





# The candidate's profile to match the jobs for, feel free to modify values
candidate = { 	"qualification_level": "Bachelor",
				"major": "Computer Science",
				"skills": "programming, java, python, databases",
				"work_experience": [
					{	"start_month":3,
						"start_year":2017,
						"end_month":7,
						"end_year":2018,
						"title":"Software Developer",
						"responsibilities":"Develope backend systems.\nDesign UI pages. \nManage database applications",
						"salary":3000
					},
					{	"start_month":7,
						"start_year":2018,
						"end_month":5,
						"end_year":2019,
						"title":"Senior Software Engineer",
						"responsibilities":"Develops software solutions by studying information needs; conferring with users. \nStudying systems flow, data usage, and work processes.\nInvestigating problem areas; following the software development lifecycle",
						"salary":5000,
					},
				]
			}



# Preparing the candidate information for matching query
qualification_major = candidate["qualification_level"] + " " + candidate["major"]
experience_years = 0
for w in candidate["work_experience"]:
	start_date = date(w["start_year"], w["start_month"],1)
	end_date = date(w["end_year"], w["end_month"],1)
	experience_years = experience_years + math.ceil((end_date - start_date).days / 365)

skills = candidate['skills']
average_salary = 0
i=0
for w in candidate["work_experience"]:
	average_salary = average_salary + w['salary']
	i = i + 1

if (i == 0):
	average_salary = 0
else:
	average_salary = average_salary / i



# The matching query, please change the job posting attributes names to test on personal index
query = { "query": {
			"bool": {
				"must":
					{
						"match": {
							"qualification_level": {
								"query" : qualification_major,
								"analyzer":"standard"
							}
						}
					},
				"should": [
					{
						"range" : { "years_of_experience" : { "lte" : experience_years } }
					},
					{
						"match": {
							"job_requirements": {
								"query" : skills,
								"analyzer":"standard"
							}
						}
					},
					{
						"range" : { "salary" : { "gte" : average_salary } }	
					}
				]
				}
			}
        }


# Sending the query to elasticesearch
index_name = 'jobs_test'
result = es.search(index=index_name, body=query)

#Printing the results json file
print(result)
