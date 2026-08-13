"PostgreSQL format"
CREATE TABLE hourly_data (
    forecast_time TIMESTAMP NOT NULL,
    consult_time TIMESTAMP NOT NULL,

    temperature_2m DOUBLE PRECISION,
    rain DOUBLE PRECISION,
    precipitation_probability DOUBLE PRECISION,
    relative_humidity_2m DOUBLE PRECISION,
    wind_speed_10m DOUBLE PRECISION,

    temperature_2m_variance DOUBLE PRECISION,
    rain_variance DOUBLE PRECISION,
    precipitation_probability_variance DOUBLE PRECISION,
    relative_humidity_2m_variance DOUBLE PRECISION,
    wind_speed_10m_variance DOUBLE PRECISION,

    PRIMARY KEY (forecast_time, consult_time)
);

"Sqlserver format"
CREATE TABLE hourly_data (
    forecast_time DATETIME2 NOT NULL,
    consult_time DATETIME2 NOT NULL,

    temperature_2m FLOAT,
    rain FLOAT,
    precipitation_probability FLOAT,
    relative_humidity_2m FLOAT,
    wind_speed_10m FLOAT,

    temperature_2m_variance FLOAT,
    rain_variance FLOAT,
    precipitation_probability_variance FLOAT,
    relative_humidity_2m_variance FLOAT,
    wind_speed_10m_variance FLOAT,

    PRIMARY KEY (forecast_time, consult_time)
);