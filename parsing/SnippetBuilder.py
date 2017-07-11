import re
import logging
from abc import ABCMeta, abstractmethod

class SnippetBuilder:
    __metaclass__ = ABCMeta

    def __init__(self, syn, secondarySyn, jobDesc):
	self.synonyms = syn
	self.secondarySynonyms = secondarySyn
	self.jobDescription = jobDesc

    @abstractmethod
    def buildJobSnippet(self): pass
