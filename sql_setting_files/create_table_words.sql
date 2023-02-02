CREATE TABLE words (
    id BIGINT NOT NULL PRIMARY KEY,
    word VARCHAR(50) NOT NULL UNIQUE,
    gap_index SMALLINT,
    mistakes BIGINT
);