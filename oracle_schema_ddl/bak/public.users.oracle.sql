--
-- Oracle database dump
--

CREATE TABLE users (
    user_id NUMBER NOT NULL,
    username VARCHAR2(50) NOT NULL,
    email VARCHAR2(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE users_seq
    START WITH 1
    INCREMENT BY 1
    NOMINVALUE
    NOMAXVALUE
    CACHE 1;

ALTER TABLE users MODIFY user_id DEFAULT users_seq.nextval;

ALTER TABLE users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);

ALTER TABLE users
    ADD CONSTRAINT users_username_key UNIQUE (username);

CREATE INDEX idx_users_email ON users (email);