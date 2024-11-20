CREATE TABLE charging_stations (
	id int8 NOT NULL,
	geom public.geometry(point, 4326) NULL
	CONSTRAINT pk_charging_stations PRIMARY KEY (id)
);


INSERT INTO charging_stations(id, geom) VALUES(0, 'POINT (-61.72048 15.999102)');

INSERT INTO charging_stations(id, geom) VALUES(1, 'POINT (-61.605293 16.20394)');
