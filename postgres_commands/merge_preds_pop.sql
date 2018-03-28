-- Merges Chandlers prediction output to Alex's population data tables
ALTER TABLE swazi_preds ALTER probability TYPE double precision USING probability::double precision;
ALTER TABLE swazi_preds ALTER age_well_years TYPE double precision USING age_well_years::double precision;

drop table if exists swazi_mvp;

SELECT a.country_name, a.water_source, a.water_tech, a.status_id, a.install_year, 
a.lat_deg, a.lon_deg, a.time_since_meas_years, a.management, a.fuzzy_water_source, a.fuzzy_water_tech,
a.predicted_class, a.probability, a.wpdx_id, b.one_km_population, b.one_km_total_water_points,
b.one_km_functioning_water_points, b.key, ((a.probability * b.one_km_population) /(1+b.one_km_functioning_water_points)) as impact_score,
a.age_well_years
INTO swazi_mvp
FROM swazi_preds a
INNER JOIN swaz_water_and_population b
ON cast(substring(a."wpdx_id" from 6 for 12) as int) = b.key
;

ALTER TABLE swazi_mvp ADD COLUMN id SERIAL PRIMARY KEY;
ALTER TABLE swazi_mvp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE swazi_mvp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE swazi_mvp ALTER predicted_class type integer USING predicted_class::integer;
ALTER TABLE swazi_mvp ALTER probability TYPE double precision USING probability::double precision;