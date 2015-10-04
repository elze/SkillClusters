import sqlalchemy
from os import listdir
import logging

import ConfigParser

dbconfig = ConfigParser.RawConfigParser()
dbconfig.read('db_postgres_settings.cfg')
#dbconfig.read('db_mysql_settings.cfg')

sqlalchemy_database_uri = dbconfig.get('database', 'SQLALCHEMY_DATABASE_URI')

config = ConfigParser.RawConfigParser()
config.read('import_settings.cfg')

logFilePath = config.get('parsing', 'LOG_FILE_PATH')
importFilePath = config.get('parsing', 'IMPORT_FILE_PATH')
processedFilePath = config.get('parsing', 'PROCESSED_FILE_PATH')

#print "logFilePath = " + logFilePath

logging.basicConfig(filename=logFilePath,level=logging.DEBUG)

import pprint

import re

from sqlalchemy import create_engine

engine = create_engine(
    sqlalchemy_database_uri
)


from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String

from sccommon.SkillPair import SkillPair
from sccommon.SkillPostCounter import SkillPostCounter

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()

skillKeywords = ["AJAX", "Akka", "AMQP", "Android", "Angular", "AngularJS", "Ant", "Apache", "ApacheMQ", "Artifactory", "ASP.NET", "AWS",
				 "Backbone", "BackboneJS", "Bootstrap", "BootstrapJS", "Bottle",
				 "C++", "C#", "Cassandra", "Chef", "Clojure", "COBOL", "Cocoa", "CoffeeScript", "Cordova",
                 "CouchDB", "Couch", "CSLA", "CSS", "CSS3", "Crystal Reports",
				 "Dart", "D3", "D3JS", "Delphi", "DevOps", "Django", "Dynamo", "DynamoDB",
				 "Eclipse", "Elixir", "Elm", "Ember", "EmberJS", "Entity Framework", "Erlang", "ES6",
				 "Flash", "Flask", "Fortran", "FoxPro", "Haskell", "IIS",
				 "GIS", "Git", "Golang", "Gradle", "Gulp",
				 "Hadoop", "Handlebars", "HandlebarsJS", "HBase", "Hibernate", "Hive", "HTML", "HTML5",
				 "IntelliJ", "iOS",
				 "J2EE", "Java", "Javascript", "JBOSS", "JCE", "JDBC", "Jenkins", "JMS", "JNDI", "JPA", "JQuery", "JSON", "JUnit",
				 "Kafka", "Kinesis", "Knockout", "KnockoutJS", "Koa", "KoaJS",
				 "Labview", "LAMP", "Lua", "Linux",
				 "Magento", "Maven", "Memcached", "Mercurial", "Mongo", "MongoDB", "MSSQL", "MS SQL", "MVC", "Mustache", "MyBatis", "MySQL",
				 ".NET", "NHibernate", "Node", "NodeJS", "Nose", "NoSQL", "NUnit",
				 "Objective C", "Objective-C", "Oracle",
                 "Perl", "Phonegap", "Photoshop", "PHP", "PostGIS", "Postgres", "Python", "Puppet",
				 "RabbitMQ", "RavenDB", "Raven", "RDBMS", "React.js", "ReactJS", "RESTful", "REST", "Ruby", "Ruby on Rails", "Rust",
				 "S3", "Sass", "Scala", "Selenium", "Silverlight", "SOAP", "Sparx", "Sphinx", "Spring",
				 "SQL", "SQL Server", "SSIS", "SSRS", "Struts", "Subversion", "SVN", "Sybase", "Symfony", "Swift",
				 "Team Foundation Server", "TFS", "Telerik", "Teradata", "TransactSQL", "Transact SQL", "Transact-SQL", "TSQL", "T-SQL", "Typescript",
                 "Underscore", "UnderscoreJS", "UML", "UNIX",
				 "VB.NET", "Visio", "Visual Basic", "Visual Studio",
				 "WCF", "WebAPI", "Web API", "Web Services", "WPF", "XML", "xUnit", "Zend"]



