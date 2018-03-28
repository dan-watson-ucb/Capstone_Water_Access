drop table if exists sierraleone_preds;

create table sierraleone_preds(row_id TEXT, country_name TEXT, water_source TEXT, 
	water_tech TEXT, status_id TEXT, management TEXT, pay TEXT, installer TEXT, 
	install_year TEXT, status TEXT, source TEXT, adm1 TEXT, adm2 TEXT, 
	wpdx_id TEXT, report_date TEXT, country_id TEXT, activity_id TEXT, 
	data_lnk TEXT, orig_lnk TEXT, photo_lnk TEXT, converted TEXT, created TEXT,
	updated TEXT, lat_deg TEXT, lon_deg TEXT, Location TEXT, count TEXT, 
	fecal_coliform_presence TEXT, fecal_coliform_value TEXT, subjective_quality 
	TEXT, new_report_date TEXT, new_install_year TEXT, age_well TEXT, 
	age_well_days TEXT, status_binary_x TEXT, time_since_measurement TEXT,
	time_since_meas_years TEXT, age_well_years TEXT, fuzzy_water_source TEXT,
	fuzzy_water_tech TEXT, cv_predictions TEXT, cv_probabilities TEXT);

\copy sierraleone_preds FROM '/Users/Dan/Desktop/Sierra_Leone_Results_nested_cv.csv'  DELIMITER ',' CSV HEADER;
-- Merges Chandlers prediction output to Alex's population data tables
ALTER TABLE sierraleone_preds ALTER cv_probabilities TYPE double precision USING cv_probabilities::double precision;
ALTER TABLE sierraleone_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists sierraleone_final;

SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.cv_predictions, a.cv_probabilities, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, ((a.cv_probabilities * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years
INTO sierraleone_final
FROM sierraleone_preds a
INNER JOIN sierra_leone_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
WHERE b.one_km_functioning_water_points >0 
;

ALTER TABLE sierraleone_final ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE sierraleone_final ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE sierraleone_final ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE sierraleone_final ALTER cv_predictions type integer USING cv_predictions::integer;
ALTER TABLE sierraleone_final ALTER cv_probabilities TYPE double precision USING cv_probabilities::double precision;
