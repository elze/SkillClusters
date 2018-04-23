from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import select, cast
from sqlalchemy import Column, Date, DateTime, Integer, Float, Numeric, String, Text, Unicode

Base = declarative_base()

class JobListing(Base):
    __tablename__ = 'sc2_job_listings'
    job_file_name = Column(String(140), primary_key=True)
    date_created = Column(Date)
    company_name = Column(String(256))
    job_title = Column(String(256))    

    def __init__(self, jobFileName, dateCreated, companyName, jobTitle):
	self.job_file_name = jobFileName
	self.date_created = dateCreated
	self.company_name = companyName
	self.job_title = jobTitle

    def __unicode__(self):
        return self.job_file_name
