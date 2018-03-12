-- Change text fields to precisions before pulling model in django
ALTER TABLE swazi_mvp ALTER lat_deg  TYPE double precision USING lat_deg::double precision;
ALTER TABLE swazi_mvp ALTER lon_deg  TYPE double precision USING lon_deg:: double precision;
ALTER TABLE swazi_mvp ALTER predicted_class type integer USING predicted_class::integer;
ALTER TABLE swazi_mvp ALTER probability TYPE double precision USING probability::double precision;



