--
-- Oracle database dump
--

CREATE SEQUENCE random_points_id_seq
    START WITH 1
    INCREMENT BY 1
    NOMINVALUE
    NOMAXVALUE
    CACHE 1;

--
-- Name: random_points; Type: TABLE
--

CREATE TABLE random_points (
    id NUMBER NOT NULL,
    geom SDO_GEOMETRY
);

--
-- Name: random_points_id_seq; Type: SEQUENCE OWNED BY
--

-- Oracle does not have direct equivalent of SEQUENCE OWNED BY, 
-- use trigger instead
CREATE OR REPLACE TRIGGER random_points_id_trg
BEFORE INSERT ON random_points
FOR EACH ROW
BEGIN
    SELECT random_points_id_seq.NEXTVAL
    INTO :NEW.id
    FROM DUAL;
END;
/

--
-- Name: random_points random_points_pkey; Type: CONSTRAINT
--

ALTER TABLE random_points
    ADD CONSTRAINT random_points_pkey PRIMARY KEY (id);