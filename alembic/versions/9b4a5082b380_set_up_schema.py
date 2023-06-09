"""set up schema

Revision ID: 9b4a5082b380
Revises: 
Create Date: 2023-06-06 15:36:28.243663

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b4a5082b380'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    CREATE SEQUENCE users_id_seq;
    """)

    op.execute("""
    CREATE SEQUENCE goal_types_type_id_seq;
    """)

    op.execute("""
    CREATE SEQUENCE goals_id_seq;
    """)

    op.execute("""
    CREATE SEQUENCE logs_id_seq;
    """)

    op.execute("""
    CREATE SEQUENCE workouts_id_seq;
    """)

    op.execute("""
    CREATE SEQUENCE projection_projection_id_seq;
    """)

    op.execute("""
    CREATE TABLE public.users (
        starting_lbs BIGINT,
        name TEXT,
        height_inches BIGINT,
        avg_calorie_intake BIGINT,
        gender TEXT,
        birthday DATE,
        id INTEGER NOT NULL DEFAULT nextval('users_id_seq'::regclass),
        password BYTEA,
        salt BYTEA,
        CONSTRAINT users_pkey PRIMARY KEY (id),
        CONSTRAINT users_id_key UNIQUE (id)
    ) TABLESPACE pg_default;
    """)

    op.execute("""
    CREATE TABLE public.goal_types (
        type_id BIGINT NOT NULL DEFAULT nextval('goal_types_type_id_seq'::regclass),
        type TEXT,
        CONSTRAINT goal_types_pkey PRIMARY KEY (type_id)
    ) TABLESPACE pg_default;
    """)

    op.execute("""
    CREATE TABLE public.goals (
        user_id BIGINT,
        type_id BIGINT,
        target_weight BIGINT,
        workout_id BIGINT,
        id INTEGER NOT NULL DEFAULT nextval('goals_id_seq'::regclass),
        CONSTRAINT goals_pkey PRIMARY KEY (id),
        CONSTRAINT goals_id_key UNIQUE (id)
    ) TABLESPACE pg_default;
    """)

    op.execute("""
    CREATE TABLE public.logs (
        user_id BIGINT,
        current_lbs BIGINT,
        time_posted TIMESTAMP WITH TIME ZONE,
        id INTEGER NOT NULL DEFAULT nextval('logs_id_seq'::regclass),
        CONSTRAINT logs_pkey PRIMARY KEY (id),
        CONSTRAINT logs_id_key UNIQUE (id)
    ) TABLESPACE pg_default;
    """)

    op.execute("""
    CREATE TABLE public.workouts (
        workout_name TEXT,
        weight BIGINT,
        distance_ft BIGINT,
        repetitions BIGINT,
        seconds BIGINT,
        sets BIGINT,
        times_per_week BIGINT,
        user_id BIGINT,
        id INTEGER NOT NULL DEFAULT nextval('workouts_id_seq'::regclass),
        CONSTRAINT workouts_pkey PRIMARY KEY (id),
        CONSTRAINT workouts_id_key UNIQUE (id)
    ) TABLESPACE pg_default;
    """)

    op.execute("""
    CREATE TABLE public.projection (
        projection_id INTEGER NOT NULL DEFAULT nextval('projection_projection_id_seq'::regclass),
        user_id INTEGER NOT NULL,
        projection_date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        projection_lbs SMALLINT NOT NULL,
        date_posted TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        CONSTRAINT projection_pkey PRIMARY KEY (projection_id),
        CONSTRAINT projection_projection_id_key UNIQUE (projection_id),
        CONSTRAINT projection_user_id_fkey FOREIGN KEY (user_id) REFERENCES users (id)
    ) TABLESPACE pg_default;
    """)


def downgrade():
    op.execute("""
    DROP TABLE public.projection;
    """)

    op.execute("""
    DROP TABLE public.workouts;
    """)

    op.execute("""
    DROP TABLE public.logs;
    """)

    op.execute("""
    DROP TABLE public.goals;
    """)

    op.execute("""
    DROP TABLE public.goal_types;
    """)

    op.execute("""
    DROP TABLE public.users;
    """)
