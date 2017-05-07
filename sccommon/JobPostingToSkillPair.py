from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import select, cast
from sqlalchemy import Column, DateTime, Integer, Float, Numeric, String, Text, Unicode

Base = declarative_base()

class JobPostingToSkillPair(Base):
    __tablename__ = 'sc2_job_postings_to_skill_pairs'
    #id = Column(Integer, primary_key=True)
    job_file_name = Column(String(140), primary_key=True)
    skill_pair_id = Column(Integer, primary_key=True)

    def __unicode__(self):
        return self.job_file_name
