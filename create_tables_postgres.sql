CREATE TABLE sc1_skill_post_counters
(
  skill_term character varying(140) NOT NULL,
  number_of_postings integer,
  CONSTRAINT pk_sc1_skill_post_counters PRIMARY KEY (skill_term)
)
WITH (
  OIDS=FALSE
);

CREATE TABLE sc1_skill_pairs
(
  id serial NOT NULL,
  primary_term character varying(140),
  secondary_term character varying(140),
  number_of_times integer,
  CONSTRAINT pk_sc1_skill_pairs PRIMARY KEY (id)

)
WITH (
  OIDS=FALSE
);

CREATE TABLE sc1_job_postings_to_skill_pairs
(
  job_file_name character varying(140),
  skill_pair_id integer,
  job_ad_snippet character varying(1500),
  CONSTRAINT pk_sc1_job_postings_to_skill_pairs PRIMARY KEY (job_file_name, skill_pair_id)

)
WITH (
  OIDS=FALSE
);

-- Table: public.sc2_job_listings

CREATE TABLE public.sc2_job_listings
(
  job_file_name character varying(140) NOT NULL,
  date_created date,
  company_name character varying(256),
  job_title character varying(256),
  CONSTRAINT pk_sc2_job_listings PRIMARY KEY (job_file_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sc2_job_listings
  OWNER TO postgres;

-- Table: public.sc2_job_hyp_company_mappings

CREATE TABLE public.sc2_job_hyp_company_mappings
(
  job_file_name character varying(140) NOT NULL,
  hyp_company character varying(256),
  CONSTRAINT pk_sc2_job_hyp_company_mappings PRIMARY KEY (job_file_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sc2_job_hyp_company_mappings
  OWNER TO postgres;


-- Table: public.sc2_job_locations

CREATE TABLE public.sc2_job_locations
(
  job_file_name character varying(140) NOT NULL,
  location character varying(140),
  CONSTRAINT pk_sc2_job_locations PRIMARY KEY (job_file_name)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE public.sc2_job_locations
  OWNER TO postgres;
