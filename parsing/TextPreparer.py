from bs4 import BeautifulSoup
import logging
import pprint
import random
import re
import string

class TextPreparer(object):

	#def __init__(self, textString, companySynonymsLists):
	def __init__(self, textString):
		self.textString = textString
	    

	def getPreparedString(self):
		#indEnNote = self.textString.find("<en-note>")
		#self.textString = self.textString[indEnNote:]
		self.textString = removeUnprintableFromWholeText(self.textString)
		soup = BeautifulSoup(self.textString, "html.parser")
		#soup = BeautifulSoup(self.textString, "html5lib")

		tagsToRemove = soup.find_all(["en-media"])
		map(lambda x: x.decompose(), tagsToRemove)

		tagsToInsertBefore = soup.find_all(["strong", "span", "em"])
		map(lambda x: x.insert_before(" "), tagsToInsertBefore)

		tagsToUnwrap = soup.find_all(["a", "span", "en-note", "body", "html", "ul", "ol", "strong", "b", "em", "i", "u"])
		map(lambda x: x.append(" "), tagsToUnwrap)
		map(lambda x: x.unwrap(), tagsToUnwrap)

		#self.intermTextString = str(soup)
		#print self.intermTextString

		delimiterTags = soup.find_all(["li"])
		map(lambda x: x.insert_before(" \n"), delimiterTags)	
		map(lambda x: x.append(";"), delimiterTags)
		map(lambda x: x.unwrap(), delimiterTags)

		#self.intermTextString = str(soup)
		#print self.intermTextString

		blockTags = soup.find_all(["blockquote", "div", "br", "dl", "dd", "dt", "p", "h1", "h2", "h3", "h4", "h5", "h6", "table", "tbody", "thead", "th", "tr", "td" ])
	
		map(lambda x: x.insert_before(" \n"), blockTags)
		map(lambda x: x.append(" \n"), blockTags)
		map(lambda x: x.unwrap(), blockTags)
	
		for x in soup.find_all():
			if len(x.text) == 0:
				x.extract()

		self.textString = str(soup)
		lines = self.textString.split("\n")

		trimmedLines = map(lambda x: x.strip(), lines)
		trimmedLines = filter(lambda x: len(x) > 0, trimmedLines)
		self.textString = '\n'.join(trimmedLines)
		return self.textString

def removeUnprintableFromWholeText(strToTrim):
	strWithoutUnprintables = strToTrim
	if strToTrim:
		withoutUnprintables = list(map(lambda x:  ' ' if x not in string.printable else x, strToTrim))
		strWithoutUnprintables =  ''.join(withoutUnprintables)
		lines = strWithoutUnprintables.split(" ")
		trimmedLines = map(lambda x: x.strip(" "), lines)
		trimmedLines = filter(lambda x: len(x) > 0, trimmedLines)
		strResult =  ' '.join(trimmedLines)
	return strResult
