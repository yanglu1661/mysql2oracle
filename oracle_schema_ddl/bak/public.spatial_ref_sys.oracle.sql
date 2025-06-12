-- Oracle database dump

SET DEFINE OFF;

--
-- Name: users; Type: TABLE; 
--

CREATE TABLE users (
    id NUMBER GENERATED ALWAYS AS IDENTITY,
    username VARCHAR2(50) NOT NULL,
    email VARCHAR2(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP,
    is_active NUMBER(1) DEFAULT 1 NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_username_key UNIQUE (username),
    CONSTRAINT users_email_key UNIQUE (email)
);

COMMENT ON TABLE users IS 'System users table';
COMMENT ON COLUMN users.id IS 'Primary key';
COMMENT ON COLUMN users.username IS 'Unique username';
COMMENT ON COLUMN users.email IS 'User email address';
COMMENT ON COLUMN users.created_at IS 'Record creation timestamp';
COMMENT ON COLUMN users.updated_at IS 'Record last update timestamp';
COMMENT ON COLUMN users.is_active IS 'User active status (1=active, 0=inactive)';

CREATE INDEX users_is_active_idx ON users (is_active);
CREATE INDEX users_created_at_idx ON users (created_at);