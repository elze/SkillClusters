import sqlalchemy
from os import listdir
import logging

import ConfigParser

dbconfig = ConfigParser.RawConfigParser()
dbconfig.read('db_postgres_settings.cfg')

sqlalchemy_database_uri = dbconfig.get('database', 'SQLALCHEMY_DATABASE_URI')

config = ConfigParser.RawConfigParser()
config.read('import_settings.cfg')

logFilePath = config.get('parsing', 'LOG_FILE_PATH')
importFilePath = config.get('parsing', 'IMPORT_FILE_PATH')
processedFilePath = config.get('parsing', 'PROCESSED_FILE_PATH')

#print "logFilePath = " + logFilePath

logging.basicConfig(filename=logFilePath,level=logging.DEBUG)

import pprint

import re

from sqlalchemy import create_engine

engine = create_engine(
    sqlalchemy_database_uri
)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

from sccommon.SkillPair import SkillPair
from sccommon.SkillPostCounter import SkillPostCounter

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

skillKeywords = ["AJAX", "AMQP", "Android", "Angular", "Ant", "ApacheMQ", "Artifactory", "ASP.NET", "Backbone", "Bootstrap",
                "C++", "C#", "Cassandra", "Chef", "Clojure", "CSS", "Crystal Reports", "Delphi", "DevOps", "Django",
				"Eclipse", "Elm", "Ember", "Entity Framework", "Flash", "Flask", "FoxPro", "Haskell", "IIS",
				"GIS", "Git", "Hadoop", "Handlebars", "Hibernate", "HTML", "HTML5", "J2EE", "Java", "Javascript",
                "JBOSS", "JCE", "JDBC", "Jenkins", "JMS", "JNDI", "JPA", "JQuery", "JSON", "JUnit", 
                "Labview", "LAMP", "Lua", "Linux", 
				"Magento", "Maven", "Memcached", "MongoDB", "MVC", "MyBatis", "MySQL", 
				".NET", "NHibernate", "Node", "Nose", "NoSQL", "NUnit",
                "Oracle", "Perl", "Photoshop", "PHP", "PostGIS", "Postgres", "Python", "Puppet",
				"RabbitMQ", "React", "REST", "Ruby", "Ruby on Rails", 
				"Scala", "Selenium", "Silverlight", "SOAP", "Sparx", "Sphinx", "Spring",
                "SQL", "SQL Server", "SSIS", "SSRS", "Struts", "Subversion", "SVN", "Symfony",
				"Team Foundation Server", "TFS", "Teradata", "UNIX",
				"VB.NET", "Visio", "Visual Basic", "Visual Studio",
                "WCF", "Web Services", "WPF", "XML", "xUnit"]



skillsDictionary = {}

skillsPostCountsDict = {}

matches = []



#for jobFileName in listdir("c:\\Users\\elze\\Documents\\MyProjects\\Python\\EvernoteRetrieval\\Notes"):
#    jobFile = open("c:\\Users\\elze\\Documents\\MyProjects\\Python\\EvernoteRetrieval\\Notes\\" + jobFileName, "r")
for jobFileName in listdir(importFilePath):
    jobFile = open(importFilePath + jobFileName, "r")
    jobDescriptionRaw = jobFile.read().lower()
    indEnNote = jobDescriptionRaw.find("<en-note>")
    jobDescription = jobDescriptionRaw[indEnNote:]
    #print importFilePath + jobFileName
    #logging.debug(jobFileName)
    #logging.debug(jobDescription)
    #logging.debug("=====================")
    for skillKeywordRaw in skillKeywords:
	skillKeyword = skillKeywordRaw.lower()
	#print skillKeyword + '\n'
	m1 = re.search('\W(' +  re.escape(skillKeyword) + ')\W', jobDescription)
	if m1:
	    if skillKeyword in skillsDictionary:
		secondarySkillDict = skillsDictionary[skillKeyword]
		skillsPostCountsDict[skillKeyword] = skillsPostCountsDict[skillKeyword] + 1
	    else:
		secondarySkillDict = {}
		skillsPostCountsDict[skillKeyword] = 1
		
	    for secondarySkillKeywordRaw in skillKeywords:
		secondarySkillKeyword = secondarySkillKeywordRaw.lower()
		if (skillKeyword != secondarySkillKeyword):
		    m2 = re.search('\W(' + re.escape(secondarySkillKeyword) + ')\W', jobDescription)
		    if m2:
			if secondarySkillKeyword in secondarySkillDict:
			    secondarySkillDict[secondarySkillKeyword] = secondarySkillDict[secondarySkillKeyword] + 1
			else:
			    secondarySkillDict[secondarySkillKeyword] = 1
	    skillsDictionary[skillKeyword] = secondarySkillDict

for skillKeyword in skillsPostCountsDict:
    skillPostCounter = SkillPostCounter()
    skillPostCounter.skill_term = skillKeyword
    skillPostCounter.number_of_postings = skillsPostCountsDict[skillKeyword]
    session.add(skillPostCounter)

for skillKeyword in skillsDictionary:
    secondarySkillHash = skillsDictionary[skillKeyword]
    for secondarySkillKeyword in secondarySkillHash:
	secondarySkillCount = secondarySkillHash[secondarySkillKeyword]
	skillpair = SkillPair()
	skillpair.primary_term = skillKeyword
	skillpair.secondary_term = secondarySkillKeyword
	skillpair.number_of_times = secondarySkillCount
	session.add(skillpair)

	#logging.debug(pprint.pformat(skillpair.__dict__))

session.commit()



