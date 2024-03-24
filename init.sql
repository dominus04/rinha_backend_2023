CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE IF NOT EXISTS users(
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    apelido VARCHAR(32) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    nascimento varchar(10) NOT NULL,
    stack VARCHAR(1024),
    campo_busca TEXT GENERATED ALWAYS AS (LOWER(apelido || nome || stack)) STORED
);

CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_campo_busca_gist ON users USING GIST (campo_busca gist_trgm_ops);