synonymsDictionary = {'angularjs': 'angular', 'backbonejs': 'backbone', 'bootstrapjs': 'bootstrap', 'couchdb': 'couch',
                      'd3js': 'd3', 'dynamodb': 'dynamo', 'emberjs': 'ember', 'handlebarsjs': 'handlebars', 'knockoutjs': 'knockout', 'koajs': 'koa',
                      'mongodb': 'mongo', 'mssql': 'sql server', 'ms sql': 'sql server', 'nodejs': 'node', 'pbjective c': 'pbjective-c',
                      'ravendb': 'raven', 'reactjs': 'react.js', 'restful': 'rest', 'svn': 'subversion',
                      'tfs': 'team foundation server',
                      'transactsql': 't-sql', 'transact sql': 't-sql', 'transact-sql': 't-sql', 'tsql': 't-sql',
                      'underscorejs': 'underscore', 'web api': 'webapi' }

skillsDictionary = {}

skillsPostCountsDict = {}

matches = []

for jobFileName in listdir(importFilePath):
    jobFile = open(importFilePath + jobFileName, "r")
    jobDescriptionRaw = jobFile.read().lower()
    indEnNote = jobDescriptionRaw.find("<en-note>")
    jobDescription = jobDescriptionRaw[indEnNote:]
    #print importFilePath + jobFileName
    #logging.debug(jobFileName)
    #logging.debug(jobDescription)
    #logging.debug("=====================")
    for skillKeywordOrig in skillKeywords:
        skillKeywordRaw = skillKeywordOrig.lower()
        #print skillKeywordRaw + '\n'
        skillKeyword = skillKeywordRaw
        if skillKeywordRaw in synonymsDictionary:
            skillKeyword = synonymsDictionary[skillKeywordRaw]
        m1 = re.search('\W(' +  re.escape(skillKeyword) + ')\W', jobDescription)
        if m1:
            if skillKeyword in skillsDictionary:
                secondarySkillDict = skillsDictionary[skillKeyword]
                skillsPostCountsDict[skillKeyword] = skillsPostCountsDict[skillKeyword] + 1
            else:
                secondarySkillDict = {}
                skillsPostCountsDict[skillKeyword] = 1

            for secondarySkillKeywordOrig in skillKeywords:
                secondarySkillKeywordRaw = secondarySkillKeywordOrig.lower()
                secondarySkillKeyword = secondarySkillKeywordRaw
                if secondarySkillKeywordRaw in synonymsDictionary:
                    secondarySkillKeyword = synonymsDictionary[secondarySkillKeywordRaw]

                if (skillKeyword != secondarySkillKeyword):
                    m2 = re.search('\W(' + re.escape(secondarySkillKeyword) + ')\W', jobDescription)
                    if m2:
                        if secondarySkillKeyword in secondarySkillDict:
                            secondarySkillDict[secondarySkillKeyword] = secondarySkillDict[secondarySkillKeyword] + 1
                        else:
                            secondarySkillDict[secondarySkillKeyword] = 1
            skillsDictionary[skillKeyword] = secondarySkillDict

for skillKeyword in skillsPostCountsDict:
    skillPostCounter = SkillPostCounter()
    skillPostCounter.skill_term = skillKeyword
    skillPostCounter.number_of_postings = skillsPostCountsDict[skillKeyword]
    session.add(skillPostCounter)

for skillKeyword in skillsDictionary:
    secondarySkillHash = skillsDictionary[skillKeyword]
    for secondarySkillKeyword in secondarySkillHash:
        secondarySkillCount = secondarySkillHash[secondarySkillKeyword]
        skillpair = SkillPair()
        skillpair.primary_term = skillKeyword
        skillpair.secondary_term = secondarySkillKeyword
        skillpair.number_of_times = secondarySkillCount
        session.add(skillpair)
        logging.debug(pprint.pformat(skillpair.__dict__))

session.commit()



