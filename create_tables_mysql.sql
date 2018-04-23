CREATE TABLE sc1_skill_post_counters (skill_term VARCHAR(128), number_of_postings INTEGER, PRIMARY KEY (skill_term));

CREATE TABLE sc1_skill_pairs (id INTEGER NOT NULL AUTO_INCREMENT, primary_term VARCHAR(128), secondary_term VARCHAR(128), number_of_times INTEGER, PRIMARY KEY (id));

CREATE TABLE sc1_job_postings_to_skill_pairs (job_file_name VARCHAR(128), skill_pair_id INTEGER, job_ad_snippet VARCHAR(1500), PRIMARY KEY (job_file_name, skill_pair_id));

CREATE TABLE sc2_job_locations (job_file_name VARCHAR(140) NOT NULL, location VARCHAR(140) NOT NULL, PRIMARY KEY (job_file_name, location);

-- Created by PHPMyAdmin:

CREATE TABLE `skillclusters`.`sc2_job_locations` ( `job_file_name` VARCHAR(140) NOT NULL , `location` VARCHAR(140) NOT NULL ) ENGINE = InnoDB;


CREATE TABLE `skillclusters`.`sc2_job_listings` ( `job_file_name` VARCHAR(140) NOT NULL , `date_created` DATE NOT NULL , `company_name` VARCHAR(256) NULL , `job_title` VARCHAR(256) NULL ) ENGINE = InnoDB;

CREATE TABLE `skillclusters`.`sc2_job_hyp_company_mappings` ( `job_file_name` VARCHAR(140) NOT NULL , `hyp_company` VARCHAR(256) NOT NULL ) ENGINE = InnoDB;




SELECT * FROM information_schema.columns WHERE table_schema = 'elze$skillclusters';