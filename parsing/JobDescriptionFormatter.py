import pprint
import random
import re
import string
import logging

from TextPreparer import TextPreparer
from DataAnonymizer import DataAnonymizer

# AliasGenerator file is not in Github, because it contains names of actual companies and products

from AliasGenerator import AliasGenerator
from sccommon.JobHypCompanyMapping import JobHypCompanyMapping
from sccommon.JobListing import JobListing
from sccommon.JobLocation import JobLocation

class JobDescriptionFormatter(object):

    def sanitizeJobDescription(self, jobFileName, jobDescription, companySynonymsDictionary, companyNamesToAliases, companyDivisions, companyProducts, productSynonymsDictionary, aliasGenerator):
	dataAnonymizer = DataAnonymizer(jobDescription, companySynonymsDictionary, companyNamesToAliases, companyDivisions, companyProducts, productSynonymsDictionary, aliasGenerator)
	jobMetadata = dataAnonymizer.getJobMetadata()
	if (hasattr(jobMetadata, 'companyName') or hasattr(jobMetadata, 'hypCompanyName')):
	    jobDescriptionSanitized = dataAnonymizer.sanitize(jobDescription, "Main")
	else:
	    jobDescriptionSanitized = jobDescription
	jobDescriptionWithHeaders, jobTitle = self.insertHeaders(jobDescriptionSanitized, dataAnonymizer)
	jobMetadata.jobTitle = jobTitle
	if jobMetadata.jobLocations:
	    #jobDescriptionWithHeaders = jobDescriptionWithHeaders + '<br/>\nLocations:\n' + '<br/>\n'.join(jobMetadata.jobLocations)
	    jobDescriptionWithHeaders = jobDescriptionWithHeaders + '\nLocations:\n' + '\n'.join(jobMetadata.jobLocations)
	return jobDescriptionWithHeaders, jobMetadata

    def getJobLocations(self, jobFileName, jobMetadata):
	locationsForThisJob = []
	if jobMetadata.jobLocations:
	    for jobLoc in jobMetadata.jobLocations:
		jobLocation = JobLocation(jobFileName, jobLoc)
		locationsForThisJob.append(jobLocation)
	return locationsForThisJob

    def insertHeaders(self, jobDescription, dataAnonymizer):
	jobDescLines = jobDescription.split("\n", 1)
	#jobDescLines = jobDescription.split("\n")
	#for jobDescLine in jobDescLines:
	    #print "insertHeaders: jobDescLine = \n" + jobDescLine
	titleLine = jobDescLines.pop(0)
	titleAndTheRest = titleLine.split(" | ")
	title = titleAndTheRest[0]
	
	#print "insertHeaders: after pop jobDescLine = \n"
	#for jobDescLine in jobDescLines:
	    #print "insertHeaders: jobDescLine = \n" + jobDescLine
	
	#jobDescLines.insert(0, dataAnonymizer.jobTitle)
	jobDescLines.insert(0, title)
	if hasattr(dataAnonymizer, 'companyAlias'):
	    jobDescLines.insert(1, "The hiring company: " + dataAnonymizer.companyAlias)
	else:
	    jobDescLines.insert(1, "The hiring company: unknown ")
	if hasattr(dataAnonymizer, 'hypCompanyAlias'):
	    jobDescLines.insert(2, "The (possible) real company, if the hiring company is a recruiting agency: " + dataAnonymizer.hypCompanyAlias)
	#jobDescription = "<br/>\n".join(jobDescLines)
	jobDescription = "\n".join(jobDescLines)
	return jobDescription, title
    
