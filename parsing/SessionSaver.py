import logging

from sccommon.SkillPair import SkillPair
from sccommon.SkillPostCounter import SkillPostCounter
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from sccommon.JobPostingToSkillPairWrapper import JobPostingToSkillPairWrapper

class SessionSaver(object):

    def __init__(self, session):
	self.session = session

    def saveSkillPostCounters(self, skillsPostCountsDict):
	for skillKeyword in skillsPostCountsDict:
	    skillPostCounter = SkillPostCounter()
	    skillPostCounter.skill_term = skillKeyword
	    skillPostCounter.number_of_postings = skillsPostCountsDict[skillKeyword]
	    self.session.add(skillPostCounter) 

    def saveSkillPairs(self, skillsDictionary):
	for skillKeyword in skillsDictionary:
	    secondarySkillHash = skillsDictionary[skillKeyword]
	    for secondarySkillKeyword in secondarySkillHash:
		skillpair = secondarySkillHash[secondarySkillKeyword]
	        self.session.add(skillpair) # UNCOMMENT THIS
                #logging.debug(pprint.pformat(skillpair.__dict__))
	        # REMOVE: The line below is only for printing
	        #ratio = skillpair.number_of_times / skillsPostCountsDict[skillKeyword]
	        #logging.debug("P: " + skillpair.primary_term + " ; S: " + skillpair.secondary_term + "; ratio: " + pprint.pformat(ratio))
        self.session.commit()

    def assignSkillPairIDsToJobPostings(self, jobPostingsToSkillsPairs):
	for jobPostingToSkillPairW in jobPostingsToSkillsPairs:
	    jobPostingToSkillPair = jobPostingToSkillPairW.jobPostingToSkillPair
	    jobPostingToSkillPair.skill_pair_id = jobPostingToSkillPairW.skillPair.id

        self.session.expunge_all()

    def saveJobPostingsToSkillsPairs(self, jobPostingsToSkillsPairs):
	for jobPostingToSkillPairW in jobPostingsToSkillsPairs:
	    jobPostingToSkillPair = jobPostingToSkillPairW.jobPostingToSkillPair
	    self.session.add(jobPostingToSkillPair)
            #logging.debug("jobPostingToSkillPair.skill_pair_id = " + str(jobPostingToSkillPair.skill_pair_id) + " primary_term = " + jobPostingToSkillPairW.skillPair.primary_term + " secondary_term = " + jobPostingToSkillPairW.skillPair.secondary_term) 
        self.session.commit()

    def saveJobListings(self, jobListings):
	for jobListing in jobListings:
	    self.session.add(jobListing) 
	self.session.commit()

    def saveJobHypCompanyMappings(self, jobHypCompanyMappings):
	for jobHypCompanyMapping in jobHypCompanyMappings:
	    self.session.add(jobHypCompanyMapping) 
	self.session.commit()

    def saveJobLocations(self, jobLocations):
	for jobLocation in jobLocations:
	    self.session.add(jobLocation) 
	self.session.commit()
