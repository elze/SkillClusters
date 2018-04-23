import pprint
import random
import re
import string
import logging

#logging.basicConfig(filename='DataAnonymizerLog01.txt',level=logging.DEBUG)

# AliasGenerator file is not in Github, because it contains names of actual companies and products
from AliasGenerator import AliasGenerator

class MatchReplacer(object):
    def __init__(self, alias):
	self.alias = alias
    
    def patternTrimmed(self, matchobj):
	if matchobj:
	    stringCaptured = matchobj.group(0)
	    #print "patternTrimmed: stringCaptured at the beginning = " + stringCaptured	
	    stringToReplace = matchobj.group(1)
	    #print "patternTrimmed: stringToReplace = " + stringToReplace	
	    stringAfterReplacement = string.replace(stringCaptured, stringToReplace, self.alias)
	    #print "patternTrimmed: stringCaptured after replacement = " + stringCaptured
	    return stringAfterReplacement
	return ""

class JobMetaData(object):
    def __init__(self):    
	self.jobLocations = []

class DataAnonymizer(object):

    def __init__(self, textString, companySynonymsDictionary, companyNamesToAliases, companyDivisions, companyProductsDictionary, productSynonymsDictionary, aliasGenerator):
	self.textString = textString
	self.companyKeywords = dict(zip(map(lambda x: x.lower(), companySynonymsDictionary.companyKeywords.keys()),
					[map(lambda x: x.lower(), companyKeywordSet) for companyKeywordSet in companySynonymsDictionary.companyKeywords.values()]))

	self.companiesToProducts = dict(zip(map(lambda x: x.lower(), companyProductsDictionary.companyProducts.keys()),
					[map(lambda x: x.lower(), productSet) for productSet in companyProductsDictionary.companyProducts.values()]))


	self.productNameAlternatives = dict(zip(map(lambda x: x.lower(), productSynonymsDictionary.productKeywords.keys()),
					[map(lambda x: x.lower(), productSet) for productSet in productSynonymsDictionary.productKeywords.values()]))

	self.companyNamesToAliases = companyNamesToAliases
	self.affiliateLists = [map(lambda x: x.lower(), companyDivisionSet) for companyDivisionSet in companyDivisions.companyDivisions] 
	self.aliasGenerator = aliasGenerator

	#logging.debug("DataAnonymizer __init__ : self.companyKeywords = " + pprint.pformat(self.companyKeywords))
	#logging.debug("DataAnonymizer __init__ : self.affiliateLists = " + pprint.pformat(self.affiliateLists))

	# companyStandardNames is an array that stores names that could possibly be
	# the company's standard, actually accepted name. The reason why there can be
	# more than one is because some job ads list both the company's name and the
	# name of the recruiting agency that represents it
	# self.companyStandardNames = []

    def getCompanyNameVariations(self, companies):
	self.companyStandardName = ""
	self.hypCompanyStandardName = ""
	#self.companyNameVariations = []
	#companyStandardNames = []
	self.companyNameAffiliatesForRegexDict = {}
	#self.companyNameRecruiterVsRealRegexDict = {}
	self.hypCompanyNameAffiliatesForRegexDict = {}
	self.productsNamesForRegexDict = {}
	self.hypProductsNamesForRegexDict = {}

	for companyElem in companies:
	    tag, companyName = self.getTagAndCompanyName(companyElem)
	    if (tag == "P"):
		self.companyStandardName, self.companyAlias, self.companyNameAlternativesForRegex, self.companyNamesToAliases, self.companyNameAffiliatesForRegexDict, self.productsNamesForRegexDict = \
		    self.processPrimaryCompany(companyName, self.companyNamesToAliases)
		
	    if (tag == "H"):
		# A company tagged with "H" is a hypothetical client of the company tagged with P, if P is a recruitment company.
		# That is to say that the job ad leads to believe that the client of the P company is the one tagged with H.
		# In some ads it is stated what the recruitment company's client is; in that case it's not hypothetical but real,
		# but we still tag it with "H".

		self.hypCompanyStandardName, self.hypCompanyAlias, self.hypCompanyNamesForRegex, self.companyNamesToAliases, self.hypCompanyNameAffiliatesForRegexDict, self.hypProductsNamesForRegexDict = \
		    self.processPrimaryCompany(companyName, self.companyNamesToAliases)
		    #self.processHypCompany(companyName, self.companyNamesToAliases)
		#print("main, after calling processHypCompany: self.productsNamesForRegexDict = " + pprint.pformat(productsNamesForRegexDict))

	z = self.productsNamesForRegexDict.update(self.hypProductsNamesForRegexDict)
	#print("main, after processing both companies: self.productsNamesForRegexDict = " + pprint.pformat(self.productsNamesForRegexDict))	
	return self.companyStandardName, self.hypCompanyStandardName
		    
    def getTagAndCompanyName(self, companyElem):
	    
	companyElem = companyElem.strip()
	companyElem = companyElem.strip("{}")
	companyElem = companyElem.strip()
	tag, companyName = companyElem.split(":")
	companyName = companyName.strip().lower()
	return tag, companyName

    def getCompanyStandardName(self, companyName, companyKeywords):
	companyStandardName = ""
	if companyName in companyKeywords.keys():
	    companyStandardName = companyName
	    #self.companyNameVariations = self.companyKeywords[self.companyStandardName]
	else:
	    for compStandardName in companyKeywords.keys():
		compNameSet = companyKeywords[compStandardName]
		if companyName in compNameSet:
		    # This is "our" company, and its standard name is compStandardName
		    companyStandardName = compStandardName
		    #self.companyNameVariations = self.companyKeywords[compStandardName]
		    
		    #print "getCompanyNameVariations: self.companyStandardNames = " + pprint.pformat(self.companyStandardNames)
		    # print "getCompanyNameVariations: self.companyNameVariations = " + pprint.pformat(self.companyNameVariations)
	if not companyStandardName:
	    companyStandardName = companyName
	return companyStandardName

    def getCompanyNameAffiliatesForRegexDict(self, companyStandardName, companyNamesToAliases, productsNamesForRegexDict):
	companyNameAffiliatesForRegexDict = {}
	# Now let's see if this company has affiliates -- parent, child, or sibling companies -- and find their name variation lists too
	#print "getCompanyNameAffiliatesForRegexDict, very beginning: companyNameAffiliatesForRegexDict as passed to it is " + pprint.pformat(companyNameAffiliatesForRegexDict)
	#productsNamesForRegexDict = {}
	for affiliateList in self.affiliateLists:
	    #print "getCompanyNameAffiliatesForRegexDict: affiliateList = " + pprint.pformat(affiliateList)
	    #print "getCompanyNameAffiliatesForRegexDict: companyStandardName = " + companyStandardName
	    if companyStandardName in affiliateList:
		#affiliateList.remove(self.companyStandardName)
		#print "getCompanyNameAffiliatesForRegexDict: companyKeywords.keys() = " + pprint.pformat(sorted(companyKeywords.keys()))
		for affiliate in affiliateList:
		    #print "getCompanyNameAffiliatesForRegexDict: affiliate in " + companyStandardName + "  affiliateList " + affiliate
		    if affiliate in companyNamesToAliases.keys():
			affiliateCompanyAlias = companyNamesToAliases[affiliate]
		    else:
			#affiliateCompanyAlias = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
			affiliateCompanyAlias = self.aliasGenerator.generateAlias(affiliate)
			companyNamesToAliases[affiliate] = affiliateCompanyAlias
		    if affiliate in self.companyKeywords.keys():
			compNameSet = self.companyKeywords[affiliate]
			companyNameAffiliatesForRegexDict[affiliateCompanyAlias] = self.getCompanyNameVariationsForRegex(compNameSet)
		    else:
			#print "getCompanyNameAffiliatesForRegexDict: calling self.getCompanyNameVariationsForRegex for affiliate " + affiliate
			companyNameAffiliatesForRegexDict[affiliateCompanyAlias] = self.getCompanyNameVariationsForRegex([affiliate])
			#print "getCompanyNameAffiliatesForRegexDict: after the call, companyNameAffiliatesForRegexDict[" + affiliateCompanyAlias + "] = " + pprint.pformat(companyNameAffiliatesForRegexDict[affiliateCompanyAlias])
		    self.addToProductsNamesForRegexDict(affiliate, companyNamesToAliases, productsNamesForRegexDict)
			    
	return companyNamesToAliases, companyNameAffiliatesForRegexDict, productsNamesForRegexDict

    def addToProductsNamesForRegexDict(self, companyName, companyNamesToAliases, productsNamesForRegexDict):
	if companyName in self.companiesToProducts.keys():
	    # prodNameSet is a set of products that the affiliate company has. Those are the standard names of the products. Each of those products may have alternative spelling.
	    prodNameSet = self.companiesToProducts[companyName]
	    for productStandardName in prodNameSet:
		productAlias = ""
		if productStandardName in companyNamesToAliases.keys():
		    productAlias = companyNamesToAliases[productStandardName]
		else:
		    productAlias = self.aliasGenerator.generateAlias(productStandardName)
		    companyNamesToAliases[productStandardName] = productAlias

		if productStandardName in self.productNameAlternatives.keys():
		    # This product has different spellings; we need to prepare regexes for all of them
		    productsNamesForRegexDict[productAlias] = self.getCompanyNameVariationsForRegex(self.productNameAlternatives[productStandardName])
		else:
		    productsNamesForRegexDict[productAlias] = self.getCompanyNameVariationsForRegex([productStandardName])

	return companyNamesToAliases, productsNamesForRegexDict


    def processPrimaryCompany(self, companyName, companyNamesToAliases):
	productsNamesForRegexDict = {}
	companyStandardName = self.getCompanyStandardName(companyName, self.companyKeywords)
	if companyStandardName in companyNamesToAliases.keys():
	    companyAlias = companyNamesToAliases[companyStandardName]
	else:
	    # self.companyAlias = ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])
	    companyAlias = self.aliasGenerator.generateAlias(companyStandardName)
	    companyNamesToAliases[companyStandardName] = companyAlias
	if companyStandardName in self.companyKeywords.keys():
	    #for variation in self.companyKeywords[self.companyStandardName]:
	    #self.companyNamesToAliases[variation] = self.companyAlias
	    companyNameAlternativesForRegex = self.getCompanyNameVariationsForRegex(self.companyKeywords[companyStandardName])
	else:
	    companyNameAlternativesForRegex = self.getCompanyNameVariationsForRegex([companyStandardName])

	self.addToProductsNamesForRegexDict(companyStandardName, companyNamesToAliases, productsNamesForRegexDict)

	#logging.debug("DataAnonymizer getCompanyNameVariations : self.companyStandardName = " + self.companyStandardName + " self.companyNamesToAliases = " + pprint.pformat(self.companyNamesToAliases))

	t = 12345, 54321, 'hello!'
	x, y, z	= t

	#companyNameAffiliatesForRegexDict = {}
	
	# Now let's see if this company has affiliates -- parent, child, or sibling companies -- and find their name variation lists too
	#meow1, meow2, meow3, meow4, meow5 =		
	companyNamesToAliases, companyNameAffiliatesForRegexDict, productsNamesForRegexDict = \
	    self.getCompanyNameAffiliatesForRegexDict(companyStandardName, companyNamesToAliases, productsNamesForRegexDict)


	#print "Returning from the call to getCompanyNameAffiliatesForRegexDict, self.companyNameAffiliatesForRegexDict = " + pprint.pformat(self.companyNameAffiliatesForRegexDict)

	return companyStandardName, companyAlias, companyNameAlternativesForRegex, companyNamesToAliases, companyNameAffiliatesForRegexDict, productsNamesForRegexDict


    def getCompanyNameVariationsForRegex(self, companyNameVariations):
	# Also need to split every variation at dots. Because otherwise we won't be able to replace the cases where in the job URL you have buildasign-com- , sailteam-io- or talentlegends-com (for company names Amazing.com Auction.com, BuildASign.com, FramesDirect.com, Sailtem.io, and TalentLegends.com)
	
	companySynonymsWithDashes = map('-'.join, map(lambda s: re.split(' |\.', s, flags=re.IGNORECASE), companyNameVariations))
	companySynonymsWithUnderscores = map('_'.join, map(lambda s: re.split(' |\.', s, flags=re.IGNORECASE), companyNameVariations))	
	companySynonymsNoSpaces = map(''.join, map(lambda s: re.split(' |\.', s, flags=re.IGNORECASE), companyNameVariations))
	
	s = '|'
	allKeywords = companyNameVariations + filter(lambda x: x not in companyNameVariations, companySynonymsWithDashes) + filter(lambda x: x not in companyNameVariations, companySynonymsWithUnderscores) + filter(lambda x: x not in companyNameVariations, companySynonymsNoSpaces)

	#reg = r'(?:^|\W)(' + re.escape(alternative) + r')(?=\W|$)'

	allEscapedNameRegexes = map(lambda v: r'(?:^|\W)(' + re.escape(v) + r')(?=\W|$)', allKeywords)

	companySynonymsMatchExtraWhitespace = []
	componentsArray = map(lambda s: s.split(" "), companyNameVariations)
	for namePartsList in componentsArray:
	    companySynonymsMatchExtraWhitespace.append(r'(?:^|\W)(' + '\s+'.join(map(re.escape, namePartsList)) + r')(?=\W|$)')
	    #companySynonymsMatchExtraWhitespace.append(map(lambda v: r'(?:^|\W)(' + '\s+'.join(map(re.escape, namePartsList)) + r')(?=\W|$)'))

	allEscapedNameRegexes = allEscapedNameRegexes + companySynonymsMatchExtraWhitespace


	#alternatives = s.join(map(re.escape, allKeywords))
	#return alternatives
	#return allKeywords
	return allEscapedNameRegexes


    def getJobMetadata(self):
	lines = self.textString.split("\n")	
	listingTitle = lines[0]
	self.dateCreated = lines[1]

	titleCompanyLocations = listingTitle.split(" ^ ")
	#jobTitleAndCompany = listingTitle.split(" ^ ")[0]
	jobTitleAndCompany = titleCompanyLocations[0]
	self.jobLocations = titleCompanyLocations[1:]
	logging.debug("DataAnonymizer getJobMetadata: listingTitle = " + listingTitle + " titleCompanyLocations[:1] = " + pprint.pformat(titleCompanyLocations[:1]))
	jobTitlesAndCompanies = jobTitleAndCompany.split(" | ")
	self.jobTitle = jobTitlesAndCompanies.pop(0)

	#jobMetaData = JobMetaData(self.jobTitle)
	jobMetaData = JobMetaData()

	if len(jobTitlesAndCompanies) > 0:
	    #return self.getCompanyNameVariations(jobTitlesAndCompanies)
	    jobMetaData.companyName, jobMetaData.hypCompanyName = self.getCompanyNameVariations(jobTitlesAndCompanies)

	if self.jobLocations:
	#if (titleCompanyLocations[1:]):
	    #jobLocations = titleCompanyLocations[1:][0].split(" ^ ")
	    jobMetaData.jobLocations = self.jobLocations

	jobMetaData.dateCreated = lines[1]
	if hasattr(self, 'companyAlias'):
	    jobMetaData.companyAlias = self.companyAlias	    
	if hasattr(self, 'hypCompanyAlias'):
	    jobMetaData.hypCompanyAlias = self.hypCompanyAlias

	#return ""
	return jobMetaData

    def sanitize(self, jobDescription, callingMethod):
	#reg = r'((?:^|\W)(' +  self.CompanyNameAlternativesRegex + r')(?=\W|$))+'
	# reg = r'(\b(' +  self.companyNameAlternativesForRegex + r')\b)+'

	if hasattr( self, 'companyNameAlternativesForRegex'):
	    self.companyNameAlternativesForRegex = sorted(self.companyNameAlternativesForRegex, key=lambda x: len(x), reverse=True)

	    #print callingMethod + " sanitize: self.companyNameAlternativesForRegex:"
            #logging.debug(callingMethod + " sanitize: self.companyNameAlternativesForRegex:")
	    for alternative in self.companyNameAlternativesForRegex:
                #print callingMethod + " alternative = " + alternative
	        #logging.debug(callingMethod + " alternative = " + alternative)
	        ##reg = r'(\b(' + re.escape(alternative) + r')\b)+'
	        #reg = r'(?:^|\W)(' + re.escape(alternative) + r')(?=\W|$)'
		matchReplacer = MatchReplacer(self.companyAlias)
	        #jobDescription = re.sub(reg, self.companyAlias, jobDescription, flags=re.IGNORECASE)
	        #jobDescription = re.sub(reg, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
		jobDescription = re.sub(alternative, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
	        #print callingMethod + " sanitize: self.companyAlias = " + self.companyAlias
	        #logging.debug(callingMethod + " alternative = " + alternative)

	#print callingMethod + " sanitize: self.companyNameAffiliatesForRegexDict:"
	#logging.debug(callingMethod + " sanitize: self.companyNameAffiliatesForRegexDict:")
	for alias in self.companyNameAffiliatesForRegexDict.keys():	    
	    self.companyNameAffiliatesForRegexDict[alias] = sorted(self.companyNameAffiliatesForRegexDict[alias], key=lambda x: len(x), reverse=True)
	    for alternative in self.companyNameAffiliatesForRegexDict[alias]:
		#print callingMethod + " alias = " + alias + " alternative = " + alternative
		#logging.debug(callingMethod + " alias = " + alias + " alternative = " + alternative)
		#reg = r'(\b(' + re.escape(alternative) + r')\b)+'
		#jobDescription = re.sub(reg, self.companyAlias, jobDescription, flags=re.IGNORECASE)
		reg = r'(?:^|\W)(' + re.escape(alternative) + r')(?=\W|$)'
		matchReplacer = MatchReplacer(alias)
		#jobDescription = re.sub(reg, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
		jobDescription = re.sub(alternative, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
		
		#print callingMethod + " sanitize: self.companyAlias = " + self.companyAlias

	if hasattr( self, 'hypCompanyNamesForRegex'):
	    #print callingMethod + " sanitize: self.hypCompanyNamesForRegex:"
	    self.hypCompanyNamesForRegex = sorted(self.hypCompanyNamesForRegex, key=lambda x: len(x), reverse=True)
	    for alternative in self.hypCompanyNamesForRegex:
		#print callingMethod + " alternative = " + alternative
		#logging.debug(callingMethod + " alternative = " + alternative)
		#reg = r'(\b(' + re.escape(alternative) + r')\b)+'
		reg = r'(?:^|\W)(' + re.escape(alternative) + r')(?=\W|$)'
		matchReplacer = MatchReplacer(self.hypCompanyAlias)		
		#jobDescription = re.sub(reg, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
		jobDescription = re.sub(alternative, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)

	if hasattr( self, 'hypCompanyNameAffiliatesForRegexDict'):
	    #print callingMethod + " sanitize: self.hypCompanyNameAffiliatesForRegexDict:"
	    #logging.debug(callingMethod + " sanitize: self.hypCompanyNameAffiliatesForRegexDict: length of its keys = " + str(len(self.hypCompanyNameAffiliatesForRegexDict.keys())))
	    for alias in self.hypCompanyNameAffiliatesForRegexDict.keys():	    
		self.hypCompanyNameAffiliatesForRegexDict[alias] = sorted(self.hypCompanyNameAffiliatesForRegexDict[alias], key=lambda x: len(x), reverse=True)
		for alternative in self.hypCompanyNameAffiliatesForRegexDict[alias]:
		    #print callingMethod + " hypothetical company alias = " + alias + " alternative = " + alternative
		    #logging.debug(callingMethod + " hypothetical company alias = " + alias + " alternative = " + alternative)
		    #reg = r'(\b(' + re.escape(alternative) + r')\b)+'
		    reg = r'(?:^|\W)(' + re.escape(alternative) + r')(?=\W|$)'
		    matchReplacer = MatchReplacer(alias)		    
		    #jobDescription = re.sub(reg, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
		    jobDescription = re.sub(alternative, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)

		    #logging.debug("jobDescription = " + jobDescription)
		    #print "jobDescription = " + jobDescription

	if hasattr( self, 'productsNamesForRegexDict'):
	    #print callingMethod + " sanitize: self.productsNamesForRegexDict:"
	    #logging.debug(callingMethod + " sanitize: self.productsNamesForRegexDict: length of its keys = " + str(len(self.productsNamesForRegexDict.keys())))
	    for alias in self.productsNamesForRegexDict.keys():	    
		self.productsNamesForRegexDict[alias] = sorted(self.productsNamesForRegexDict[alias], key=lambda x: len(x), reverse=True)
		for alternative in self.productsNamesForRegexDict[alias]:
		    #print callingMethod + " hypothetical company alias = " + alias + " alternative = " + alternative
		    #logging.debug(callingMethod + " hypothetical company alias = " + alias + " alternative = " + alternative)
		    #reg = r'(\b(' + re.escape(alternative) + r')\b)+'
		    reg = r'(?:^|\W)(' + re.escape(alternative) + r')(?=\W|$)'
		    matchReplacer = MatchReplacer(alias)		    
		    #jobDescription = re.sub(reg, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)
		    jobDescription = re.sub(alternative, matchReplacer.patternTrimmed, jobDescription, flags=re.IGNORECASE)

		    #logging.debug("jobDescription = " + jobDescription)
		    #print "jobDescription = " + jobDescription		    

	return jobDescription
    
