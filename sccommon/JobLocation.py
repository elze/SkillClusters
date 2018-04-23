from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import select, cast
from sqlalchemy import Column, DateTime, Integer, Float, Numeric, String, Text, Unicode

Base = declarative_base()

class JobLocation(Base):
    __tablename__ = 'sc2_job_locations'
    job_file_name = Column(String(140), primary_key=True)
    location = Column(String(140))

    def __init__(self, jobFileName, location):
	self.job_file_name = jobFileName
	self.location = location

    def __unicode__(self):
        return self.job_file_name
