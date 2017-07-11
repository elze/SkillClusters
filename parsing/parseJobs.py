import sqlalchemy
from os import listdir
import logging
import string

import ConfigParser

dbconfig = ConfigParser.RawConfigParser()
dbconfig.read('db_postgres_settings_my.cfg')
#dbconfig.read('db_mysql_python_anywhere_settings.cfg')

sqlalchemy_database_uri = dbconfig.get('database', 'SQLALCHEMY_DATABASE_URI')

config = ConfigParser.RawConfigParser()
config.read('import_settings.cfg')

logFilePath = config.get('parsing', 'LOG_FILE_PATH')
importFilePath = config.get('parsing', 'IMPORT_FILE_PATH')
processedFilePath = config.get('parsing', 'PROCESSED_FILE_PATH')

logging.basicConfig(filename=logFilePath,level=logging.DEBUG)

import pprint

import re

from bs4 import BeautifulSoup

from sqlalchemy import create_engine

engine = create_engine(
    sqlalchemy_database_uri
)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

from sccommon.SkillPair import SkillPair
from sccommon.SkillPostCounter import SkillPostCounter
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from sccommon.JobPostingToSkillPairWrapper import JobPostingToSkillPairWrapper

from JobDescriptionProcessor import JobDescriptionProcessor
#from SkillPairProcessor import SkillPairProcessor
from TextPreparer import TextPreparer

#from SnippetBuilderSplit import SnippetBuilderSplit
from SnippetBuilderIter import SnippetBuilderIter

from SessionSaver import SessionSaver

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#import keywordsAndDictionary
import keywordsWithSynonyms

skillsDictionary = {}

skillsPostCountsDict = {}

jobPostingsToSkillsPairs = []

############## TO DO ##############
# Read all the records fom the skill_post_counters table;
# Place them in the skillsPostCountsDict dictionary: skill_term will be the name, and number_of_postings will be the value
# 
#########################

jobFileNames = []

# This assumes that under importFilePath there are many directories containing job postings,
# in other words, that the directory tree has a depth of 1. If that's not the case, the logic
# below needs to be modified.


for importFileDirectory in listdir(importFilePath):
    print importFileDirectory
    for jobFileName in listdir(importFilePath + importFileDirectory):
	jobFileNames.append(importFileDirectory + "/" + jobFileName)


for jobFileName in jobFileNames:
    jobFile = open(importFilePath + jobFileName, "r")
    jobDescription = jobFile.read()

    textPreparer = TextPreparer(jobDescription)
    jobDescription = textPreparer.getPreparedString()

    logging.debug("=====================")    
    logging.debug(jobDescription)
    logging.debug(jobFileName)

    jobDescriptionProcessor = JobDescriptionProcessor(keywordsWithSynonyms)
    jobDescriptionProcessor.processJobDescription(jobFileName, jobDescription, skillsDictionary, skillsPostCountsDict, jobPostingsToSkillsPairs)


sessionSaver = SessionSaver(session)

sessionSaver.saveSkillPostCounters(skillsPostCountsDict)

sessionSaver.saveSkillPairs(skillsDictionary)

# To jobPostingToSkillPair objects assign SkillPair ids

sessionSaver.assignSkillPairIDsToJobPostings(jobPostingsToSkillsPairs)

# Save jobPostingsToSkillsPairs

sessionSaver.saveJobPostingsToSkillsPairs(jobPostingsToSkillsPairs)


