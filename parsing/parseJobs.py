import sqlalchemy
from os import listdir
import logging


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
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from sccommon.JobPostingToSkillPairWrapper import JobPostingToSkillPairWrapper


from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

#import keywordsAndDictionary
import keywordsWithSynonyms

skillsDictionary = {}

skillsPostCountsDict = {}

jobPostingsToSkillsPairs = []

matches = []

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


#for jobFileName in listdir(importFilePath):
for jobFileName in jobFileNames:
    jobFile = open(importFilePath + jobFileName, "r")
    jobDescriptionRaw = jobFile.read().lower()
    indEnNote = jobDescriptionRaw.find("<en-note>")
    jobDescription = jobDescriptionRaw[indEnNote:]
    #print importFilePath + jobFileName
    #logging.debug(jobFileName)
    #logging.debug(jobDescription)
    #logging.debug("=====================")
    #for skillKeywordOrig in keywordsAndDictionary.skillKeywords:
    for skillKeywordObj in keywordsWithSynonyms.skillKeywords:
	skillKeywordObjKeys = skillKeywordObj.keys()
        #skillKeywordRaw = skillKeywordOrig.lower()
	skillKeywordRaw = skillKeywordObjKeys[0]
        #print skillKeywordRaw + '\n'
	#logging.debug(skillKeywordRaw)
        skillKeyword = skillKeywordRaw.lower()
	synonyms = [ skillKeyword ]
	if skillKeywordObj[skillKeywordRaw]:
	    synonyms.extend(skillKeywordObj[skillKeywordRaw])
	synonyms = map(lambda x: x.lower(), synonyms)
	
	####
        #if skillKeywordRaw in keywordsAndDictionary.synonymsDictionary:
        #    skillKeyword = keywordsAndDictionary.synonymsDictionary[skillKeywordRaw]
	#    if skillKeywordRaw == ".net":
	#	logging.debug("skillKeyword that we got from the dictionary = " + skillKeyword)

	for synonym in synonyms:
	    if synonym == ".net":
		logging.debug("synonym = " + synonym)

	    m1 = re.search('\W(' +  re.escape(synonym) + ')\W', jobDescription)
	    if m1:
		if synonym == ".net":
		    logging.debug("Found " + synonym + " in the job description")
		if skillKeyword in skillsDictionary:
		    secondarySkillDict = skillsDictionary[skillKeyword]
		    if skillKeyword == ".net":		
			logging.debug("There is already an entry for its synonym " + skillKeyword + " in skillsDictionary")
		else:
		    if skillKeyword == ".net":
			logging.debug("There is no entry for its synonym " + skillKeyword + " in skillsDictionary")
		    secondarySkillDict = {}
		############# TO DO #########################
		# For this skillKeyword, retrieve all the records from skill_pairs table
		# where this skillKeyword is the primary_term;
		# Populate secondarySkillDict with them
		####################
		
		if skillKeyword in skillsPostCountsDict:
		    skillsPostCountsDict[skillKeyword] = skillsPostCountsDict[skillKeyword] + 1
		    if skillKeyword == ".net":
			logging.debug("skillKeyword already is in skillsPostCountsDict, and its count after increment is " + str(skillsPostCountsDict[skillKeyword]))
		else:
		    skillsPostCountsDict[skillKeyword] = 1
		    if skillKeyword == ".net":
			logging.debug("skillKeyword " + skillKeyword + " was not in skillsPostCountsDict, and its count is now 1 ")

		# Now for all the skillkeywords we check if they also appear in the same job posting with "primary" keyword

		for skillKeywordSecondaryObj in keywordsWithSynonyms.skillKeywords:
		    #logging.debug("skillKeywordSecondaryObj = " + pprint.pformat(skillKeywordSecondaryObj))
		    skillKeywordSecondaryObjKeys = skillKeywordSecondaryObj.keys()
		    skillKeywordSecondary = skillKeywordSecondaryObjKeys[0]

		    if (skillKeywordRaw != skillKeywordSecondary):

			secondarySynonyms = [ skillKeywordSecondary ]
			if skillKeywordSecondaryObj[skillKeywordSecondary]:
			    secondarySynonyms.extend(skillKeywordSecondaryObj[skillKeywordSecondary])
			secondarySynonyms = map(lambda x: x.lower(), secondarySynonyms)

			for secondarySynonym in secondarySynonyms:	    
			    m2 = re.search('\W(' +  re.escape(secondarySynonym) + ')\W', jobDescription)
			    if m2:
				if skillKeyword == ".net":
				    if secondarySynonym in [ 'mssql', 'sql server', 'ms sql', 'sqlserver']:
					logging.debug("Found secondarySynonym " + secondarySynonym + " in the job description for primary keyword " + skillKeyword)
				if skillKeywordSecondary in secondarySkillDict:
				    #secondarySkillDict[skillKeywordSecondary] = secondarySkillDict[skillKeywordSecondary] + 1
				    #skillpair = secondarySkillDict[skillKeywordSecondary]
				    #skillpair.number_of_times = skillpair.number_of_times + 1
				    secondarySkillDict[skillKeywordSecondary].number_of_times = secondarySkillDict[skillKeywordSecondary].number_of_times + 1
				    
				    jobPostingToSkillPair = JobPostingToSkillPair()
				    jobPostingToSkillPair.job_file_name = jobFileName
				    jobPostingToSkillPairWrapper = JobPostingToSkillPairWrapper(jobPostingToSkillPair, secondarySkillDict[skillKeywordSecondary])
				    jobPostingsToSkillsPairs.append(jobPostingToSkillPairWrapper)
				    logging.debug("skillKeywordSecondary " + skillKeywordSecondary + " is in secondarySkillDict; skillpair.primary_term = " + secondarySkillDict[skillKeywordSecondary].primary_term + " secondary_term = " + secondarySkillDict[skillKeywordSecondary].secondary_term + "; jobFileName = " + jobFileName)
				    #logging.debug("skillKeywordSecondary " + skillKeywordSecondary + " is in secondarySkillDict; skillpair.primary_term = " + skillpair.primary_term + " secondary_term = " + skillpair.secondary_term + "; jobFileName = " + jobFileName)
				    logging.debug("jobPostingToSkillPairWrapper = " + pprint.pformat(jobPostingToSkillPairWrapper))
				    if len(jobPostingsToSkillsPairs) < 20:
					logging.debug("jobPostingsToSkillsPairs after append :")
					map(lambda x: logging.debug(x), jobPostingsToSkillsPairs)
				    
				else:
				    #secondarySkillDict[skillKeywordSecondary] = 1
				    skillpair = SkillPair()
				    skillpair.primary_term = skillKeyword
				    skillpair.secondary_term = skillKeywordSecondary
				    skillpair.number_of_times = 1
				    secondarySkillDict[skillKeywordSecondary] = skillpair

				    #logging.debug("skillKeywordSecondary " + skillKeywordSecondary + " is not in secondarySkillDict; skillpair is new; skillpair.primary_term = " + skillpair.primary_term + " secondary_term = " + skillpair.secondary_term + "; jobFileName = " + jobFileName)
				    logging.debug("skillKeywordSecondary " + skillKeywordSecondary + " is not in secondarySkillDict; skillpair.primary_term = " + secondarySkillDict[skillKeywordSecondary].primary_term + " secondary_term = " + secondarySkillDict[skillKeywordSecondary].secondary_term + "; jobFileName = " + jobFileName)				    
				    jobPostingToSkillPair = JobPostingToSkillPair()
				    jobPostingToSkillPair.job_file_name = jobFileName				
				    jobPostingToSkillPairWrapper = JobPostingToSkillPairWrapper(jobPostingToSkillPair, skillpair)
				    jobPostingsToSkillsPairs.append(jobPostingToSkillPairWrapper)					
				    logging.debug("jobPostingToSkillPairWrapper = " + pprint.pformat(jobPostingToSkillPairWrapper))
				    if len(jobPostingsToSkillsPairs) < 20:
					logging.debug("jobPostingsToSkillsPairs after append :")
					map(lambda x: logging.debug(x), jobPostingsToSkillsPairs)

				if skillKeyword == ".net":
				    if secondarySynonym in [ 'mssql', 'sql server', 'ms sql', 'sqlserver']:
					logging.debug("secondarySkillDict[skillKeywordSecondary] = " + pprint.pformat(secondarySkillDict[skillKeywordSecondary]))
				break

		# At this point we have finished checking the job description for all the other skill keywords
		# to see if they occur together with the primary keyword

		# Now we'll break the loop for synonym in synonyms , because if one synonyms was found
		# in the job description, we should not look for the rest

		skillsDictionary[skillKeyword] = secondarySkillDict
		
		break
	    
