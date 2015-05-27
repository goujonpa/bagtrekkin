-- NEED TO CREATE INDEXES

DROP TABLE IF EXISTS compagnies;
CREATE TABLE IF NOT EXISTS compagnies (
  id_company SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
);

CREATE INDEX compagnies_idx_1 on compagnies(id_company)

INSERT INTO compagnies (id_company, name) VALUES
(NULL, 'TAP'),
(NULL, 'TAM'),
(NULL, 'British Airways');

DROP TABLE IF EXISTS employees;
CREATE TABLE IF NOT EXISTS employees (
  id_employee SERIAL PRIMARY KEY,
  cpf varchar(255) UNIQUE NOT NULL,
  function varchar(255) NOT NULL,
  name varchar(255) NOT NULL,
  password varchar(255) NOT NULL,
  status varchar(255) NOT NULL,
  token varchar(255) NOT NULL,
  id_company int(11) NOT NULL,
  district varchar(255) NOT NULL,
);

CREATE INDEX employees_idx_1 on employees(id_employee)
CREATE INDEX employees_idx_2 on employees(id_company)
CREATE INDEX employees_idx_3 on employees(cpf)

INSERT INTO employees (id_employee, cpf, function, name, password, status, token, id_company, district) VALUES
(NULL, '710.831.318-68', 'check-in', 'Arthur Raimbaud', '0a75f6cb015fd589b71b757f6cf2f5e9', 'active', 'f4cfbd4d244e690924bcef7ca171a665', 1, 'Paris, France - Orly'),
(NULL, '710.831.320-25', 'check-in', 'Pierre Verger', '0a75f6cb015fd589b71b757f6cf2f5e9', 'active', '5011b7b19a1908f080bef30c406909d4', 2, 'Paris, France - Orly');

DROP TABLE IF EXISTS etickets;
CREATE TABLE IF NOT EXISTS etickets (
  id_eticket SERIAL PRIMARY KEY,
  ticket_number varchar(255) UNIQUE NOT NULL,
  id_passenger int(11) NOT NULL,
  summary varchar(255) NOT NULL,
);

CREATE INDEX etickets_idx_1 on etickets(id_eticket)
CREATE INDEX etickets_idx_2 on etickets(ticket_number)
CREATE INDEX etickets_idx_3 on etickets(id_passenger)

INSERT INTO etickets (id_eticket, ticket_number, id_passenger, summary) VALUES
(NULL, '047-6535417938', 1, 'Paris - Recife'),
(NULL, '047-2159354990', 2, 'Paris - Recife');


DROP TABLE IF EXISTS flights;
CREATE TABLE IF NOT EXISTS flights (
  id_flight SERIAL PRIMARY KEY,
  id_eticket int(11) NOT NULL,
  duration time NOT NULL,
  aircraft varchar(255) NOT NULL,
  airline varchar(255) NOT NULL,
  departure_loc varchar(255) NOT NULL,
  departure_time time NOT NULL,
  arrival_loc varchar(255) NOT NULL,
  arrival_time time NOT NULL,
  id_company int(11) NOT NULL,
  flight_date date NOT NULL,
);

CREATE INDEX flights_idx_1 on flights(id_flight)
CREATE INDEX flights_idx_2 on flights(id_company)
CREATE INDEX flights_idx_3 on flights(id_eticket)


INSERT INTO flights (id_flight, id_eticket, duration, aircraft, airline, departure_loc, departure_time, arrival_loc, arrival_time, id_company, flight_date) VALUES
(NULL, 1, '02:25:00', 'Airbus Industrie A319', 'TP421', 'Paris, France - Orly, terminal W', '13:15:00', 'Lisbon, Portugal - Airport, terminal 1', '14:40:00', 1, '2015-02-25'),
(NULL, 1, '07:45:00', 'Airbus Industrie A330-200', 'TP015', 'Lisbon, Portugal - Airport, terminal 1', '16:35:00', 'Recife, Brazil - Guararapes International', '21:20:00', 1, '2015-02-25'),
(NULL, 2, '07:45:00', 'Airbus Industrie A330-200', 'TP015', 'Lisbon, Portugal - Airport, terminal 1', '16:35:00', 'Recife, Brazil - Guararapes International', '21:20:00', 1, '2015-02-19'),
(NULL, 2, '02:25:00', 'Airbus Industrie A319', 'TP421', 'Paris, France - Orly, terminal W', '13:15:00', 'Lisbon, Portugal - Airport, terminal 1', '14:40:00', 1, '2015-02-19');


