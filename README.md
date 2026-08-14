# weatherAPI-ingestion-pipeline

This project is a data ingestion pipeline built to collect weather data from the Open-Meteo API, process it, and store the results in a relational database.

The project is part of pratical study of some technologies and concepts, focusing on the flow from external API ingestion to data storage and automated execution.

## Overview

The pipeline periodically retrieves weather information from the Open-Meteo API, transforms the received data into a structured format and storage it in a SQL database.

The project also explores containers and cloud, using Docker to package the application and Azure SQL as the database.

The execution process was designed to be automated through GitHub Actions, allowing the ingestion pipeline to run without requiring manual execution.

## Technologies

- Python
- Pandas
- Open-Meteo API
- SQLAlchemy
- Azure SQL
- Docker
- GitHub Actions
- SQL

## Development

The initial development of the pipeline was relatively straightforward, ingestion itself, API connectivity, data cleaning, and structuring were simple to implement. The Open-Meteo website also made the process easier by allowing me to define the weather data and parameters i wanted to retrieve, which made the API integration more practical.

As I continued studying data engineering, especially through DataTalks.Club's Data Engineering Zoomcamp and other materials, new ideas started to pop and the project evolved beyond its original scope.

The database architecture changed a lot, i initially used PostgreSQL locally, eventually migrated to Azure SQL, and during studies, i was introduced to `Docker`, which became another important part of the project. Applying the concept to the pipeline was great, especially because running the application inside a container made it much easier to integrate the entire process with GitHub Actions. Instead of having to configure the execution environment directly in the workflow, the pipeline could simply run the Docker container, making the automated execution more consistent and easier to manage.

The automation itself also led to a problem. Although the GitHub Actions workflow was correctly configured with a schedule trigger, the schedules were not consistently occurring at the given times. Since the pipeline needed a more reliable external scheduler, i ended up using an external ([cron service](https://cron-job.org/en/)) to send an HTTP POST request to the GitHub API, triggering the workflow through workflow_dispatch using a GitHub authentication token.
 
Overall, the project is evolved as i learned more. It bencame a practical way to experimet with `API integration`, `data cleaning`, `PostgreSQL`, `Azure SQL`, `Docker`, `GitHub Actions`, and workflow automation. 
The project isnt finished, and i will keep adding new things to it.

