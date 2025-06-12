CREATE VIEW view_user_roles AS 
SELECT u.user_id AS user_id, u.username AS username, u.email AS email, r.role_name AS role_name, ur.assigned_at AS assigned_at 
FROM (users u JOIN user_roles ur ON (u.user_id = ur.user_id)) JOIN roles r ON (ur.role_id = r.role_id);