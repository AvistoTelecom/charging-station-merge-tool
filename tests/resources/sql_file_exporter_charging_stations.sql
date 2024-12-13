CREATE TABLE charging_stations (
	id int8 NOT NULL PRIMARY KEY,
	geom public.geometry(point, 4326) NULL
);


INSERT INTO charging_stations(id, geom) VALUES(0, 'POINT (-61.72048 15.999102)');

INSERT INTO charging_stations(id, geom) VALUES(1, 'POINT (-61.605293 16.20394)');
