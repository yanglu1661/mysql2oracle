CREATE TABLE roles (
  role_id NUMBER GENERATED ALWAYS AS IDENTITY,
  role_name VARCHAR2(50) NOT NULL,
  PRIMARY KEY (role_id),
  UNIQUE (role_name)
);