import unittest
import json
import logging
import pprint
import sys
sys.path.append('../parsing')
sys.path.append('..')

#import keywordsWithSynonyms

from sccommon.SkillPair import SkillPair
from sccommon.JobPostingToSkillPair import JobPostingToSkillPair
from SnippetBuilderIter import SnippetBuilderIter
from SkillPairProcessor import SkillPairProcessor
from JobDescriptionProcessor import JobDescriptionProcessor

class TestStringMethods(unittest.TestCase):

    def setUp(self):
	self.keywordsWithSynonyms = {}
	self.keywordsWithSynonyms = type('KeywordsAndSynonyms', (object,), { "skillKeywords": [{"Angular" : ["AngularJS", "Angular.JS"]}, {"SQL Server": ["SQLServer", "MSSQL", "MS SQL"]}, {"Node": ["NodeJS", "Node.JS"]}, {"SSIS": ["SQL Server Integration Services"]}, {"TransactSQL": ["Transact SQL", "Transact-SQL", "TSQL", "T-SQL"]}]})
	self.jobDescriptionMultipleSynonyms1 = r""".Net Developer
US-Nationwide 12/6/2013
This is a full-time - perm position in St. Petersburg, FL (Tampa, Florida Area)
Job Responsibilities
As .NET Developer you will work on an entrepreneurial IT team to develop software and integrated solutions for large corporate and government clients in the transportation industry.
Specific duties of the .NET Developer Include:
Performing web site updates;Writing and designing web page content in ASP.NET /C#;Conferring with management to prioritize needs, resolve conflicts, develop content criteria, and choose solutions;Backing up files from web sites to local directories for instant recovery in case of problem;Identifying problems uncovered by testing or customer feedback, and correct problems or refer problems to appropriate personnel for correction;Evaluating code to ensure that it is valid, is properly structured, meets industry standards and is compatible with browsers, devices, or operating systems.;Maintaining understanding of current web technologies or programming practices;Analyzing user needs to determine technical requirements;Developing test routines and schedules to ensure that test cases mimic external interfaces and address all browser and device types ;
JOB REQUIREMENTS
Specific requirements for the .NET Developer include:
Minimum 3 years web development experience in ASP.NET/C#;Database knowledge in MSSQL Server, with Graphics and GUI capability;Required proficiency in: ASP.NET, C#, JQuery, XML, HTML,CSS, MS SQL Server, Source Control, MS Office Suite;Desired proficiency in: WPF, WCF, Silverlight, Mapping/GIS, Flash, Photoshop, Illustrator, Crystal Reports, MySQL, Web Services;Ability to pass a criminal and financial background check;Ability to work onsite at our office in the Tampa Bay area;Aggressive, entrepreneurial, team player ;Self-directed, organized, and extremely attentive to details;
JOB SNAPSHOT
Employment TypeFull-Time
Job TypeInformation Technology
EducationNot Specified
ExperienceAt least 3 year(s)
Manages OthersNot Specified
IndustryInternet - ECommerce, Computer Software
Required TravelNot Specified
Job IDBH-11830"""

	# This job description has both MS SQL and SQL Server versions
	self.jobDescriptionMultipleSynonyms2 = r"""Job Overview
Title:
Python Developer
Skills:
"Python Developer" SDLC, HTML, JavaScript, ASP.NET, C#, MSSQL, Fortran,
Date Posted:
3-6-2015
Location:
Austin, TX
Area Code:
512
Employ. Type:
CON_CORP CON_IND CON_W2
Pay Rate:
DOE
Job Length:
6 months plus
Position ID:
CK357141213
Dice ID:
10111245
Printer-FriendlyJob Description
Python Developer;Austin, TX;***** is seeking a Python Developer for a 6 month contract for our client in downtown Austin.
Job Description
Performs moderately complex (journey-level) computer programming and software development work. Work involves assisting the Team Lead in coordinating programming
projects, analyzing proposed computer applications; and providing technical assistance. Plans and analyzes user requirements, procedures and problems to automate
processing and to improve existing systems. Assists in maintaining existing and new internal and open source software. Performs moderately complex data processing,
quality assurance and management functions for water quality and other water-related time-series data. Assists in maintaining software that retrieves and inserts data into
relational databases. Assists in maintaining data related webpages and fulfills customer requests for data. Works under limited supervision, with considerable latitude for the
use of initiative and independent judgment.
Essential Job Functions
* Assist in the identification and scheduling of project deliverables, milestones and required tasks
* Generate project requirements, provide effort estimates and resource requirements
* Develop, analyze and revise system design procedures, program code, test procedures and quality standards
* Prepare detailed analysis, plans, diagrams and verification procedures for existing and proposed computer applications
* Develop diagrams and flowcharts to represent operations and data flow for applications
* Code, test and debug computer application programs as outlined by technical and functional requirements
* Use current software design and development methodologies and techniques to ensure quality and maintainability of applications and systems * Prepare test data and
assist end users with testing
* Prepare instructions for use during production runs
* Prepare and develop instructions or manuals for end users
* Research and analyze project proposals and software and system modifications
* Analyze proposed computer applications in terms of equipment requirements and capabilities
* Analyze, review and revise code to increase operating efficiency or to adapt to new procedures
* Assist in the generation or installation of systems software
* Develop and implement specialized programs to supplement and enhance systems software
* Assist in maintaining the webpage.
Assists in expanding the webpage to include new datasets.
* Perform related work as assigned
Minimum Qualifications * Graduation from an accredited college or university with major coursework in Computer Science, Information Science, Information Technology or
related field. * Relevant experience may be substituted for education on a year-for-year basis * One year of experience developing software applications using Python.
Experience may be academic, open source or work related.
Experience in the development and analysis of geospatial, engineering and/or scientific data.
Experience with the graphical display of engineering and/or scientific data.
Experience in the use of UNIX/Linux operating systems, with experience in systems administration.
Experience in the development and analysis of time-series data.
Experience with numerical and statistical methods
Experience with groundwater and/or surface water modeling. Knowledge, Skills, and Abilities
Knowledge and understanding of the Software Development Life Cycle (SDLC).
Knowledge of relational databases and data management, with experience with PostgreSQL preferred.
Knowledge of State of Texas environmental and natural resources, particularly water resources management
Knowledge of HTML, CSS, JavaScript, ASP .NET, C# and/or AJAX applications.
Knowledge of Microsoft SQL Server 2005/2008/2012.
Skill in the development of unit tested software.
Skill in the development of web applications and/or web services using Python, with experience in Flask or Django preferred
Skill in the development of scientific Python applications, with experience in NumPy, SciPy or Pandas preferred.
Skill in the development of FORTRAN applications
Skill in the deployment of software applications, with experience in Fabric or Ansible preferred.
Skill in the use of distributed version control systems, with experience in GitHub preferred.
Skill in providing excellent customer service, both internally and externally.
Skill in decision making and problem solving.
Ability to develop, analyze and design system requirements and processes.
Ability to communicate both technical and non-technical issues effectively, both verbally and in writing.
Ability to prioritize deadlines.
Ability to multi-task and manage multiple projects with limited supervision
Ability to work and collaborate with others in multi-disciplinary teams. Remarks
Copy of required academic transcripts and/or licensures must be submitted at the time of hire."""

	# This job description also has both MS SQL and SQL Server versions
	self.jobDescriptionMultipleSynonyms3 = r"""NET Software Developer (Contract)
Job Description:
This position will augment development staff on an enterprise project to upgrade Client s investment data warehouse and refactor custom data processing applications. This will be a six-month contract position with the potential for several months of follow-on work, depending on need.; Responsibilities/Duties:
Write custom software applications for storage of raw vendor data and integrate multiple data sources into a consolidated data model.;Design and build back-end databases and to store key investment data.;Build data interfaces and integrations between applications.;Build and execute unit tests for newly developed code.;Participate in software code reviews and present code solutions to Client staff.; Minimum Requirements:
At least 5+ of experience in developing applications with an emphasis in data processing and integration.;Excellent programming skills with proficiency in the following programming languages: Visual Studio .NET, C#, Transact SQL and LINQ;;Knowledge of XML, XSD, and XSLT. Experience parsing XML using standard .NET parsing libraries.;Practical knowledge with MS SQL 2012/2014 or relational database technologies; including the ability to design and maintain application data structures; Development experience with the Entity Framework or other ORM mappers;Experience working with SQL Server Integration Services (SSIS) or related ETL tools.;Experience in developing, documenting, and executing test plans;;Excellent communications (oral and written);;4 year college degree (preferred);"""

	# This job description also has both Web Services and webservices
	self.jobDescriptionMultipleSynonyms4 = r"""PHP Developer-RESTful, Soap, JavaScript
North Austin Texas area
Permanent Direct Hire
Benefits include medical, 401K and annual bonus program
This is NOT a telecommute or contract position
No H1 sponsorships available at this time.
Compensation commensurate with experience
Looking for a PHP Developer with 4+ years of experience to be part of a highly collaborative, quality focused, Agile development team. Will be writing unit tests, writing elegant, reusable and maintainable, object-oriented code utilizing frameworks and 3rd party libraries. Just placed 2 hires there and you can be next.
Opportunity to solve difficult problems and helping to build maintainable applications. You should be comfortable working in a fast-paced, highly collaborative environment with small sprint teams. Also, you should be able to find the ideal way to implement requirements in a clean, elegant and object-oriented way utilizing source control, documentation, and established coding standards. This is not a management position.
Skills This PHP Developer will need:
Bachelor's Degree OR 4+ years of programming experience;PHP Frameworks (Familiarity with Laravel a plus);RESTful and SOAP Web Services;Knowledge and experience using design patterns;Strong SQL skills, writing complex queries; database analysis and optimization skills a plus;Experience with JavaScript libraries: JQuery, Angular and/or Bootstrap;Experience using IDEs (Eclipse, Netbeans, PHPStorm, IntelliJ);Knowledge and experience with PHPUnit, Jenkins CI;PHP Developer preferences (not required):
Multiple object oriented programming language background, knowledge of Java, JSP,Servlets, Python is preferred.;Keywords: php, developer, laravel, rest, restful, soap, web services, webservices, sql, javascript, jquery, angular, bootstrap, phpunit, jenkins, ci, java, jsp, servlets, python, unit testing
http://jobview.monster.com/getjob.aspx?JobId=146398024&amp;jvs=cf,can-6342,can,0"""

	# This job description has both multiple synonyms and multiple secondary synonyms: Angular and AngularJS, Node and NodeJS. 
	self.jobDescriptionMultipleSynonyms5 = r"""Senior Software Engineer, Spanning (SaaS, Cloud Apps, Node.js) in
Austin, Texas
'&gt;' &gt;Accelerate your career as you help reinvent the value and
impact of information for business everywhere. At ****, we are leading
customers on their journey to cloud computing by enabling them to store,
manage, protect and analyze their information assets in a more agile,
trusted and cost-effective way. If you are passionate about technology
and want to be part of the information management revolution, join more
than 50,000+ ****ers around the world who are leading the journey to the
cloud.
Job Description We believe strongly that a
well-designed application makes customers happy, reduces support costs,
and removes the need for static documentation. We ensure that every
feature is customer driven, and simple enough to explain on a single
page wiki. Rather than hire into well defined categories, we are looking
for engineers that want to take ownership, deliver results, and make a
difference in many different parts of our product and process evolution.
Here is a short list of things that we discuss daily. If they make
sense to you, then you likely make sense to us:
Code reviews and Test Driven Development are a way of life. We know that the slow way is the fast way.
;Our engineers are masters of at least 1 part of our stack, are
fluent in 2, and understand all 3. Our technology looks like this:
;JavaScript[Angular/Backbone]/CSS[Sass]
;Java/Node.js
;AWS/SQL[MySql/PostGres]/NoSQL[Cassandra]
;We make heavy use of Source Code Management [Git] tooling and
expect to see multiple code checkins daily. All code commits go through a
highly collaborative code review process.
;A deep understanding of JavaScript and recent experience with
node.js and at least one of the popular client frameworks such as
backbone.js, angular.js, or ExtJS.
;Proven experience with single page web applications that make
asynchronous server requests via REST. I ll call it AJAX just to get the
buzzword hit on search engines.
;Practical experience with CSS and an understanding of responsive
layouts. Experience with CSS pre-processing using SASS or similar tools
is a plus.
;A strong desire to understand how customers use our product, not
just show off all our features.If you think you might be the right
person for this role, we want to hear from you. We look forward to
meeting you.
,;
Region NA
Job Group 1 Engineering
Job Group 2 Product Development
Job Group 3 SW Development
Business Unit 208 - CLOUD SERVICES
Job Code 203033 Senior Software Engineer
Title Senior Software Engineer, Spanning (SaaS, Cloud Apps, Node.js)
Location(s) US - Texas - Austin
Business Core Technologies (CTD)
Functional Area(s) Engineering - Software
Requisition ID 159800BR"""

	# This job description has both multiple synonyms and multiple secondary synonyms: Angular and AngularJS, Node and NodeJS. 
	self.jobDescriptionMultipleSynonyms6 = r"""PHP Developer (PHP / MySQL / JavaScript)
This position is open as of 2/26/2016.
PHP Developer at Growing Entertainment Solutions Company
If you are a PHP Developer with 3 to 5 years of experience, please read on!
Located in Austin TX, the client is a leading provider of end to end ticketing services for some of the most popular music festivals and entertainment events. Their suite of products and serviced include marketing, ticketing fulfillment, and RFID chip tickets. Currently they are in need of an experienced PHP developer to enhance their current product and work on new and innovative solutions.
<b>Top Reasons to Work with Us</b>
1. Stable mid sized tech company with strong backing
2. Develop products that for some of the most exciting and popular events in the world
3. Your work will have a direct impact on enhancing the experience of attending some of the world's best events
<b>What You Will Be Doing</b>
- Collaborating with other Developers, Systems Engineers, Product Managers, Designers, and Quality Assurance on various development projects
- Implementation and design of complex projects
- Review and improve existing code for better performance and sustainability
- New development
- Fixing code defects
- Reviewing user stories and think of ways to improve the product/user experience
- Aid in project planning and estimates
<b>What You Need for this Position</b>
Required:
- eCommerce application development, high volume is desired
- PHP
- SQL queries and database optimization
- Linux (the client uses Apache, Varnish, Memcache, Nginx, MySQL, Redis, Cassandra, MongoDB)
- Front End Development (Javascript, AngularJS, Local Storage, Grunt/Yeoman/Bower)
- SCRUM development process
- Data Design and Modeling
Desired
- DevOps practices (delivery and deployment of infrastructure to AWS)
- Version Control - Git
- AWS (EC2, VPC, EBS, RDS)
- Scripting languages (Javascript/NodeJS, Java, Ruby, Perl or Python )
- Docker
<b>What's In It for You</b>
- Great Compensation (up to 100k base)
- Vacation/PTO
- Medical
- Dental
- Vision
- 401(k)
So, if you are a PHP Developer with 3 to 5 years of experience, please apply today!
<b>Required Skills</b>
eCommerce Application Development, OOP Design Patterns, PHP, Linux, MySQL, Front End Development (JavaScript/Angular etc..), Amazon Web Services (AWS), DevOps Practices (continuous delivery/deployment), Version Control - Git, Scripting Languages (Node/Java/Ruby/Python)
If you are a good fit for the PHP Developer at Growing Entertainment Solutions Company position, and have a background that includes:
eCommerce Application Development, OOP Design Patterns, PHP, Linux, MySQL, Front End Development (JavaScript/Angular etc..), Amazon Web Services (AWS), DevOps Practices (continuous delivery/deployment), Version Control - Git, Scripting Languages (Node/Java/Ruby/Python) and you are interested in working the following job types:
Information Technology, Engineering, Professional Services
http://www.startwire.com/express_apply_jobs/NzIwXzRfSjNGODBXNktDUkM4VzE0WjhUWF9jY2NibWFzdGVydWFfZw==?source=careerbliss_C"""

	self.jobDescriptionMultipleSynonyms7 = r"""Lead Programmer Analyst Job
Listing Info
Facility: Welbilt Walk-Ins, LP - KPS TX
Lead Programmer Analyst
Job ID 7558
Job Number 012435
Location US - Fort Worth, TX
Education Required Bachelors Degree
Languages Required English only
Experience Required Minimum 8 Years
Relocation Provided Yes
General Job Objective
Have you heard?
Blaze the trails of technology as our next Lead Programmer Analyst!
In addition to your involvement in typical programming functions, you'll collaborate with management on projects to include the co-development of project proposals, appropriate timeframes and delivery dates, and methodologies to be used to deliver the desired outcomes.
Major responsibilities include leading a team through the development, design, and implementation of new software platforms aimed at improving the customer (internal &amp; external) information flow. You're on top of IT if you possess pervasive knowledge in these areas!
ASP.Net MVC;WCF services, long running processing, asynchronous services;Entity Framework and LINQ;T-SQL and MS SQL Server;Javascript front-end frameworks, jQuery, and AJAX;Inversion or Control / Dependency Injection;Team Foundation Server source control management;Agile/Scrum methodologies;Build and Test automation and test frameworks;Batch and shell;XML and XSLT;A reporting tool;C++;Message queue;Application Life-cycle management
Demonstrated knowledge of engineering design work, been engaged in both a development and maintenance focused programmers role, solid experience leading projects from inception to completion, and highly skilled in training elements connected to end user interface. Manufacturing automation experience highly desired. Reporting directly to the Programming Manager, this position is based in Fort Worth, Texas.
If you're up to the challenge, the reward is satisfaction . . . and knowing you helped Build Something Real. Join our passionate team and help build something you can be proud of a future filled with passion, pride, and satisfaction.;Essential Job Functions
Analyzes, researches, designs, codes, tests, deploys, programs and applications.;Provide leadership for the IS team, in accordance with enterprise and local policy;Maintains programs after implementation;Consults with senior leadership on projects to include the co-development of project proposals, appropriate timeframes and delivery dates, and methodology to be used to deliver the desired outcomes.;Provide technical guidance to staff regarding application and system programming and analysis, best practices, functional cross training, code tours and department procedures.;Designs and code screen layouts, graphical user interfaces, printed output, and interfaces with other systems.;Research and evaluate software and hardware improvements that will assist in programming projects or to be introduced as new program platforms.;Insures data integrity and software reliability;Writes and maintains documentation to describe program development, logic, coding, changes, and corrections, including any required corporate policy compliance documentation;Provides technical assistance by responding to inquiries concerning errors, problems, and questions with programs;Requirements
Bachelor's degree and a minimum of 8 years of information technology experience required.;Must have working knowledge of engineering design work, been engaged in both a development and maintenance focused programmers role, solid experience leading projects from inception to completion, and highly skilled in training elements connected to end user interface.;Should have thorough understanding of the business environment, spanning all disciplines and the interplay that occurs in the day-to-day business environment.;Manufacturing automation experience highly desired.;Incumbent must have pervasive knowledge in the following languages or programming software: ASP.Net MVC, WCF services, long running processing, asynchronous services, entity framework and LINQ, T-SQL and MS SQL Server, Javascript front-end frameworks, jQuery, and AJAX, Inversion or Control / Dependency Injection, Team Foundation Server source control management, Agile/Scrum methodologies, build and test automation and test frameworks, batch and shell, XML and XSLT, A reporting tool, C++, message queue, and Application Life-cycle management. Strong knowledge in the following is preferred: Other NoSql and search index technologies, SQL Server Reporting Services, Inventor, CAD API, ObjectARX/DBX, Active X, COM, SharePoint, Web frameworks for mobile,
Windows Mobile 5.0-6.5, Symbol/Motorola Mobility SDK, Progress DB and Progress 4GL, DBA Capabilities, Proficiency with vector-based math, geometry, and computational algorithms;Incumbent must have exceptional interpersonal communication skills, oral and written.;Incumbent must have knowledge of project management methodologies and ability to document, communicate and implement a project plan. Pluses will include ability to engage in analytical investigative process with end users to determine root cause of a problem and then design an effective solution meeting all of the needs of the end user.;Manitowoc Foodservice, a division of The Manitowoc Company, Inc., designs, manufactures and supplies best-in-class food and beverage equipment for the global foodservice market. Manitowoc Foodservice offers customers unparalleled operator and patron insights, collaborative kitchen solutions, culinary expertise and world-class implementation support and service, whether locations are around the corner or across the globe. With operations in the Americas, Europe and Asia, the company has a portfolio of best-in-class brands including Cleveland, Convotherm , Delfield , Frymaster , Garland , Kolpak , Kysor Panel Systems , Lincoln, Manitowoc Ice, Merco , Multiplex , Merrychef , Servend and Manitowoc Beverage Systems.
J2W:CB1;Eeo Statement
The Manitowoc Company is an Equal Opportunity Employer. Minorities, Females, Disabled, and Veterans are encouraged to apply."""

	self.jobDescriptionMultipleSynonyms8 = r"""C# / .Net Developer
We are currently seeking a C#.Net Developer in Austin, Texas to join our team. We are the world's leading information security and advisory company. In order to be considered for the Development Engineer position, the candidate must work well with others and have in-depth knowledge in the .Net and C# environments.
Job Responsibilities
Work closely with other .Net C# Developers;Collaborate with Project Managers, Architects and other departments to develop both new and expand functionality to existing applications to provide delivery of the platform according to schedule;Mentor and Assure Design and Coding Standards are maintained;Bring depth in the .NET and C# environments;Attend all design and code reviews for the features that are being implemented within the system;Learn the architecture of the platform and assure that the architecture is maintained as features are added to the system;Required Skills &amp; Qualifications
3 - 7 years of experience;Experience with the following languages: C,C++, Assembler, C#, SQL,;Experience with the following Libraries/Frameworks: WinAPI, .NET, OLE/COM, Microsoft Office API, ADO, .NET, .NET 4.5, C#, LINQ, SQL, XML, XAML, COM, Design Patterns, MVC, MVP, MVVM , Ms SQL/T-SQL, ADO.Net Entity Framework, Linq to Sql, Multithreading/Multiprocessing, Networking, Obfuscation, Jira, GUI design, OOD, OOP ,Ms;Experience with the following Software: Microsoft Visual Studio, SVN, Jira;Experience with the following Systems: Windows 95/98/2000/XP/Vista/7/8, Linux Hardware: PCs, Peripherals, Network accessories;Experience with the following Databases: MySQL, SQLite, MS SQL, Oracle, Postgre SQL, MS Access;Experience with the following Environments: Web services, SQL SERVER , SOAP;
https://www.ziprecruiter.com/jobs/providence-partners-2153f745/c-net-developer-88570ade?mid=526"""


	self.jobDescriptionMultipleSynonyms9 = r"""Sr ETL Developer
Join a fast-paced team developing web-based applications as it should be done: employing Agile principles, test-driven development, and design patterns.
The ideal candidate is experienced in a broad set of database technologies. The candidate should have strong analytical, problem solving, and communication skills with a keen attention to detail. As part of a multi-disciplined development team, the candidate should be motivated to able to jump in, attack new challenges, and learn new skills independently.
Required Skills and Experience
Senior ETL developer with 5-7 years demonstrable experience using ETL tools with SQL Server 2008, SQL Server Integration Services 2008, Altova MapForce experience preferred
Strong knowledge of Data Warehousing methodologies and concepts, including and not limited to: star schemas, snowflakes, ETL processes, dimensional modeling and reporting tools
Should have good understanding of SSIS architecture and SQL Server data base artifacts: SQL Server 2005/2008 Integration Services (SSIS), Analysis Services (SSAS), Reporting Services (SSRS)
Experience in analysis, design and construction of data marts and data warehouses - preferably SQL Server-based
Strong in T-SQL, Stored Procedures and other database related artifacts
Must demonstrate the ability to analyze, research or query existing relational and dimensional databases using SQL
Demonstrated experience developing and implementing business intelligence solutions such as dashboards, reports and scorecards - e.g., SQL Server Business Intelligence Development Studio (BIDS), Cognos, Business Objects
Experience manipulating various data sources to support management business decisions
Experience in performance tuning of database execution
Demonstrated understanding of Test Driven Development (TDD) and an understanding of the principles of Lean Software Development is a desired
Ability and willingness to follow established development and testing practices
Demonstrated leadership abilities and teamwork skills
Bachelor's degree or higher in computer technology discipline is desired
Experience in the education sector is a plus
Job Responsibilities
Performing ETL on education data from school districts to prepare data for state-wide real-time education dashboard tools
Developing ETL to cleanse and transform education data using SSIS 2008
Design Star Schema for fact and dimension tables
Develop ETL and reports to identify and report data anomalies and exception reports
Modify existing ETL packages to support updates to data standard and reporting tools
* U.S. citizen or green card holder
JOB REQUIREMENTS
Senior ETL developer with 5-7 years demonstrable experience using ETL tools with SQL Server 2008, SQL Server Integration Services 2008, Altova MapForce experience preferred
JOB SNAPSHOT
Employment TypeFull-Time
Job TypeInformation Technology
EducationNot Specified
ExperienceAt least 5 year(s)
Manages OthersNot Specified
IndustryComputer Software
Required TravelNone
http://www.careerbuilder.com/JobSeeker/Jobs/JobDetails.aspx?HostID=US&amp;SiteID=cb_emailrec_US&amp;Job_DID=JHP2S36SHMWX0C58CQP"""

	# This job description has both Angular.js and Angular, and SQL Server and MS SQL
	self.jobDescriptionMultipleSynonyms10 = r"""UI/UX Angular.js Developer
We
are seeking a 3+ year UI/UX Developer with strong Angular.js for our
Austin, TX based client that specializes in financial trading and
quantitative analysis of market trends. This is a new position due to
growth and has been slated as a long-term contract with possible
conversion to full-time.
Duration of the project will be through
both beta and production launches. The tool, which generates algorithms
to help traders automate financial and stock trading processes, has been
built but our client requires a talented UI/UX Angular.js Developer to
take to it to the next level. The solution has been developed with a
stack of Angular.js, Node.js, JSON, REST, HTML/CSS, and PostgreSQL.
Conversion
to full-time will include a competitive base salary based on market
rate and candidate s W2 salary history, up to 50% of base salary bonus
structure (hybrid individual &amp; company performance) 401k w/
matching, and affordable healthcare benefits.
Dress code is very casual (shorts, t-shirts) and the CIO offers flex schedules when needed.
If converted to full-time, the benefits of the UI/UX Angular.js position include
Bonus structure of up to 50% base salary
401k w/ matching 100% of first 1%, 50% of next 6%
BCBS health insurance, AD&amp;D/Life, LTD, HSA $450 annual company contribution
EAP child care, financial &amp; legal assistance
PTO; 10 days vacation, 5 personal/sick days, 9 holidays (all NYSE recognized holidays)
Learn the financial trading industry
Direct mentorship from CIO
Work with seasoned developers
Casual dress code and office environment
Remote work and flex schedule at manager s discretion
Career track for growth and promotion
Your ideas are valued and you will see your contributions in action
Our client at a glance
Mid-sized with 7 IT professionals 4 Software Developers, 2 DevOps Engineers, 1 CIO
20 years in business; casual office environment with emphasis on collaboration
Agile &amp; RAD SDLC constant development and feedback from end-users
Hosts own servers and infrastructure
High employee tenure
Leader in its niche
Proprietary financial trading solutions: gray and black box trading for
partial / full automation, execution platform, and a tool to develop
trading algorithms.
Technologies used: MFC, .NET, MS SQL,
Windows Server, SVN, Visual Studio, C++, C#, IronPython, ZeroMQ, SBE,
Redis, log4cxx, log4net, xercesc, boost, Node.js Angular.js, JavaScript,
JQuery, Engine X, Linux, Python, PyPy, Scikit Learn, Pandas Numpy,
Numba, Bokeh, Docker, Slurm, Salt, Flask, HDF5, Tornado, PostgresSQL,
Jupyter Hub, Airflow, iopro, conda, rsync, bash, HTML5/CSS3, REST, IIS,
JSON, ASP.NET, MySQL
UI/UX Angular.js Developer responsibilities:
True hybrid position: code and design, with focus on Angular.js
Assist established development team to improve software tool s
intuitiveness by measuring end-user workflow, heat maps, and usage
statistics.
Utilize design knowledge to improve user interface, dashboards, buttons/widgets, and menus.
Performance-tuning and testing. Optimize application for speed and scalability.
Ensure user input via web forms is validated.
Interface with various RDBMS solutions.
Operational support.
Integrate tool into a WordPress site along with Vanilla Forum.
Heavy collaboration with team.
Additional projects may include integrating another mature, internal .NET application s UI into the company s website.
Requirements of the UI/UX Angular.js Developer
Strong Angular.js coding ability
Design skillset UI/UX, user workflow, graphics/buttons/dashboards/menu design
HTML5/CSS3
Databases PostgreSQL, SQL Server, and/or MySQL
Windows and Linux environments
SVN, JSON
WordPress (basic knowledge)
Vanilla Forum (will be taught)
Rapid prototyping and responsive web design
Other technologies such as Node.js, ASP.NET, RESTful web services, IIS, and C# are nice to have, but not are required.
Interested? Apply now! Our client is moving fast
UI/UX Angular.js Developer candidates, please submit resume to this position by applying directly or contacting via LinkedIn at https://www.linkedin.com/in/jonesjustinb
Interview
process will consist of phone screen with recruiter, technical phone
screen with CIO, and in-person face-to-face interview at Austin, TX
location.
Employment Type: Contractor
Compensation:
$50 to $65 Hourly
https://www.ziprecruiter.com/jobs/ztech-solutions-12d5f4d2/ui-ux-angular-js-developer-cd15e115?mid=5&amp;source=ziprecruiter-firehose&amp;contact_id=6177d945&amp;auth_token=9d852e14942b919640f301662a611982671c4d2b&amp;expires=1460461280"""

	# 0301_0485/7abcbfd5-5712-40f8-b535-b6fc4f98df45.txt
	self.jobDescription_tsql_sqlserver1 = r"""C#.NET Developer
Duration: 12 months, contract extensions likely
Job Description:
RCM Technologies is currently staffing a consultant as a Senior C#.NET Developer in Austin, TX
Duration: 12 months
Start date: ASAP
Experience: 5 years minimum
Skills:
C#.NET, ASP.NET, MVC3/4, Web Services, T-SQL.;T-SQL, SQL Server experience;UX, front-end development to enhance customer user experience;Strong competencies and experience in data structures and concepts such parentheses balancing.;Strong experience and competencies in .NET frameworks, MVC frameworks, MVC Entity frameworks, and N-tier architecture;Skilled in JavaScript and common libraries.;"""

	# 0301_0485/b267f95c-3a87-4618-9f9e-b894a3564de0.txt
	self.jobDescription_tsql_sqlserver2 = r"""Software Developer
Design and develop custom software solutions utilizing the latest Microsoft and .NET technologies. Work alongside business partners and application teams to fulfill software system development requirements for assorted Business Areas.
ESSENTIAL DUTIES AND RESPONSIBILITIES include the following. Other duties may be assigned.
Development of browser based applications using Microsoft technologies in a Service Oriented Architecture.;Follow technical task assignments through from inception to completion.;Participate in collaborative environment including to contribution on software design, development estimates, and fulfillment of assigned tasks.;Coordinate activities with technical project management to ensure that tasks progress on schedule.;Maintain task reporting for management, customers or others.;Confer with technical project personnel for technical advice and problem resolution.;
QUALIFICATIONS - To perform this job successfully, an individual must be able to perform each essential duty satisfactorily. The requirements listed below are representative of the knowledge, skill, and/or ability required.
Minimum requirements:
3-5 years of application development experience.;A strong C# ASP.NET background and a passion for technology.HTML, JavaScript, CSS, AJAX, and jQuery experience is a plusStrong design skills and ability to work independently and in a team setting.;Strong working knowledge of SQL Server (T-SQL, Stored Procedures, and performance tuning).;A broad knowledge of ASP.NET architecture and development as well as a strong knowledge of web services such as SOAP, REST, and WCF Data Services.;Established experienced with C# development using technologies including: C#, .NET 3.5 4.5, Web Services, and WCF.;MVC 4 experience would be nice to have.;Understanding of Object-relational Mapping (Entity Framework, nHibernate, etc).;EDUCATION AND/OR EXPERIENCE:
A bachelor s degree in Computer Science and 3 - 5 years of experience in the analysis, design, development and deployment of software components preferred.
Additional expertise or certifications may substitute for education. Financial Services experience is a plus.
Apply here:https://www7.ultirecruit.com/NAT1022/JobBoard/ListJobs.aspx?__vt=ExtCan"""

	# 0486_0600/538d23e4-b33b-4534-82c1-9cfc8a3db2c2.txt
	self.jobDescription_tsql_sqlserver3 = r"""c#.Net Developer Contract 12 months
Austin, TX 1/21/2014
RCM Technologies is currently staffing a consultant as a Senior C#.NET Developer in Austin, TX
Duration: 12 months
Start date: ASAP
Experience: 7-8 years minimum
Skills:C#.NET, ASP.NET, MVC3/4, Web Services;T-SQL, SQL Server experience;Strong Java front end development experience;Responsibilities:
Senior developer tasks working on a POC project for data caprute and presentation.
Key competencies:
C#.NET, ASP.NET, Web Services, T-SQL.;Significant web UI application development experience;Strong competencies and experience in data structures and concepts such parentheses balancing.;Strong experience and competencies in .NET frameworks, MVC frameworks, MVC Entity frameworks, and N-tier architecture;JavaScript and strong competency with common libraries.;Experience with Java front end development;Specific experience with REST.api or WEB.api.;
JOB REQUIREMENTS
c#C#.NET, ASP.NET, MVC3/4, Web Services;T-SQL, SQL Server experience;Strong Java front end development experience;
Please contact: [Click Here to Email Your Resum ] at RCM Technologies for confidential consideration
[Click Here to Email Your Resum ]
952-831-1628 Please email resume before calling.
JOB SNAPSHOT
Employment TypeContractor
Job TypeInformation Technology
EducationNot Specified
ExperienceNot Specified
Manages OthersNot Specified
IndustryConsulting
Required TravelNot Specified
Job ID66"""

	# 1401_1600/2b87a790-bd6b-4d1f-9926-03a81406425a.txt
	self.jobDescription_tsql_sqlserver4 = r"""C# / .Net Developer
We are currently seeking a C#.Net Developer in Austin, Texas to join our team. We are the world's leading information security and advisory company. In order to be considered for the Development Engineer position, the candidate must work well with others and have in-depth knowledge in the .Net and C# environments.
Job Responsibilities
Work closely with other .Net C# Developers;Collaborate with Project Managers, Architects and other departments to develop both new and expand functionality to existing applications to provide delivery of the platform according to schedule;Mentor and Assure Design and Coding Standards are maintained;Bring depth in the .NET and C# environments;Attend all design and code reviews for the features that are being implemented within the system;Learn the architecture of the platform and assure that the architecture is maintained as features are added to the system;Required Skills &amp; Qualifications
3 - 7 years of experience;Experience with the following languages: C,C++, Assembler, C#, SQL,;Experience with the following Libraries/Frameworks: WinAPI, .NET, OLE/COM, Microsoft Office API, ADO, .NET, .NET 4.5, C#, LINQ, SQL, XML, XAML, COM, Design Patterns, MVC, MVP, MVVM , Ms SQL/T-SQL, ADO.Net Entity Framework, Linq to Sql, Multithreading/Multiprocessing, Networking, Obfuscation, Jira, GUI design, OOD, OOP ,Ms;Experience with the following Software: Microsoft Visual Studio, SVN, Jira;Experience with the following Systems: Windows 95/98/2000/XP/Vista/7/8, Linux Hardware: PCs, Peripherals, Network accessories;Experience with the following Databases: MySQL, SQLite, MS SQL, Oracle, Postgre SQL, MS Access;Experience with the following Environments: Web services, SQL SERVER , SOAP;"""

	# 1401_1600/a6593048-80da-46d8-b8d3-07a1ef610f17.txt
	self.jobDescription_tsql_sqlserver5 = r""".Net Developer (553666)
General Information
Job Posting ID 7057574 Creation Date Oct 09, 2015
Employer Posting No --- Closing Date Nov 08, 2015
Job Site Address AUSTIN, Texas 73301 Employer Type Staffing Company
Openings 1
Job Description
C# Developer
Austin, Texas
Salary: $95,000-115,000
If you are interested, please send your resume to Cameron Banning at cbanning@apexsystemsinc.com
Apex Systems is seeking a Senior .Net Developer. This position will plan, design, develop, test, debug, and deploy mission-critical applications using C# ASP.NET. We are seeking a candidate who is a strong communicator and highly proficient with .NET technologies.
Skills Required
C# --must be proficient
ASP.NET
JavaScript (JQuery/JSon/AJAX is a plus)
Web services
MS SQL (T-SQL)
Other Qualifications
4+ years of .NET experience
Good planning, problem solving, analytical, people and communication skills required
Test and debug code. Identify and implement design patterns where appropriate
Create design documents and contribute to other technical documentation as required
Present or demonstrate products and concepts to various audiences
Work with a business analyst to translate business requirements into user stories
Work in a collaborative environment; be willing and able to provide and receive technical assistance
Support existing products and platforms while encouraging creative use of new technologies where appropriate
Balance and maintain progress on concurrent tasks of varying magnitude
Education
Bachelor s degree preferred in Computer Science, Information Systems, or related field and/or relevant experience
We are an equal opportunity employer. We evaluate qualified applicants without regard to race, color, religion, sex, national origin, disability, veteran status, and other protected characteristics. The EEO is the Law poster is available http://www1.eeoc.gov/employers/upload/eeoc_self_print_poster.pdf
Equal Opportunity/Affirmative Action Employer
VEVRAA Federal Contractor
We request Priority Protected Veteran &amp; Disabled Referrals for all of our locations within the state.
Supervisory Experience Required No
Shift Days (First) Duration Temp OR Temp to Hire"""

	# 0301_0485/b84b6a03-f0c5-4e16-ae31-150da3a6c87f.txt
	self.jobDescription_tsql_sqlserver01 = r"""Senior Asp.net MVC Engineer
Full-time $80k - $120k
Senior Asp.net MVC Engineer for fast growing innovative SaaS company. We're passionate about helping online businesses become more productive and save our clients thousands of hours every day by automating the fulfillment side of their business. We partner with top eCommerce and shipping companies in the world like eBay and Amazon to make a previously complicated and labor-intensive process simple and enjoyable. Our cloud SAAS Software is very exciting and currently integrates with over 50 different ecommerce systems including Amazon, Ebay, Shopify. We quadrupled last year and now that were are profitable hope to do the same thing in 2014.
Top 3 Reasons to Work with Us
1. Great pay and Excellent benefits
2. Career growth and financial stability
3. Flexible work environment
What You Will Be Doing
As a Senior Asp.net MVC Developer, you will be responsible for building rich and interactive web applications that help our customers manage their eCommerce sales. Enjoy creative freedom in a start-up environment that embraces new technologies. If you are interested in building cutting-edge SaaS software that is loved by its customers come join us today!!
What You Need for this Position
At Least 3 Years of experience and knowledge of:
- Broad knowledge in web-based application development
- 2+ years experience with ASP.NET MVC and C#
- Experience with client-side scripting (JavaScript, jQuery, Backbone js, Bootstrap).
- Experience with T-SQL and SQL Server
- C#
- ASP.NET
- MVC
- SQL
- JavaScript
- JQuery
- TSQL
- Client Side Scripting
- BackBone
- SaaS
What's In It for You
- Vacation/PTO
- Medical
- Dental
- Relocation Assistance
So, if you are a Senior Asp.net MVC Engineer with experience, please apply today!
Preferred Skills
C#;ASP.NET;MVC;SQL;Javascript;jQuery;TSQL;SaaS;Cloud;eCommerce;
Job ID: CMM-1133480"""


    def skill_pair_default(self, o):
	if isinstance(o, SkillPair):
	    return dict(id=o.id,
		    secondary_term=o.secondary_term,
                    number_of_times=o.number_of_times,
                    ratio=str(o.ratio))

    def job_posting_to_skill_pair_default(self, o):
	if isinstance(o, JobPostingToSkillPair):
	    return dict(skill_pair_id = o.skill_pair_id,
		job_file_name=o.job_file_name,
		    job_ad_snippet=o.job_ad_snippet)


    def test_process_job_descriptions_correctly(self):
	jobFileNames = []
	jobFileNames.append("1801_2000\f0ac5805-3799-4ead-9ffa-494040b58b93.txt") # jobFileNames[0] -> self.jobDescriptionMultipleSynonyms6
	jobFileNames.append("1401_1600/2b87a790-bd6b-4d1f-9926-03a81406425a.txt") # jobFileNames[1] -> self.jobDescriptionMultipleSynonyms8
	jobFileNames.append("0601_0800\0442b780-b100-4a1b-85b3-30bfee4568ef.txt") # jobFileNames[2] -> self.jobDescriptionMultipleSynonyms9
	jobFileNames.append("1801_2000\bd6f79bd-c711-4dcf-ba5e-5adbec448853.txt") # jobFileNames[3] -> self.jobDescriptionMultipleSynonyms10
	jobFileNames.append("0301_0485/b84b6a03-f0c5-4e16-ae31-150da3a6c87f.txt") # jobFileNames[4] -> self.jobDescription_tsql_sqlserver01

	jobDescriptions = [self.jobDescriptionMultipleSynonyms6,
			   self.jobDescriptionMultipleSynonyms8, self.jobDescriptionMultipleSynonyms9, self.jobDescriptionMultipleSynonyms10, self.jobDescription_tsql_sqlserver01]

	skillsDictionary = {}
	skillsPostCountsDict = {}
	jobPostingsToSkillsPairs = []

	for i in range(len(jobDescriptions)):
	    jobDescriptionProcessor = JobDescriptionProcessor(self.keywordsWithSynonyms)
	    jobDescriptionProcessor.processJobDescription(jobFileNames[i], jobDescriptions[i], skillsDictionary, skillsPostCountsDict, jobPostingsToSkillsPairs)

	expectedSkillsPostCountsDict = {"Angular": 2, "Node": 2, "SQL Server": 4, "SSIS": 1, "TransactSQL": 3}
	self.assertDictEqual(expectedSkillsPostCountsDict, skillsPostCountsDict)	

	expectedSkillsDictionary = {"Angular": {"Node": {"id": None, "number_of_times": 2, "ratio": "None", "secondary_term": "Node"}, "SQL Server": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "SQL Server"}}, "Node": {"Angular": {"id": None, "number_of_times": 2, "ratio": "None", "secondary_term": "Angular"}, "SQL Server": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "SQL Server"}}, "SQL Server": {"Angular": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "Angular"}, "Node": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "Node"}, "SSIS": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "SSIS"}, "TransactSQL": {"id": None, "number_of_times": 3, "ratio": "None", "secondary_term": "TransactSQL"}}, "SSIS": {"SQL Server": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "SQL Server"}, "TransactSQL": {"id": None, "number_of_times": 1, "ratio": "None", "secondary_term": "TransactSQL"}} , "TransactSQL": {"SQL Server": {"id": None, "number_of_times": 3, "ratio": "None", "secondary_term": "SQL Server"}, "SSIS": {"id": None, "number_of_times": 1,"ratio": "None", "secondary_term": "SSIS"}}}


	skillsDictionaryJson = json.dumps(skillsDictionary, sort_keys=True, default=self.skill_pair_default)

	skillsDictionaryUnwrapped = json.loads(skillsDictionaryJson)
	self.assertDictEqual(expectedSkillsDictionary, skillsDictionaryUnwrapped)

    def test_handle_multiple_synonyms_correctly_in_creating_pairs(self):
	jobFileName1 = "0301_0485\3bc612d0-903b-4c5d-ae45-d6f1f30d4b96.txt"

	synonyms = ["TransactSQL", "Transact SQL", "Transact-SQL", "TSQL", "T-SQL"]

	skillKeyword = "TransactSQL"
	secondarySkillDict = {}
	skillPairProcessor1 = SkillPairProcessor(jobFileName1, self.jobDescriptionMultipleSynonyms7, skillKeyword)
	jobPostingsToSkillsPairsForThisKeyword1 = skillPairProcessor1.createOrModifySkillPairs(self.keywordsWithSynonyms, synonyms, secondarySkillDict)	

	jobFileName2 = "1401_1600/2b87a790-bd6b-4d1f-9926-03a81406425a.txt"
	skillPairProcessor2 = SkillPairProcessor(jobFileName2, self.jobDescriptionMultipleSynonyms8, skillKeyword)
	jobPostingsToSkillsPairsForThisKeyword2 = skillPairProcessor2.createOrModifySkillPairs(self.keywordsWithSynonyms, synonyms, secondarySkillDict)	

	jobFileName3 = "0601_0800\0442b780-b100-4a1b-85b3-30bfee4568ef.txt"
	skillPairProcessor3 = SkillPairProcessor(jobFileName3, self.jobDescriptionMultipleSynonyms9, skillKeyword)
	jobPostingsToSkillsPairsForThisKeyword3 = skillPairProcessor3.createOrModifySkillPairs(self.keywordsWithSynonyms, synonyms, secondarySkillDict)	

	jobFileName4 = "1801_2000\f0ac5805-3799-4ead-9ffa-494040b58b93.txt"
	skillPairProcessor4 = SkillPairProcessor(jobFileName4, self.jobDescriptionMultipleSynonyms6, skillKeyword)
	jobPostingsToSkillsPairsForThisKeyword4 = skillPairProcessor4.createOrModifySkillPairs(self.keywordsWithSynonyms, synonyms, secondarySkillDict)	

	jobFileName5 = "1801_2000\bd6f79bd-c711-4dcf-ba5e-5adbec448853.txt"
	skillPairProcessor5 = SkillPairProcessor(jobFileName5, self.jobDescriptionMultipleSynonyms10, skillKeyword)
	jobPostingsToSkillsPairsForThisKeyword5 = skillPairProcessor5.createOrModifySkillPairs(self.keywordsWithSynonyms, synonyms, secondarySkillDict)	

    def test_handle_multiple_synonyms_correctly_in_job_snippets(self):
	jobFileName = "0301_0485\024a22bd-5011-4a3a-bccd-e2ab03065c79.txt"
	expected_snippet = r"web development experience in ASP.NET/C#;Database knowledge in <b>MSSQL</b> Server, with Graphics and GUI c ... ed proficiency in: ASP.NET, C#,<b>JQuery</b>, XML, HTML,CSS, <b>MS SQL</b> Server, Source Control, MS Office Suite;Desired proficiency i"

	synonyms1 = ["SQL Server", "SQLServer", "MSSQL", "MS SQL"]
	secondarySynonyms1 = ['JQuery']

	snippetBuilder = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescriptionMultipleSynonyms1)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
	
        self.assertEqual(job_ad_snippet, expected_snippet)

	synonyms2 = ['JQuery']
	secondarySynonyms2 = ["SQL Server", "SQLServer", "MSSQL", "MS SQL"]

	snippetBuilder = SnippetBuilderIter(synonyms2, secondarySynonyms2, self.jobDescriptionMultipleSynonyms1)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
	
        self.assertEqual(job_ad_snippet, expected_snippet)

    def test_handle_multiple_js_synonyms_correctly_in_job_snippets(self):
	jobFileName = "1801_2000\f0ac5805-3799-4ead-9ffa-494040b58b93.txt"
	expected_snippet = r" Front End Development (Javascript, <b>AngularJS</b>, Local Storage, G ... uages (Javascript<b>NodeJS</b>, Java, Ruby, Perl ... pment (JavaScript<b>Angular</b> etc..), Amazon We ... ipting Languages <b>Node</b>/Java/Ruby/Python) ... pment (JavaScript<b>Angular</b> etc..), Amazon We ... ipting Languages <b>Node</b>/Java/Ruby/Python) and you are inte"

	synonyms1 = ["Node", "Node.js", "NodeJS"]
	secondarySynonyms1 = ["Angular", "Angular.js", "AngularJS"]

	snippetBuilder = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescriptionMultipleSynonyms6)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
	
        self.assertEqual(job_ad_snippet, expected_snippet)

	synonyms2 = ["Angular", "Angular.js", "AngularJS"]
	secondarySynonyms2 = ["Node", "Node.js", "NodeJS"]

	snippetBuilder = SnippetBuilderIter(synonyms2, secondarySynonyms2, self.jobDescriptionMultipleSynonyms6)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
        self.assertEqual(job_ad_snippet, expected_snippet)

    def test_handle_multiple_dot_js_synonyms_correctly_in_job_snippets(self):
	jobFileName = "1601_1800\7bb60d26-d607-4234-83ef-9e07e6d0f447.txt"
	expected_snippet = r"gineer, Spanning (SaaS, Cloud Apps, <b>Node</b>.js) in Austin, Te ... this: ;JavaScript<b>Angular</b>/Backbone]/CSS[Sass] ;Java/<b>Node</b>.js ;AWS/SQL[MySql ... t experience with<b>node</b>.js and at least o ... h as backbone.js,<b>angular</b>.js, or ExtJS. ;Pr ... SaaS, Cloud Apps,<b>Node</b>.js) Location(s) US - Texas - Austi"

	synonyms1 = ["Node", "NodeJS"]
	secondarySynonyms1 = ["Angular", "AngularJS"]

	snippetBuilder = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescriptionMultipleSynonyms5)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
	
        self.assertEqual(job_ad_snippet, expected_snippet)

	synonyms2 = ["Angular", "AngularJS"]
	secondarySynonyms2 = ["Node", "NodeJS"]

	snippetBuilder = SnippetBuilderIter(synonyms2, secondarySynonyms2, self.jobDescriptionMultipleSynonyms5)
	job_ad_snippet = snippetBuilder.buildJobSnippet()
	lines = job_ad_snippet.split("\n")
	job_ad_snippet = ' '.join(lines)
        self.assertEqual(job_ad_snippet, expected_snippet)	

    def test_bold_in_job_snippets(self):
	expected_snippet1 = "5 years minimum Skills: C#.NET, ASP.NET, MVC3/4, Web Services, <b>T-SQL</b>.;<b>T-SQL</b>, <b>SQL Server</b> experience;UX, front-end development to enhance customer user"

	synonyms1 = ["TransactSQL", "Transact SQL", "Transact-SQL", "TSQL", "T-SQL"]
	secondarySynonyms1 = ["SQL Server", "SQLServer", "MSSQL", "MS SQL"]

	snippetBuilder1 = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescription_tsql_sqlserver1)
	job_ad_snippet1 = snippetBuilder1.buildJobSnippet()
	lines = job_ad_snippet1.split("\n")
	job_ad_snippet1 = ' '.join(lines)
	
        self.assertEqual(job_ad_snippet1, expected_snippet1)

	expected_snippet2 = "nd ability to work independently and in a team setting.;Strong working knowledge of <b>SQL Server</b> (<b>T-SQL</b>, Stored Procedures, and performance tuning).;A broad knowledge of ASP.NET architec"

	snippetBuilder2 = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescription_tsql_sqlserver2)
	job_ad_snippet2 = snippetBuilder2.buildJobSnippet()
	lines = job_ad_snippet2.split("\n")
	job_ad_snippet2 = ' '.join(lines)
	self.assertEqual(job_ad_snippet2, expected_snippet2)

	expected_snippet3 = "lls:C#.NET, ASP.NET, MVC3/4, Web Services;<b>T-SQL</b>, <b>SQL Server</b> experience;Strong Ja ... P.NET, Web Services,<b>T-SQL</b>.;Significant web UI  ... MVC3/4, Web Services<b>T-SQL</b>, <b>SQL Server</b> experience;Strong Java front end develop"

	snippetBuilder3 = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescription_tsql_sqlserver3)
	job_ad_snippet3 = snippetBuilder3.buildJobSnippet()
	lines = job_ad_snippet3.split("\n")
	job_ad_snippet3 = ' '.join(lines)
	self.assertEqual(job_ad_snippet3, expected_snippet3)

	expected_snippet4 = " SQL, XML, XAML, COM, Design Patterns, MVC, MVP, MVVM , Ms SQL/<b>T-SQL</b>, ADO.Net Entity Framework, Linq ... owing Databases: MySQL, SQLite,<b>MS SQL</b>, Oracle, Postgre SQL, MS Access ... ing Environments: Web services,<b>SQL SERVER</b> , SOAP;"

	snippetBuilder4 = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescription_tsql_sqlserver4)
	job_ad_snippet4 = snippetBuilder4.buildJobSnippet()
	lines = job_ad_snippet4.split("\n")
	job_ad_snippet4 = ' '.join(lines)
	self.assertEqual(job_ad_snippet4, expected_snippet4)

	expected_snippet5 = "# --must be proficient ASP.NET JavaScript (JQuery/JSon/AJAX is a plus) Web services <b>MS SQL</b> (<b>T-SQL</b>) Other Qualifications 4+ years of .NET experience Good planning, problem solving, "

	snippetBuilder5 = SnippetBuilderIter(synonyms1, secondarySynonyms1, self.jobDescription_tsql_sqlserver5)
	job_ad_snippet5 = snippetBuilder5.buildJobSnippet()
	lines = job_ad_snippet5.split("\n")
	job_ad_snippet5 = ' '.join(lines)
	self.assertEqual(job_ad_snippet5, expected_snippet5)

if __name__ == '__main__':
    unittest.main()
