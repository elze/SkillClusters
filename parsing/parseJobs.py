def processJobAndWriteToFile(jobFileName, jobDescription, companySynonymsDictionary, companyNamesToAliases, companyDivisions, companyProducts, productSynonymsDictionary, aliasGenerator):
    jobDescriptionFormatter = JobDescriptionFormatter()
    jobDescriptionSanitized, jobMetaData = jobDescriptionFormatter.sanitizeJobDescription(jobFileName, jobDescription, companySynonymsDictionary, companyNamesToAliases, companyDivisions, companyProducts, productSynonymsDictionary, aliasGenerator)
    locationsForThisJob = jobDescriptionFormatter.getJobLocations(jobFileName, jobMetaData)
    #jobLocations.extend(locationsForThisJob)
    if len(locationsForThisJob) > 1:
	logging.debug("^^^^^^^^^^^ Job with more than one location: " + jobFileName)

    jobHypCompanyMapping = None
    if (hasattr(jobMetaData, 'companyName') or hasattr(jobMetaData, 'hypCompanyName')):
	if jobMetaData.companyName:
	    jobListing = JobListing(jobFileName, jobMetaData.dateCreated, jobMetaData.companyName, jobMetaData.jobTitle)
	else:
	    jobListing = JobListing(jobFileName, jobMetaData.dateCreated, '', jobMetaData.jobTitle)
	if jobMetaData.hypCompanyName:
	    jobHypCompanyMapping = JobHypCompanyMapping(jobFileName, jobMetaData.hypCompanyName)
    else:
	jobListing = JobListing(jobFileName, jobMetaData.dateCreated, "", jobMetaData.jobTitle)


    #jobListings.append(jobListing)

    #subdirForProcessedFiles = os.getcwd() + "/parsing/ProcessedJobPostings/" + jobFileNameToSubdir[jobFileName]
    subdirForProcessedFiles = os.getcwd() + "../SkillClustersProcessedJobPostings/" + jobFileNameToSubdir[jobFileName]
    if not os.path.exists(subdirForProcessedFiles):
	os.makedirs(subdirForProcessedFiles)
    #f = open(os.getcwd() + "/parsing/ProcessedJobPostings/" + jobFileName, 'w')
    f = open(os.getcwd() + "../SkillClustersProcessedJobPostings/" + jobFileName, 'w')
    f.write(jobDescriptionSanitized)
    f.close()
    return jobDescriptionSanitized, jobListing, locationsForThisJob, jobHypCompanyMapping


import sqlalchemy
from os import listdir
import os
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

from TextPreparer import TextPreparer
from DataAnonymizer import DataAnonymizer
# AliasGenerator file is not in Github, because it contains names of actual companies and products
from AliasGenerator import AliasGenerator
from JobDescriptionFormatter import JobDescriptionFormatter

# These four files are not in Github, because they contain names of actual companies and products

import companySynonymsDictionary
import companyDivisions
import companyProducts
import productSynonymsDictionary

import keywordsWithSynonyms



companyNamesToAliases = {}

skillsDictionary = {}

skillsPostCountsDict = {}

jobListings = []

jobLocations = []

jobHypCompanyMappings = []

jobPostingsToSkillsPairs = []

aliasGenerator = AliasGenerator()

#print "Current working directory is " + os.getcwd()

from sqlalchemy import create_engine

engine = create_engine(
    sqlalchemy_database_uri
)

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

from sccommon.SkillPair import SkillPair
from sccommon.SkillPostCounter import SkillPostCounter
from sccommon.JobListing import JobListing
from sccommon.JobLocation import JobLocation
from sccommon.JobHypCompanyMapping import JobHypCompanyMapping
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from sccommon.JobPostingToSkillPairWrapper import JobPostingToSkillPairWrapper

from JobDescriptionProcessor import JobDescriptionProcessor

from SnippetBuilderIter import SnippetBuilderIter

from SessionSaver import SessionSaver

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()


############## TO DO ##############
# Read all the records fom the skill_post_counters table;
# Place them in the skillsPostCountsDict dictionary: skill_term will be the name, and number_of_postings will be the value
# 
#########################

jobFileNames = []
jobFileNameToSubdir = {}

# This assumes that under importFilePath there are many directories containing job postings,
# in other words, that the directory tree has a depth of 1. If that's not the case, the logic
# below needs to be modified.

for importFileDirectory in listdir(importFilePath):
    print importFileDirectory
    for jobFileName in listdir(importFilePath + importFileDirectory):
	jobFileExtendedName = importFileDirectory + "/" + jobFileName
	#jobFileNames.append(importFileDirectory + "/" + jobFileName)
	jobFileNames.append(jobFileExtendedName)
	jobFileNameToSubdir[jobFileExtendedName] = importFileDirectory


for jobFileName in jobFileNames:
    jobFile = open(importFilePath + jobFileName, "r")
    jobDescription = jobFile.read()

    lines = jobDescription.split("\n")	
    listingTitle = lines[0]
    date_created = lines[1]


    indEnNote = jobDescription.find("<en-note>")
    jobDescription = jobDescription[indEnNote:]

    textPreparer = TextPreparer(jobDescription)    
    jobDescription = textPreparer.getPreparedString()

    jobDescription = '\n'.join([listingTitle, date_created, jobDescription])


    jobDescription, jobListing, locationsForThisJob, jobHypCompanyMapping = processJobAndWriteToFile(jobFileName, jobDescription, companySynonymsDictionary, companyNamesToAliases, companyDivisions, companyProducts, productSynonymsDictionary, aliasGenerator)

    jobListings.append(jobListing)
    jobLocations.extend(locationsForThisJob)
    if not (jobHypCompanyMapping is None):
	jobHypCompanyMappings.append(jobHypCompanyMapping)

    logging.debug("=====================")    
    logging.debug(jobDescription)
    logging.debug(jobFileName)

    jobDescriptionProcessor = JobDescriptionProcessor(keywordsWithSynonyms)
    jobDescriptionProcessor.processJobDescription(jobFileName, jobDescription, skillsDictionary, skillsPostCountsDict, jobPostingsToSkillsPairs)




#sessionSaver = SessionSaver(session)

#sessionSaver.saveSkillPostCounters(skillsPostCountsDict)

#sessionSaver.saveSkillPairs(skillsDictionary)

# To jobPostingToSkillPair objects assign SkillPair ids

#sessionSaver.assignSkillPairIDsToJobPostings(jobPostingsToSkillsPairs)

# Save jobPostingsToSkillsPairs

#sessionSaver.saveJobPostingsToSkillsPairs(jobPostingsToSkillsPairs)

#sessionSaver.saveJobListings(jobListings)

#sessionSaver.saveJobHypCompanyMappings(jobHypCompanyMappings)

#sessionSaver.saveJobLocations(jobLocations)

