import re
import logging

from SnippetBuilder import SnippetBuilder

class SnippetBuilderSplit(SnippetBuilder):

    def buildJobSnippet(self):

	s = '|'
	primarySecondaryAlternatives = s.join(map(re.escape, self.synonyms))
	primarySecondaryAlternatives = primarySecondaryAlternatives + '|' + s.join(map(re.escape, self.secondarySynonyms))
	allKeywords = self.synonyms + self.secondarySynonyms
	maxKeywordLengh = max(map(lambda x: len(x), allKeywords))
	logging.debug("Splitting the job description into segments at the boundaries of " + primarySecondaryAlternatives)
	segments = re.split(r'(\b' +  primarySecondaryAlternatives + r'\b)+', self.jobDescription, flags=re.IGNORECASE)
	#map(lambda x: logging.debug("************" + x), segments)
	# The number of text segments between keywords could be between len(segments) / 2 - 1 to len(segments) / 2 + .1
	textSnippetsCount = len(segments) / 2
	# We want the relevant text snippets from the job description that are displayed to the user
	# at the first glance to be not much more than 250 characters
	approxSnippetLengh = 0
	if textSnippetsCount > 0:
	    approxSnippetLengh = 250 / textSnippetsCount
	else:
	    logging.debug("!!!!!!! approxSnippetLengh = 0; primarySecondaryAlternatives = " + primarySecondaryAlternatives + " textSnippetsCount = " + str(textSnippetsCount) + " approxSnippetLengh = " + str(approxSnippetLengh) + " len(segments) = " + str(len(segments)))
	    #logging.debug("We are here")
	    #logging.debug("maxKeywordLengh = " + str(maxKeywordLengh) + " textSnippetsCount = " + str(textSnippetsCount) + " approxSnippetLengh = " + str(approxSnippetLengh))
	snippets = []
	for i in range(len(segments)):
	    #logging.debug("i = " + str(i))
	    segment = segments[i]
	    if len(segment) > maxKeywordLengh:
		# this segment is not a keyword but text between keywords
		if i == 0:
		    # this is the first segment, so let's take only the text to the left of the keyword that follows it
		    if len(segment) > approxSnippetLengh:
			indexFromTheRight = -1 - approxSnippetLengh
			segm = segment[indexFromTheRight:]
			#logging.debug("indexFromTheRight = " + str(indexFromTheRight) + " Leftmost segm = " + segm)
			snippets.append(segm)
		    else:
			snippets.append(segment)
		else:
		    if i == len(segments)-1:
			# this is the last segment, so let's take only the text to the right of the keyword that precedes it
			if len(segment) > approxSnippetLengh:
			    segm = segment[:approxSnippetLengh]
			    #logging.debug("Rightmost segm = " + segm)
			    snippets.append(segm)
			else:
			    snippets.append(segment)
		    else:
			# this is a middle segment, so let's take a snippet from the text to the right of the preceding keyword, and another to the left of the keyword that follows
			if len(segment) > approxSnippetLengh:
			    halfSnippetLength = approxSnippetLengh / 2
			    segm1 = segment[:halfSnippetLength]
			    indFromTheEnd = -1 - halfSnippetLength
			    segm2 = segment[indFromTheEnd:]
			    segm = segm1 + " ... " + segm2
			    #logging.debug("Middle segm = " + segm)
			    snippets.append(segm)
			else:
			    snippets.append(segment)
	    else:
		# this segment is either a keyword or a very short text between keywords
		#snippets.append("!!!" + segment + "!!!")
		if segment in allKeywords:
		    snippets.append("<b>" + segment + "</b>")
		else:
		    snippets.append(segment)

	logging.debug("~~~~~~~~~~~ snippets produced from this job description ") 
	map(lambda x: logging.debug("~~~~~ " + x), snippets)

	job_ad_snippet = ' '.join(snippets)

        return job_ad_snippet
