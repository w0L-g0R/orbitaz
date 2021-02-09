Create Table commodity_product(
	id_cp SERIAL PRIMARY KEY,
	commodity VARCHAR (100) NOT NULL,
	product VARCHAR (100),
	vat boolean not null,	
	source VARCHAR (300) NOT NULL,
	start_time DATE NOT NULL,
	granularity Text NOT NULL
);


Create Table price(
	id_p SERIAL PRIMARY KEY,
	"value" float NOT NULL,
	"date" timestamp without time zone NOT NULL,
	traded_volume INTEGER,
	counter_update INTEGER NOT NULL,
	id_cp INTEGER NOT NULL REFERENCES Commodity_product(id_cp)
);
	

Create Table point_of_origin (
	id_po SERIAL PRIMARY KEY,
	country VARCHAR (75) NOT NULL,
	country_acronym VARCHAR (10) NOT NULL,
	eu BOOLEAN
);


Create Table unit (
	id_u SERIAL PRIMARY KEY,
	currency VARCHAR(100) NOT NULL,
	currency_acronym VARCHAR(5) NOT NULL,
	measure VARCHAR(100) NOT NULL,
	measure_acronym VARCHAR(10) NOT NULL

);


Create Table "index" (
	id_i SERIAL PRIMARY KEY,
	indexname VARCHAR(100) NOT NULL,
	start_time DATE NOT NULL,
	base_year INTEGER NOT NULL,
	granularity VARCHAR(20) NOT NULL
);


Create Table index_value (
	id_iv SERIAL PRIMARY Key,
	"value" float NOT NULL,	
	"date" DATE NOT NULL,
	id_i INTEGER NOT NULL REFERENCES "index"(id_i)
);

/* Auflösung n:m Beziehung in 1:n beziehung*/

Create Table commodity_point_of_origin (
	id SERIAL PRIMARY KEY,
	id_cp INTEGER NOT NULL REFERENCES commodity_product(id_cp),
	id_po INTEGER NOT NULL REFERENCES point_of_origin(id_po)
);

/* Auflösung n:m Beziehung in 1:n beziehung*/

Create Table commodity_unit (
	id SERIAL PRIMARY KEY,
	id_cp INTEGER NOT NULL REFERENCES commodity_product(id_cp),
	id_u INTEGER NOT NULL REFERENCES unit(id_u)
);

/* Auflösung n:m Beziehung in 1:n beziehung*/

Create Table index_point_of_origin (
	id SERIAL PRIMARY KEY,
	id_i INTEGER NOT NULL REFERENCES "index"(id_i),
	id_po INTEGER NOT NULL REFERENCES  point_of_origin(id_po)
);

Create Table contractual_partner (
	id_copa SERIAL PRIMARY KEY,
	gender VARCHAR (1) NOT NULL,
	first_name VARCHAR (30) NOT NULL,
	last_name varchar (30) NOT NULL,
	company_name varchar (30) NOT NULL,
	address varchar (50) NOT NULL,
	telefon varchar (15),
	email varchar (30) NOT NULL,
	active_contract BOOLEAN NOT NULL,
	data_access BOOLEAN NOT NULL
);