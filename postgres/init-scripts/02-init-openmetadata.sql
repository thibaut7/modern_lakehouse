-- Create user and database for OpenMetadata
CREATE USER openmetadata_user WITH PASSWORD 'openmetadata_password';
CREATE DATABASE openmetadata_db;
GRANT ALL PRIVILEGES ON DATABASE openmetadata_db TO openmetadata_user;
ALTER DATABASE openmetadata_db OWNER TO openmetadata_user;
