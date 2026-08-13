# weatherAPI-ingestion-pipeline

A simple weather data project built with Python, SQL, and an weather API.  
The project focuses on collecting, processing, and storing weather information for analysis and automation purposes.

## Technologies
- Python
- Pandas
- SQL
- Open-Meteo API
- SQLAlchemy
- Azure SQL
- Docker

## About
This project is being developed to practice data engineering concepts such as data pipelines, API integration, data transformation, and database management.

## Instructions
### 1. Install Docker

Install Docker Desktop for your operating system:
- https://docs.docker.com/desktop/setup/install/windows-install/
- https://docs.docker.com/desktop/setup/install/mac-install/
- https://docs.docker.com/desktop/setup/install/linux/

### 2. Create a Supabase project

Create a Supabase project and use the SQL structure provided in the `sql` folder to create the required database tables.

### 3. Configure the database connection

In your Supabase project, go to:

**Connect → Transaction Pooler → Type: SQLAlchemy → Add files: .env**

Create a `.env` file and paste the content, as showed in `.env.example`.

### 4. Build the Docker image and run
From the project root, run:
```bash
docker build -t weatherpipeline:1.0.0 .
```
then:
```bash
docker run --rm --env-file .env weatherpipeline:1.0.0
```