DROP TABLE IF EXISTS logs;
CREATE TABLE IF NOT EXISTS logs (
  id_log SERIAL PRIMARY KEY,
  horodator datetime NOT NULL,
  id_employee int(11) NOT NULL,
  id_luggage int(11) NOT NULL,
  id_flight int(11) NOT NULL,
  localisation varchar(255) DEFAULT NULL,
);

CREATE INDEX logs_idx_1 on logs(id_log)
CREATE INDEX logs_idx_2 on logs(id_employee)
CREATE INDEX logs_idx_3 on logs(id_luggage)
CREATE INDEX logs_idx_1 on logs(id_flight)

INSERT INTO logs (id_log, horodator, id_employee, id_luggage, id_flight, localisation) VALUES
(NULL, '2015-02-19 12:00:00', 1, 1, 3, 'Paris, France - Orly, terminal W'),
(NULL, '2015-02-20 12:01:00', 1, 2, 3, 'Paris, France - Orly, terminal W'),
(NULL, '2015-02-25 12:49:00', 2, 5, 1, 'Paris, France - Orly, terminal W'),
(NULL, '2015-02-25 12:51:00', 2, 6, 1, 'Paris, France - Orly, terminal W');

DROP TABLE IF EXISTS luggages;
CREATE TABLE IF NOT EXISTS luggages (
  id_luggage SERIAL PRIMARY KEY,
  material_number varchar(64) UNIQUE NOT NULL,
  id_passenger int(11) NOT NULL,
);

CREATE INDEX luggages_idx_1 on luggages(id_luggage)
CREATE INDEX luggages_idx_2 on luggages(material_number)
CREATE INDEX luggages_idx_3 on luggages(id_passenger)

INSERT INTO luggages (id_luggage, material_number, id_passenger) VALUES
(NULL, 'A1E637F492D938', 1),
(NULL, '21474FA83EC647', 1),
(NULL, 'EB56834CA78203', 2),
(NULL, '93AE748291FB03', 2);

DROP TABLE IF EXISTS passengers;
CREATE TABLE IF NOT EXISTS passengers (
  id_user SERIAL PRIMARY KEY,
  email varchar(255) NOT NULL,
  first_name varchar(255) NOT NULL,
  last_name varchar(255) NOT NULL,
  full_name varchar(255) NOT NULL,
  pnr varchar(255) UNIQUE NOT NULL,
  tel varchar(255) NOT NULL,
);

CREATE INDEX passengers_idx_1 on luggages(id_user)
CREATE INDEX passengers_idx_2 on luggages(pnr)


INSERT INTO passengers (id_user, email, first_name, last_name, full_name, pnr, tel) VALUES
(NULL, 'hr2@cin.ufpe.br', 'Hugo', 'Rodde', 'Hugo Rodde', 'x9jjb5', '+558147802343'),
(NULL, 'pjmg@cin.ufpe.br', 'Paul Jean Michel', 'Goujon', 'Paul Jean Michel Goujon', 'ysvi82', '+558189328925');

ALTER TABLE employees
  ADD CONSTRAINT employees_fk_1 FOREIGN KEY (id_company) REFERENCES compagnies (id_company);

ALTER TABLE etickets
  ADD CONSTRAINT etickets_fk_1 FOREIGN KEY (id_passenger) REFERENCES passengers (id_user);

ALTER TABLE flights
  ADD CONSTRAINT flights_fk_2 FOREIGN KEY (id_eticket) REFERENCES etickets (id_eticket),
  ADD CONSTRAINT flights_fk_1 FOREIGN KEY (id_company) REFERENCES compagnies (id_company);

ALTER TABLE logs
  ADD CONSTRAINT logs_fk_1 FOREIGN KEY (id_employee) REFERENCES employees (id_employee),
  ADD CONSTRAINT logs_fk_2 FOREIGN KEY (id_luggage) REFERENCES luggages (id_luggage),
  ADD CONSTRAINT logs_fk_3 FOREIGN KEY (id_flight) REFERENCES flights (id_flight);

ALTER TABLE luggages
  ADD CONSTRAINT luggages_fk_1 FOREIGN KEY (id_passenger) REFERENCES passengers (id_user);
