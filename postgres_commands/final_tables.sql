--Code to create the final tables in postgres
-- Afghanistan

drop table if exists afghanistan_preds;

create table afghanistan_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy afghanistan_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/afghanistan_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE afghanistan_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE afghanistan_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists afghanistan_final;
drop table if exists afghanistan_temp;

CREATE TEMPORARY TABLE afghanistan_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM afghanistan_preds a
INNER JOIN afghanistan_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE afghanistan_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE afghanistan_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE afghanistan_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE afghanistan_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE afghanistan_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE afghanistan_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE afghanistan_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE afghanistan_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE afghanistan_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE afghanistan_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE afghanistan_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE afghanistan_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM afghanistan_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- India
drop table if exists india_preds;

create table india_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy india_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/india_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE india_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE india_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists india_final;
drop table if exists india_temp;

CREATE TEMPORARY TABLE india_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM india_preds a
INNER JOIN india_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE india_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE india_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE india_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE india_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE india_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE india_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE india_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE india_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE india_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE india_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE india_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE india_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM india_temp
-------------------------
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- Kenya

drop table if exists kenya_preds;

create table kenya_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy kenya_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/kenya_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE kenya_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE kenya_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists kenya_final;
drop table if exists kenya_temp;

CREATE TEMPORARY TABLE kenya_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM kenya_preds a
INNER JOIN kenya_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE kenya_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE kenya_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE kenya_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE kenya_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE kenya_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE kenya_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE kenya_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE kenya_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE kenya_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE kenya_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE kenya_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE kenya_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM kenya_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- Liberia

drop table if exists liberia_preds;

create table liberia_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy liberia_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/liberia_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE liberia_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE liberia_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists liberia_final;
drop table if exists liberia_temp;

CREATE TEMPORARY TABLE liberia_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM liberia_preds a
INNER JOIN liberia_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE liberia_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE liberia_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE liberia_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE liberia_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE liberia_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE liberia_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE liberia_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE liberia_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE liberia_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE liberia_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE liberia_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE liberia_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM liberia_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------

-- Malawi

drop table if exists malawi_preds;
drop table if exists malawai_preds;

create table malawi_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy malawi_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/malawi_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE malawi_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE malawi_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists malawi_final;
drop table if exists malawi_temp;

CREATE TEMPORARY TABLE malawi_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM malawi_preds a
INNER JOIN malawi_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE malawi_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE malawi_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE malawi_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE malawi_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE malawi_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE malawi_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE malawi_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE malawi_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE malawi_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE malawi_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE malawi_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE malawi_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM malawi_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- Sierra Leone

drop table if exists sierraleone_preds;

create table sierraleone_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy sierraleone_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/sierra_leone_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE sierraleone_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE sierraleone_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists sierraleone_final;
drop table if exists sierraleone_temp;

CREATE TEMPORARY TABLE sierraleone_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM sierraleone_preds a
INNER JOIN sierra_leone_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE sierraleone_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE sierraleone_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE sierraleone_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE sierraleone_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE sierraleone_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE sierraleone_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE sierraleone_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE sierraleone_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE sierraleone_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE sierraleone_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE sierraleone_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE sierraleone_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM sierraleone_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------

-- South Sudan

drop table if exists southsudan_preds;

create table southsudan_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy southsudan_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/south_sudan_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE southsudan_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE southsudan_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists southsudan_final;
drop table if exists southsudan_temp;

CREATE TEMPORARY TABLE southsudan_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM southsudan_preds a
INNER JOIN south_sudan_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE southsudan_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE southsudan_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE southsudan_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE southsudan_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE southsudan_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE southsudan_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE southsudan_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE southsudan_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE southsudan_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE southsudan_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE southsudan_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE southsudan_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM southsudan_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------

-- Swaziland
drop table if exists swazi_preds;

create table swazi_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy swazi_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/swaziland_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE swazi_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE swazi_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists swazi_final;
drop table if exists swazi_temp;

CREATE TEMPORARY TABLE swazi_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM swazi_preds a
INNER JOIN swaziland_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE swazi_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE swazi_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE swazi_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE swazi_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE swazi_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE swazi_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE swazi_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE swazi_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE swazi_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE swazi_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE swazi_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE swazi_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM swazi_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- Uganda

drop table if exists uganda_preds;

create table uganda_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy uganda_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/uganda_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE uganda_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE uganda_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists uganda_final;
drop table if exists uganda_temp;

CREATE TEMPORARY TABLE uganda_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM uganda_preds a
INNER JOIN uganda_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE uganda_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE uganda_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE uganda_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE uganda_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE uganda_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE uganda_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE uganda_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE uganda_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE uganda_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE uganda_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE uganda_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE uganda_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM uganda_temp

--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------
-- Zimbabwe

drop table if exists zimbabwe_preds;

