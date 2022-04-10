CREATE TABLE area (
    id bigint NOT NULL DEFAULT nextval('"APIapp_provider_id_seq"'::regclass),
	provider_id bigint,
    area_name character varying(250) COLLATE pg_catalog."default" NOT NULL,
	area_price FLOAT,
    polygon GEOMETRY
);

CREATE INDEX areas_polygon_idx ON area USING GIST (polygon);
