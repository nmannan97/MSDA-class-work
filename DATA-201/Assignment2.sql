CREATE TABLE employees (
    id NUMBER PRIMARY KEY,
    name_first VARCHAR2 (50) NOT NULL,
    name_second VARCHAR2 (50) NOT NULL,
    unique_ids VARCHAR2(20)
)
SELECT us er FROM dual;

INSERT INTO employees(id, name_first, name_second, unique_ids)
VALUES (1, "Charlamane", "Happsburg", " ");

INSERT INTO employees(id, name_first, name_second, unique_ids)
VALUES (2, "Jane", "Doe", "UwU");

SELECT * FROM employees;