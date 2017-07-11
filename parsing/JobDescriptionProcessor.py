import logging
import re

from sccommon.SkillPair import SkillPair
from sccommon.SkillPostCounter import SkillPostCounter
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from sccommon.JobPostingToSkillPairWrapper import JobPostingToSkillPairWrapper

from SkillPairProcessor import SkillPairProcessor


class JobDescriptionProcessor(object):

    def __init__(self, keywordsWithSynonyms):
	self.keywordsWithSynonyms = keywordsWithSynonyms

    def processJobDescription(self, jobFileName, jobDescription, skillsDictionary, skillsPostCountsDict, jobPostingsToSkillsPairs):
	for skillKeywordObj in self.keywordsWithSynonyms.skillKeywords:
	    skillKeywordObjKeys = skillKeywordObj.keys()
	    skillKeywordRaw = skillKeywordObjKeys[0]
	    skillKeyword = skillKeywordRaw
	    synonyms = [ skillKeyword ]
	    if skillKeywordObj[skillKeyword]:
		synonyms.extend(skillKeywordObj[skillKeyword])	

	    for synonym in synonyms:
		m1 = re.search('\W(' +  re.escape(synonym) + ')\W', jobDescription, flags=re.IGNORECASE)
		if m1:
		    if skillKeyword in skillsDictionary:
			secondarySkillDict = skillsDictionary[skillKeyword]
		    else:
			secondarySkillDict = {}
		    ############# TO DO #########################
		    # For this skillKeyword, retrieve all the records from skill_pairs table
		    # where this skillKeyword is the primary_term;
		    # Populate secondarySkillDict with them
		    ####################
		
		    if skillKeyword in skillsPostCountsDict:
			skillsPostCountsDict[skillKeyword] = skillsPostCountsDict[skillKeyword] + 1
		    else:
			skillsPostCountsDict[skillKeyword] = 1

		    # Now for all the skillkeywords we check if they also appear in the same job posting with "primary" keyword

		    skillPairProcessor = SkillPairProcessor(jobFileName, jobDescription, skillKeyword)
		    jobPostingsToSkillsPairsForThisKeyword = skillPairProcessor.createOrModifySkillPairs(self.keywordsWithSynonyms, synonyms, secondarySkillDict)
		    jobPostingsToSkillsPairs.extend(jobPostingsToSkillsPairsForThisKeyword)

		    # At this point we have finished checking the job description for all the other skill keywords
		    # to see if they occur together with the primary keyword

		    # Now we'll break the loop for synonym in synonyms , because if one synonyms was found
		    # in the job description, we should not look for the rest

		    skillsDictionary[skillKeyword] = secondarySkillDict
		
		    break	

