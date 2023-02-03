CREATE TABLE words (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    word VARCHAR(50) NOT NULL UNIQUE,
    gap_index SMALLINT,
    gap_type VARCHAR(6),
    mistakes NUMERIC(4,2),
    word_sets TEXT ARRAY
);