DROP TABLE employees;

CREATE TABLE employees (
    id NUMBER PRIMARY KEY,
    name_first VARCHAR2(50) NOT NULL,
    name_second VARCHAR2(50) NOT NULL,
    unique_ids VARCHAR2(20)
);

INSERT INTO employees(id, name_first, name_second, unique_ids)
VALUES (1, 'Charlemagne', 'Happsburg', '0');

INSERT INTO employees(id, name_first, name_second, unique_ids)
VALUES (2, 'Jane', 'Doe', 'UwU');

SELECT * FROM system.employees;
