drop table if exists swazi_preds;

create table swazi_preds(row_id TEXT,country_name TEXT,water_source TEXT, water_tech TEXT,
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

\copy swazi_preds FROM '/Users/Dan/Desktop/prediction_files/Swaziland_w_outyear_predictions.csv'  DELIMITER ',' CSV HEADER;
\copy swazi_preds FROM '/Users/Dan/Desktop/swaziland_with_preds.csv'  DELIMITER ',' CSV HEADER;
\copy water_django FROM '/Users/Dan/Desktop/WPD.csv'  DELIMITER ',' QUOTE '"' CSV HEADER;
ALTER TABLE water_django ALTER lat_deg TYPE double precision USING lat_deg::double precision;
ALTER TABLE water_django ALTER lon_deg TYPE double precision USING lon_deg::double precision;