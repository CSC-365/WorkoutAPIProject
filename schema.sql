BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> cc180ca59bbd

CREATE TABLE users (
    user_id BIGSERIAL NOT NULL, 
    starting_lbs BIGINT, 
    name TEXT, 
    height_inches BIGINT, 
    avg_calorie_intake BIGINT, 
    age BIGINT, 
    gender TEXT, 
    CONSTRAINT users_pkey PRIMARY KEY (user_id)
);

CREATE TABLE goals (
    goal_id BIGSERIAL NOT NULL, 
    user_id BIGINT, 
    type_id BIGINT, 
    target_weight BIGINT, 
    workout_id BIGINT, 
    CONSTRAINT goals_pkey PRIMARY KEY (goal_id)
);

CREATE TABLE log (
    log_id BIGSERIAL NOT NULL, 
    user_id BIGINT, 
    current_lbs BIGINT, 
    time_posted TIMESTAMP WITH TIME ZONE, 
    CONSTRAINT log_pkey PRIMARY KEY (log_id)
);

CREATE TABLE workouts (
    workout_id BIGSERIAL NOT NULL, 
    workout_name TEXT, 
    weight BIGINT, 
    distance_ft BIGINT, 
    repetitions BIGINT, 
    seconds BIGINT, 
    sets BIGINT, 
    times_per_week BIGINT, 
    user_id BIGINT, 
    CONSTRAINT workouts_pkey PRIMARY KEY (workout_id), 
    CONSTRAINT workouts_user_id_fkey FOREIGN KEY(user_id) REFERENCES users (user_id)
);

CREATE TABLE goal_types (
    type_id BIGSERIAL NOT NULL, 
    type TEXT, 
    CONSTRAINT goal_types_pkey PRIMARY KEY (type_id)
);

INSERT INTO alembic_version (version_num) VALUES ('cc180ca59bbd') RETURNING alembic_version.version_num;

-- Running upgrade cc180ca59bbd -> 7f462fa3993b

ALTER TABLE users DROP COLUMN age;

ALTER TABLE users ADD COLUMN birthday DATE;

ALTER TABLE workouts DROP CONSTRAINT workouts_user_id_fkey;

ALTER TABLE users DROP COLUMN user_id;

ALTER TABLE users ADD COLUMN id SERIAL NOT NULL;

ALTER TABLE users ADD UNIQUE (id);

ALTER TABLE goals DROP COLUMN goal_id;

ALTER TABLE goals ADD COLUMN id SERIAL NOT NULL;

ALTER TABLE workouts DROP COLUMN workout_id;

ALTER TABLE workouts ADD COLUMN id SERIAL NOT NULL;

ALTER TABLE log DROP COLUMN log_id;

ALTER TABLE log ADD COLUMN id SERIAL NOT NULL;

UPDATE alembic_version SET version_num='7f462fa3993b' WHERE alembic_version.version_num = 'cc180ca59bbd';

-- Running upgrade 7f462fa3993b -> 54db841c5205

CREATE TABLE projection (
    projection_id SERIAL NOT NULL, 
    user_id INTEGER NOT NULL, 
    projection_date TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    projection_lbs SMALLINT NOT NULL, 
    date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL, 
    PRIMARY KEY (projection_id), 
    CONSTRAINT projection_user_id_fkey FOREIGN KEY(user_id) REFERENCES users (id)
);

UPDATE alembic_version SET version_num='54db841c5205' WHERE alembic_version.version_num = '7f462fa3993b';

-- Running upgrade 54db841c5205 -> 7ebb53893509

ALTER TABLE users ADD COLUMN password BYTEA;

ALTER TABLE users ADD COLUMN salt BYTEA;

UPDATE alembic_version SET version_num='7ebb53893509' WHERE alembic_version.version_num = '54db841c5205';

-- Running upgrade 7ebb53893509 -> c1e0267a981d

ALTER TABLE users DROP COLUMN password;

ALTER TABLE users ADD COLUMN password BYTEA;

ALTER TABLE users DROP COLUMN salt;

ALTER TABLE users ADD COLUMN salt BYTEA;

UPDATE alembic_version SET version_num='c1e0267a981d' WHERE alembic_version.version_num = '7ebb53893509';

COMMIT;

