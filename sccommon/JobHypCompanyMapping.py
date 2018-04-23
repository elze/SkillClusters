from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import select, cast
from sqlalchemy import Column, DateTime, Integer, Float, Numeric, String, Text, Unicode

Base = declarative_base()

class JobHypCompanyMapping(Base):
    __tablename__ = 'sc2_job_hyp_company_mappings'
    job_file_name = Column(String(140), primary_key=True)
    hyp_company = Column(String(256))

    def __init__(self, jobFileName, hypCompany):
	self.job_file_name = jobFileName
	self.hyp_company = hypCompany

    def __unicode__(self):
        return self.job_file_name
