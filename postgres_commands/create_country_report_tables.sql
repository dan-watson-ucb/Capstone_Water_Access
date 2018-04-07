--create country_summary table
drop table if exists country_summary;

CREATE TABLE country_summary(id INTEGER,measure TEXT,values DOUBLE PRECISION,country TEXT);

\copy country_summary FROM '/Users/Dan/Desktop/country_report_files/summary_results_by_country.csv'  DELIMITER ',' CSV HEADER;

------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------
--create country_status_watertech table
drop table if exists country_mostimportant;

CREATE TABLE country_mostimportant(id INTEGER,
country TEXT,most_important_feature TEXT,feature_value DOUBLE PRECISION, num_functioning DOUBLE PRECISION,
num_not_functioning DOUBLE PRECISION, percentage_broken DOUBLE PRECISION);

\copy country_mostimportant FROM '/Users/Dan/Desktop/country_report_files/country_waterpoint_status_by_most_important_feature.csv'  DELIMITER ',' CSV HEADER;

------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------
-- create country_status_watertech

drop table if exists country_status_watertech;

CREATE TABLE country_status_watertech(id INTEGER,fuzzy_water_tech TEXT , num_functioning DOUBLE PRECISION,
num_not_functioning DOUBLE PRECISION, percentage_broken DOUBLE PRECISION,country TEXT);

\copy country_status_watertech FROM '/Users/Dan/Desktop/country_report_files/country_waterpoint_status_by_fuzzy_water_tech.csv'  DELIMITER ',' CSV HEADER;

------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------
-- create country_status_watersource
drop table if exists country_status_watersource;

CREATE TABLE country_status_watersource(id INTEGER,fuzzy_water_source TEXT, num_functioning DOUBLE PRECISION,
num_not_functioning DOUBLE PRECISION,percentage_broken DOUBLE PRECISION,country TEXT);

\copy country_status_watersource FROM '/Users/Dan/Desktop/country_report_files/country_waterpoint_status_by_fuzzy_water_source.csv'  DELIMITER ',' CSV HEADER;