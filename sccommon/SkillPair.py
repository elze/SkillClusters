from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import column_property
from sqlalchemy import select, cast
from sqlalchemy import Column, DateTime, Integer, Float, Numeric, String, Text, Unicode

from sccommon.SkillPostCounter import SkillPostCounter

Base = declarative_base()

class SkillPair(Base):
    __tablename__ = 'sc1_skill_pairs'
    #__tablename__ = 'skill_pairs'
    id = Column(Integer, primary_key=True)
    primary_term = Column(String(140))
    secondary_term = Column(String(140))
    number_of_times = Column(Integer)

    ratio = column_property(
        select(
            [cast(cast(number_of_times, Float) / cast(SkillPostCounter.number_of_postings, Float), Numeric(7, 3))]). \
            where(SkillPostCounter.skill_term == primary_term). \
            correlate_except(SkillPostCounter)
    )


    def __unicode__(self):
        return self.primary_term
