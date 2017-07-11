from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, Unicode

Base = declarative_base()

class SkillPostCounter(Base):
    __tablename__ = 'sc4_skill_post_counters'
    #__tablename__ = 'skill_post_counters'
    skill_term = Column(String(140), primary_key=True)
    number_of_postings = Column(Integer)

    def __unicode__(self):
        return self.skill_term
