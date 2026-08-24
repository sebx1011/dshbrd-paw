create table lambdas (
    id serial primary key,
    lambda_name varchar(255) not null unique,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp
);

create table metrics (
    id serial primary key,
    lambda_id int references lambdas(id) on delete restrict,
    fecha date not null,
    invocaciones int not null,
    errores int null,
    created_at timestamp default current_timestamp,
    updated_at timestamp default current_timestamp,
    unique (lambda_id, fecha)
);

insert into lambdas (lambda_name) values
('episodios-crearPreAdmisionHospitalizado-prod'),
('episodios-generarDocumentosPreAdmision-prod'),
('episodios-firmarDocumentosPreAdmision-prod');