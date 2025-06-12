CREATE TABLE user_roles (
  user_id NUMBER NOT NULL,
  role_id NUMBER NOT NULL,
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id,role_id)
);

CREATE INDEX role_id ON user_roles (role_id);