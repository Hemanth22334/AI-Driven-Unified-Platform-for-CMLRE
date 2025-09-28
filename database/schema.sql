-- PostgreSQL schema for the marine data platform

CREATE TABLE oceanography (
    id SERIAL PRIMARY KEY,
    location_id INT,
    timestamp TIMESTAMP,
    water_temp_C FLOAT,
    salinity_PSU FLOAT,
    depth_m FLOAT,
    dissolved_oxygen_mgL FLOAT
);

CREATE TABLE taxonomy (
    id SERIAL PRIMARY KEY,
    species_name VARCHAR(255),
    scientific_name VARCHAR(255) UNIQUE,
    family VARCHAR(255),
    "order" VARCHAR(255),
    class VARCHAR(255)
);

CREATE TABLE morphology (
    id SERIAL PRIMARY KEY,
    specimen_id INT UNIQUE,
    species_id INT,
    otolith_shape_data JSONB,
    length_cm FLOAT,
    weight_g FLOAT,
    FOREIGN KEY (species_id) REFERENCES taxonomy(id)
);

CREATE TABLE molecular_data (
    id SERIAL PRIMARY KEY,
    specimen_id INT,
    dna_sequence TEXT,
    e_dna_sample_id VARCHAR(255),
    FOREIGN KEY (specimen_id) REFERENCES morphology(specimen_id)
);