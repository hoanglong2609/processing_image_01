create table "user"
(
    id bigserial not null,
    code text,
    name text,
    mail text,
    password text,
    subject_ids bigint[],
    role int,
    CONSTRAINT pkey_user PRIMARY KEY (id)
);

create table "score"
(
    id bigserial not null,
    student_id bigint,
    image_id bigint,
    score float,
    filled_cell int [],
    subject_id bigint,
    code int,
    CONSTRAINT pkey_score PRIMARY KEY (id)
);

create table "subject"
(
    id bigserial not null,
    name text,
    CONSTRAINT pkey_subject PRIMARY KEY (id)
);

create table "image"
(
    id bigserial not null,
    url text,
    path text,
    CONSTRAINT pkey_image PRIMARY KEY (id)
);

-- file result by code and class_id
create table "result"
(
    id bigserial not null,
    code int,
    image_id bigint,
    subject_id bigint,
    result int [],
    CONSTRAINT pkey_result PRIMARY KEY (id)
);

create unique index unit_unique_code_class_id on result (code, subject_id) where true;