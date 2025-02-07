-- Drop the table if it exists (without error)
BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE test';
EXCEPTION
    WHEN OTHERS THEN
        NULL;  -- Ignore errors (if table does not exist)
END;
/

-- Create the new table
CREATE TABLE test (
    id NUMBER PRIMARY KEY, 
    name_first VARCHAR2(20) NOT NULL,
    name_last VARCHAR2(20) NOT NULL
);

-- Insert data (use single quotes for strings)
INSERT INTO test (id, name_first, name_last)
VALUES (0, 'Na-meme', 'Mamaman');

-- Commit the transaction
COMMIT;

-- Select data to verify insertion
SELECT * FROM test;
/
