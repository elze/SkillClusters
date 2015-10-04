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
