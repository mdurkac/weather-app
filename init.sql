drop table locations;
CREATE TABLE IF NOT EXISTS locations (
    id INTEGER PRIMARY KEY,
    name TEXT,
    country TEXT,
    country_code TEXT,
    latitude FLOAT,
    longitude FLOAT 
);

INSERT INTO locations (id, name, country, country_code, latitude,longitude) VALUES 
    (2950159,'Berlin', 'Germany','de', 52.52437, 13.41053),
    (3078610, 'Brno', 'Czechia','cz', 49.19522, 16.60796),
    (724443, 'Košice', 'Slovakia', 'sk', 48.71395, 21.25808);

select * FROM locations;