create table zimbabwe_preds(country_name TEXT,water_source TEXT, water_tech TEXT,
	status_id TEXT,status_0_yes TEXT,management TEXT,pay TEXT,installer TEXT,
	install_year TEXT,status TEXT,source TEXT,adm1 TEXT,adm2 TEXT,wpdx_id TEXT,
	report_date TEXT,country_id TEXT,activity_id TEXT,data_lnk TEXT,orig_lnk TEXT,
	photo_lnk TEXT,converted TEXT,created TEXT,updated TEXT,lat_deg TEXT,lon_deg TEXT,Location TEXT,
	Count TEXT,fecal_coliform_presence TEXT,fecal_coliform_value TEXT,subjective_quality TEXT,
	new_report_date TEXT,new_install_year TEXT,age_well TEXT,age_well_days TEXT, 
	status_binary TEXT,time_since_measurement TEXT,time_since_meas_years TEXT,
	age_well_years TEXT,fuzzy_water_source TEXT,fuzzy_water_tech TEXT,today_preds TEXT,
	today_predprob TEXT,one_year_preds TEXT,one_year_predprob TEXT,three_year_preds TEXT,
	three_year_predprob TEXT,five_year_preds TEXT,five_year_predprob TEXT);

-- Load data from local csv
\copy zimbabwe_preds FROM '/Users/Dan/Desktop/prediction_files/deduplicated/zimbabwe_dedup.csv'  DELIMITER ',' CSV HEADER;

-- Merge Swazi_preds with population data
ALTER TABLE zimbabwe_preds ALTER today_predprob TYPE double precision USING today_predprob::double precision;
ALTER TABLE zimbabwe_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists zimbabwe_final;
drop table if exists zimbabwe_temp;

CREATE TEMPORARY TABLE zimbabwe_temp AS
SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.today_preds, a.today_predprob, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, b.district, b.sub_district, 
((a.today_predprob * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years, a.one_year_preds, a.one_year_predprob, a.three_year_preds,
a.three_year_predprob, a.five_year_preds, a.five_year_predprob
FROM zimbabwe_preds a
INNER JOIN zimbabwe_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >=0
;

ALTER TABLE zimbabwe_temp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE zimbabwe_temp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE zimbabwe_temp ALTER today_preds type integer USING today_preds::integer;
ALTER TABLE zimbabwe_temp ALTER today_predprob TYPE double precision USING today_predprob::double precision;
-- ALTER TABLE sierraleone_final ALTER install_year TYPE float(1) USING install_year::float(1); Doesn't work because '__missing__'
ALTER TABLE zimbabwe_temp ALTER time_since_meas_years TYPE double precision using time_since_meas_years::double precision;
ALTER TABLE zimbabwe_temp ALTER one_year_preds TYPE float(1) USING one_year_preds::float(1);
ALTER TABLE zimbabwe_temp ALTER one_year_predprob TYPE double precision USING one_year_predprob::double precision;
ALTER TABLE zimbabwe_temp ALTER three_year_preds TYPE float(1) USING three_year_preds::float(1);
ALTER TABLE zimbabwe_temp ALTER three_year_predprob TYPE double precision USING three_year_predprob::double precision;
ALTER TABLE zimbabwe_temp ALTER five_year_preds TYPE float(1) USING five_year_preds::float(1);
ALTER TABLE zimbabwe_temp ALTER five_year_predprob TYPE double precision USING five_year_predprob::double precision;

CREATE TABLE zimbabwe_final AS
SELECT  country_name, water_source, water_tech, status_id, install_year, 
lat_deg, lon_deg, time_since_meas_years, management, fuzzy_water_source, fuzzy_water_tech,
today_preds, today_predprob, wpdx_id, one_km_population, one_km_total_water_points,
one_km_functioning_water_points, key, district, sub_district, impact_score,
age_well_years, one_year_preds, one_year_predprob, three_year_preds,
three_year_predprob, five_year_preds, five_year_predprob, CASE WHEN percent_rank() OVER (ORDER BY impact_score desc) <=.33 THEN 'High'
WHEN percent_rank() OVER (ORDER BY impact_score desc) > .33 AND percent_rank() OVER (ORDER BY impact_score desc) <= .66 THEN 'Medium'
ELSE 'Low' end as impact_text
FROM zimbabwe_temp
--------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------






------------------------------------------------------------------------------------------------------------
-------------UNION- RUN AFTER TABLES MADE
------------------------------------------------------------------------------------------------------------
drop table if exists final_all;
drop table if exists final;
drop table if exists final_two;

CREATE TEMPORARY TABLE final
AS
SELECT * FROM afghanistan_final
	UNION
SELECT * FROM kenya_final
	UNION
SELECT * FROM india_final
	UNION
SELECT * FROM liberia_final
	UNION
SELECT * FROM malawi_final
	UNION
SELECT * FROM sierraleone_final
    UNION
SELECT * FROM southsudan_final
	UNION
SELECT * FROM swazi_final
	UNION
SELECT * FROM uganda_final
	UNION
SELECT * FROM zimbabwe_final;

SELECT a.*, b.pred as pred_1_year, b.text_output as one_year_preds_text
into TEMPORARY TABLE final_two
FROM final a
INNER JOIN preds_text b
ON a.one_year_preds = b.pred;

SELECT a.*, b.pred as pred_today, b.text_output as today_preds_text
into final_all
from final_two a
INNER JOIN preds_text b
ON a.today_preds =b.pred; 

SELECT * FROM final_all limit 10;

ALTER TABLE final_all
DROP COLUMN pred_1_year;

ALTER TABLE final_all
DROP COLUMN pred_today;


--- Create menu table
drop table if exists menu_table;
SELECT distinct country_name, district, sub_district, status_id, fuzzy_water_tech, 
fuzzy_water_source, management, today_preds_text,one_year_preds_text, impact_text 
into menu_table
from final_all;




