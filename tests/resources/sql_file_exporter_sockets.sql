CREATE TABLE sockets (
	id varchar NOT NULL PRIMARY KEY,
	geom public.geometry(point, 4326) NULL,
	power_rated float8 NULL,
	number_of_sockets int NULL,
	socket_type_ef bool,
	socket_type_2 bool,
	socket_type_combo_ccs bool,
	socket_type_chademo bool,
	socket_type_autre bool,
	charging_station_id id NOT NULL,
	id_itinerance varchar NULL,
	retrieve_from varchar NOT NULL
);

ALTER TABLE sockets ADD CONSTRAINT fk_sockets_charging_stations FOREIGN KEY (charging_station_id) REFERENCES charging_stations(id);


INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test1', 'POINT (2.3522 48.8566)', 22.0, 1, True, False, False, False, False, 0, 'iti1', 'OSM');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test2', 'POINT (2.3444 48.8554)', 305.0, 2, False, True, False, False, False, 0, 'iti2', 'OSM');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test3', 'POINT (2.3442 48.855)', 3.8, 3, False, False, True, False, False, 0, 'iti3', 'DATA_GOUV');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test4', 'POINT (2.35 48.8555)', 50.0, 4, False, False, False, True, False, 1, 'iti4', 'DATA_GOUV');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test5', 'POINT (2.36 48.842)', 105.0, 5, False, False, False, False, True, 1, 'iti5', 'DATA_GOUV');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test6', 'POINT (2.2945 48.8584)', 200.0, 2, True, False, False, False, False, 1, 'iti6', 'OSM');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test7', 'POINT (2.3376 48.8606)', 150.0, 3, False, True, False, False, False, 1, 'iti7', 'DATA_GOUV');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test8', 'POINT (2.3614 48.866)', 75.0, 1, False, False, True, False, False, 0, 'iti8', 'OSM');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test9', 'POINT (2.2699 48.8848)', 120.0, 4, True, False, False, True, False, 0, 'iti9', 'DATA_GOUV');

INSERT INTO sockets(id, geom, power_rated, number_of_sockets, socket_type_ef, socket_type_2, socket_type_combo_ccs, socket_type_chademo, socket_type_autre, charging_station_id, id_itinerance, retrieve_from) VALUES('test10', 'POINT (2.33 48.8738)', 60.0, 2, False, True, False, False, True, 1, 'iti10', 'OSM');
