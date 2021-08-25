SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+02:00";


CREATE TABLE appointments (
  appointment_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  appointment_type_id int(11) NOT NULL,
  room_id int(11) NOT NULL,
  begins_at datetime DEFAULT NOW(),
  created_at datetime DEFAULT NOW(),
  updated_at datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE appointment_crons (
  appointment_type_id int(11) NOT NULL,
  cron_id int(11) NOT NULL,
  PRIMARY KEY (appointment_type_id, cron_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE appointment_roles (
  appointment_type_id int(11) NOT NULL,
  role_id int(11) NOT NULL,
  PRIMARY KEY (appointment_type_id, role_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE appointment_rooms (
  appointment_type_id int(11) NOT NULL,
  room_id int(11) NOT NULL,
  PRIMARY KEY (appointment_type_id, room_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE appointment_types (
  appointment_type_id int(11) PRIMARY KEY AUTO_INCREMENT,
  title varchar(254) NOT NULL UNIQUE,
  description text NOT NULL,
  duration_minutes int(11) DEFAULT 60,
  max_participants int(11) DEFAULT 10,
  created_at datetime DEFAULT NOW(),
  updated_at datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE assignments (
  appointment_id bigint(20) NOT NULL,
  assignee_id bigint(20) NOT NULL,
  assigned_at datetime DEFAULT NOW(),
  refused_at datetime DEFAULT NULL,
  changed_at datetime DEFAULT NULL,
  hrate_factor int(11) DEFAULT 1,
  work_factor int(11) DEFAULT 1,
  PRIMARY KEY (appointment_id, assignee_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE availabilities (
  staff_id bigint(20) NOT NULL,
  cron_id int(11) NOT NULL,
  priority int(11) DEFAULT 1,
  created_at datetime DEFAULT NOW(),
  updated_at datetime DEFAULT NULL,
  PRIMARY KEY (staff_id, cron_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE bookings (
  member_id bigint(20) NOT NULL,
  appointment_id bigint(20) NOT NULL,
  booked_at datetime DEFAULT NOW(),
  cancelled_at datetime DEFAULT NULL,
  PRIMARY KEY (member_id, appointment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE crons (
  cron_id int(11) PRIMARY KEY AUTO_INCREMENT,
  schedule varchar(254) DEFAULT '* * * * *' UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE invoices (
  invoice_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  membership_id bigint(20) NOT NULL,
  paydue_at datetime DEFAULT NOW()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE members (
  member_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  email varchar(254) NOT NULL UNIQUE,
  member_name varchar(254) NOT NULL UNIQUE,
  password varchar(254) NOT NULL,
  created_at datetime DEFAULT NOW(),
  updated_at datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE memberships (
  membership_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  member_id bigint(20) NOT NULL,
  supscription_id int(11) NOT NULL,
  started_at datetime DEFAULT NOW(),
  ended_at datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE payrolls (
  payroll_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  member_id bigint(20) NOT NULL,
  for_from datetime DEFAULT NOW(),
  for_until datetime DEFAULT NOW()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE periods (
  period_id int(11) PRIMARY KEY AUTO_INCREMENT,
  period_name varchar(254) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE prices (
  price_id int(11) PRIMARY KEY AUTO_INCREMENT,
  period_id int(11) NOT NULL,
  promotion text,
  amount_euro decimal(10,2) NOT NULL,
  valid_from datetime DEFAULT NOW(),
  valid_until datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE roles (
  role_id int(11) PRIMARY KEY AUTO_INCREMENT,
  title varchar(254) NOT NULL UNIQUE,
  description text,
  hrate_euro decimal(10,2) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE rooms (
  room_id int(11) PRIMARY KEY AUTO_INCREMENT,
  title varchar(254) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE specials (
  special_id int(11) PRIMARY KEY AUTO_INCREMENT,
  member_id bigint(20) NOT NULL,
  conditions text,
  price_factor int(11) DEFAULT 1,
  hrate_factor int(11) DEFAULT 1,
  valid_from datetime DEFAULT NOW(),
  valid_until datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE staff_roles (
  staff_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  member_id bigint(20) NOT NULL,
  role_id int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE supscriptions (
  supscription_id int(11) PRIMARY KEY AUTO_INCREMENT,
  price_id int(11) NOT NULL,
  title varchar(254) NOT NULL UNIQUE,
  description text NOT NULL,
  minimum_days int(11) DEFAULT 1,
  maximum_days int(11) DEFAULT NULL,
  created_at datetime DEFAULT NOW(),
  updated_at datetime DEFAULT NULL,
  is_active tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE transactions (
  transaction_id bigint(20) PRIMARY KEY AUTO_INCREMENT,
  invoice_id int(11) DEFAULT NULL,
  payroll_id int(11) DEFAULT NULL,
  comments text,
  amount_euro decimal(10,2) NOT NULL,
  occured_at datetime DEFAULT NOW()
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


ALTER TABLE appointment_crons
  ADD CONSTRAINT appointment_crons_fk1 FOREIGN KEY (appointment_type_id) REFERENCES appointment_types(appointment_type_id),
  ADD CONSTRAINT appointment_crons_fk2 FOREIGN KEY (cron_id) REFERENCES crons(cron_id);

ALTER TABLE appointment_roles
  ADD CONSTRAINT appointment_roles_fk1 FOREIGN KEY (appointment_type_id) REFERENCES appointment_types(appointment_type_id),
  ADD CONSTRAINT appointment_roles_fk2 FOREIGN KEY (role_id) REFERENCES roles(role_id);

ALTER TABLE appointment_rooms
  ADD CONSTRAINT appointment_rooms_fk1 FOREIGN KEY (appointment_type_id) REFERENCES appointment_types(appointment_type_id),
  ADD CONSTRAINT appointment_rooms_fk2 FOREIGN KEY (room_id) REFERENCES rooms(room_id);

ALTER TABLE appointments
  ADD CONSTRAINT appointments_fk1 FOREIGN KEY (appointment_type_id) REFERENCES appointment_types(appointment_type_id),
  ADD CONSTRAINT appointments_fk2 FOREIGN KEY (room_id) REFERENCES rooms(room_id);

ALTER TABLE assignments
  ADD CONSTRAINT assignments_fk1 FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id),
  ADD CONSTRAINT assignments_fk2 FOREIGN KEY (assignee_id) REFERENCES staff_roles(staff_id);

ALTER TABLE availabilities
  ADD CONSTRAINT availabilities_fk1 FOREIGN KEY (staff_id) REFERENCES staff_roles(staff_id),
  ADD CONSTRAINT availabilities_fk2 FOREIGN KEY (cron_id) REFERENCES crons(cron_id);

ALTER TABLE bookings
  ADD CONSTRAINT bookings_fk1 FOREIGN KEY (member_id) REFERENCES members(member_id),
  ADD CONSTRAINT bookings_fk2 FOREIGN KEY (appointment_id) REFERENCES appointments(appointment_id);

ALTER TABLE invoices
  ADD CONSTRAINT invoices_fk1 FOREIGN KEY (membership_id) REFERENCES memberships(membership_id);

ALTER TABLE memberships
  ADD CONSTRAINT memberships_fk1 FOREIGN KEY (member_id) REFERENCES members(member_id),
  ADD CONSTRAINT memberships_fk2 FOREIGN KEY (supscription_id) REFERENCES supscriptions(supscription_id);

ALTER TABLE payrolls
  ADD CONSTRAINT payrolls_fk1 FOREIGN KEY (member_id) REFERENCES members(member_id);

ALTER TABLE prices
  ADD CONSTRAINT prices_fk1 FOREIGN KEY (period_id) REFERENCES periods(period_id);

ALTER TABLE specials
  ADD CONSTRAINT specials_fk1 FOREIGN KEY (member_id) REFERENCES members(member_id);

ALTER TABLE staff_roles
  ADD CONSTRAINT staff_roles_fk1 FOREIGN KEY (member_id) REFERENCES members(member_id),
  ADD CONSTRAINT staff_roles_fk2 FOREIGN KEY (role_id) REFERENCES roles(role_id);

ALTER TABLE supscriptions
  ADD CONSTRAINT supscriptions_fk1 FOREIGN KEY (price_id) REFERENCES prices(price_id);


CREATE TRIGGER lcase_insert BEFORE INSERT ON members FOR EACH ROW
  SET NEW.email = LOWER(NEW.email);

CREATE TRIGGER lcase_update BEFORE UPDATE ON members FOR EACH ROW
  SET NEW.email = LOWER(NEW.email);


INSERT INTO periods (period_name) VALUES ('hour');
INSERT INTO periods (period_name) VALUES ('week');
INSERT INTO periods (period_name) VALUES ('month');


COMMIT;