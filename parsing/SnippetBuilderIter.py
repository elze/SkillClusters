import re
import logging
import pprint

from SnippetBuilder import SnippetBuilder

class SnippetBuilderIter(SnippetBuilder):

    def buildJobSnippet(self):
	s = '|'
	allKeywords = self.synonyms + self.secondarySynonyms
	primarySecondaryAlternatives = s.join(map(re.escape, allKeywords))

	keywordMatches = re.finditer(r'((?:^|\W)(?P<keyw>' + primarySecondaryAlternatives + r')(?=\W|$))+', self.jobDescription, flags=re.IGNORECASE)
	namedGroupMatches = map(lambda x: (x.start('keyw'), x.end('keyw'), x.group('keyw')), keywordMatches)

	# The greatest total number of text snippets (including the keywords) can be
	textSnippetsCount = len(namedGroupMatches) + 1
	# We want the relevant text snippets from the job description that are displayed to the user
	# at the first glance to be not much more than 250 characters
	TargetJobSnippetLength = 250
	MinApproxSnippetLength = 30
	approxSnippetLength = 0
	if textSnippetsCount > 0:
	    approxSnippetLength = TargetJobSnippetLength / textSnippetsCount
	else:
	    logging.debug("!!!!!!! approxSnippetLengh = 0; textSnippetsCount = " + str(textSnippetsCount))
	if (approxSnippetLength < MinApproxSnippetLength):
	    approxSnippetLength = MinApproxSnippetLength

	snippets = []

	for i in range(len(namedGroupMatches)):
	    namedGroupMatch = namedGroupMatches[i]
	    if i == 0:
		if namedGroupMatch[0] > 0:
		    keywordStartIndex = namedGroupMatch[0]
		    # namedGroupMatch[0] is the index at which this keyword begins in the text
		    # then this keyword is not at the beginning of the job description
		    # but is preceded but some text; we want to extract some of that text right before the keyword
		    segment = self.jobDescription[0: keywordStartIndex]
		    if keywordStartIndex > approxSnippetLength:
			# the text that precedes the first keyword is longer than it should be; let's extract the end of it
			indexFromTheRight = -1 - approxSnippetLength
			segm = segment[indexFromTheRight:]
			snippets.append(segm)
		    else:
			snippets.append(segment)
		# In any case we also need to append the actual keyword
		snippets.append("<b>" + namedGroupMatch[2] + "</b>") # append the actual keyword
	    else:
		# This keyword is somewhere on the middle of the job description
		endPreviousKeyword = namedGroupMatches[i-1][1]
		startThisKeyword = namedGroupMatches[i][0]
		if startThisKeyword - endPreviousKeyword > approxSnippetLength + 5:
		    halfSnippetLength = approxSnippetLength / 2
		    segmLeft = self.jobDescription[endPreviousKeyword: endPreviousKeyword + 1 + halfSnippetLength ]
		    segmRight = self.jobDescription[startThisKeyword -1 - halfSnippetLength : startThisKeyword - 1 ]
		    segment = segmLeft + " ... " + segmRight
		else:
		    segment = self.jobDescription[endPreviousKeyword: startThisKeyword]
		snippets.append(segment)
		snippets.append("<b>" + namedGroupMatch[2]+ "</b>") # append the actual keyword
	    
		if i == len(namedGroupMatches)-1:
		    # This is the last keyword in the job description, so we also need to extract the text to the right of it
		    endThisKeyword = namedGroupMatch[1]
		    if len(self.jobDescription) - endThisKeyword > approxSnippetLength:
			segment = self.jobDescription[endThisKeyword : endThisKeyword + approxSnippetLength]
		    else:
			segment = self.jobDescription[endThisKeyword: ]
		    snippets.append(segment)
	    
	job_ad_snippet = ''.join(snippets)
        return job_ad_snippet
