--
-- Oracle database dump
--

CREATE TABLE orders (
    order_id NUMBER NOT NULL,
    user_id NUMBER NOT NULL,
    status VARCHAR2(20) DEFAULT 'pending' NOT NULL,
    total_amount NUMBER(10,2) DEFAULT 0.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE SEQUENCE orders_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NOMINVALUE
    NOMAXVALUE
    CACHE 1;

ALTER TABLE orders MODIFY (order_id DEFAULT orders_order_id_seq.NEXTVAL);

ALTER TABLE orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (order_id);

CREATE INDEX idx_orders_pending ON orders (user_id);

--
-- Oracle database dump complete
--