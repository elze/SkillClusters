import re
import logging
import pprint
from sccommon.SkillPair import SkillPair
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from sccommon.JobPostingToSkillPairWrapper import JobPostingToSkillPairWrapper
from SnippetBuilderIter import SnippetBuilderIter

class SkillPairProcessor(object):

    def __init__(self, jobFileName, jobDescription, skillKeyword):
	self.jobFileName = jobFileName
	self.jobDescription = jobDescription
	self.skillKeyword = skillKeyword

    def processSkillPairsForSecondarySynonyms(self, synonyms, secondarySynonyms, skillKeywordSecondary, secondarySkillDict):
	jobDescription = self.jobDescription
	jobFileName = self.jobFileName
	skillKeyword = self.skillKeyword
	jobPostingsToSkillsPairsInner = []
	for secondarySynonym in secondarySynonyms:
	    m2 = re.search('\W(' +  re.escape(secondarySynonym) + ')\W', jobDescription, flags=re.IGNORECASE)
	    if m2:
		job_ad_snippet = self.getJobAdSnippet(synonyms, secondarySynonyms, jobDescription)
					
		if skillKeywordSecondary in secondarySkillDict:
		    skillpair = secondarySkillDict[skillKeywordSecondary]
		    skillpair.number_of_times = skillpair.number_of_times + 1		    
		else:
		    skillpair = SkillPair()
		    skillpair.primary_term = skillKeyword
		    skillpair.secondary_term = skillKeywordSecondary
		    skillpair.number_of_times = 1
		    secondarySkillDict[skillKeywordSecondary] = skillpair
		    
		jobPostingToSkillPair = JobPostingToSkillPair()
		jobPostingToSkillPair.job_file_name = jobFileName
		jobPostingToSkillPairWrapper = JobPostingToSkillPairWrapper(jobPostingToSkillPair, secondarySkillDict[skillKeywordSecondary])
		jobPostingsToSkillsPairsInner.append(jobPostingToSkillPairWrapper)

		    
		jobPostingToSkillPair.job_ad_snippet = job_ad_snippet

		break
	return jobPostingsToSkillsPairsInner

    def createOrModifySkillPairs(self, keywordsWithSynonyms, synonyms, secondarySkillDict):
	jobFileName = self.jobFileName
	jobDescription = self.jobDescription
	skillKeyword = self.skillKeyword

	jobPostingsToSkillsPairsForThisKeyword = []

	for skillKeywordSecondaryObj in keywordsWithSynonyms.skillKeywords:
	    skillKeywordSecondaryObjKeys = skillKeywordSecondaryObj.keys()
	    skillKeywordSecondary = skillKeywordSecondaryObjKeys[0]
	    
	    if (skillKeyword != skillKeywordSecondary):

		secondarySynonyms = [ skillKeywordSecondary ]
		if skillKeywordSecondaryObj[skillKeywordSecondary]:
		    secondarySynonyms.extend(skillKeywordSecondaryObj[skillKeywordSecondary])
		jobPostingsToSkillsPairsForThisKeyword.extend(self.processSkillPairsForSecondarySynonyms(synonyms, secondarySynonyms, skillKeywordSecondary, secondarySkillDict))

	return jobPostingsToSkillsPairsForThisKeyword

    def getJobAdSnippet(self, synonyms, secondarySynonyms, jobDescription):
	snippetBuilder = SnippetBuilderIter(synonyms, secondarySynonyms, jobDescription)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
	return job_ad_snippet