for skillKeyword in skillsPostCountsDict:
    skillPostCounter = SkillPostCounter()
    skillPostCounter.skill_term = skillKeyword
    skillPostCounter.number_of_postings = skillsPostCountsDict[skillKeyword]
    session.add(skillPostCounter) # COMMENTED OUT TO AVOID WRITING TO DATABASE

for skillKeyword in skillsDictionary:
    secondarySkillHash = skillsDictionary[skillKeyword]
    for secondarySkillKeyword in secondarySkillHash:
        skillpair = secondarySkillHash[secondarySkillKeyword]
        session.add(skillpair) # COMMENTED OUT TO AVOID WRITING TO DATABASE
        #logging.debug(pprint.pformat(skillpair.__dict__))
	# REMOVE: The line below is only for printing
	#ratio = skillpair.number_of_times / skillsPostCountsDict[skillKeyword]
	#logging.debug("P: " + skillpair.primary_term + " ; S: " + skillpair.secondary_term + "; ratio: " + pprint.pformat(ratio))

session.commit() # COMMENTED OUT TO AVOID WRITING TO DATABASE

for jobPostingToSkillPairW in jobPostingsToSkillsPairs:
    jobPostingToSkillPair = jobPostingToSkillPairW.jobPostingToSkillPair
    jobPostingToSkillPair.skill_pair_id = jobPostingToSkillPairW.skillPair.id

session.expunge_all()

#print ("jobPostingsToSkillsPairs length = " + str(len(jobPostingsToSkillsPairs)))

for jobPostingToSkillPairW in jobPostingsToSkillsPairs:
    jobPostingToSkillPair = jobPostingToSkillPairW.jobPostingToSkillPair
    session.add(jobPostingToSkillPair)
    #logging.debug("jobPostingToSkillPair.skill_pair_id = " + str(jobPostingToSkillPair.skill_pair_id) + " primary_term = " + jobPostingToSkillPairW.skillPair.primary_term + " secondary_term = " + jobPostingToSkillPairW.skillPair.secondary_term) 

session.commit()

################ TO DO #############
# Move the processed job files from the "forImport" directory to the "imported" directory
###############


#import shutil
#shutil.move('C:\\bacon.txt', 'C:\\eggs')
