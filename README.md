# Flask Visitor Counter with PostgreSQL

This project is a simple Flask web application that logs and displays visitor information using a PostgreSQL database. Each visit is recorded with a timestamp, the instance name of the server, and additional request details.

## Features
- The `/` route displays the total visit count and stores information about the new visit in a PostgreSQL database.
- The `/<entry_id>` displays the visit information for that visit. E.g. `/1` shows the first visit recorded.

## Environment Variables
The application relies on the following environment variables for configuration:

- `DB_NAME`: Name of the PostgreSQL database
- `DB_USER`: Username for the PostgreSQL database
- `DB_PASSWORD`: Password for the PostgreSQL database
- `DB_HOST`: Database host
- `DB_PORT`: Port on which PostgreSQL is running
- `INSTANCE_NAME`: Name of the EC2 instance / host where the app is running

When running locally, these variables are set in [docker-compose.yml](./docker-compose.yml).

## Running the Application Locally

### Requirements
- Docker

### Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/khdev-devops/grupparbete-mar6
   cd grupparbete-mar6
   ```

2. **Start the application using Docker Compose:**
   ```sh
   ./local-start.sh
   ```
   By default, the application will run on port `5000`. To run it on a different port, specify the port number:
   ```sh
   ./local-start.sh 5001
   ```

3. **Access the application:**
   Open a web browser and go to:
   ```sh
   http://localhost:5000/
   ```
   or (if using a custom port, e.g. 5001)
   ```sh
   http://localhost:5001/
   ```

4. **Retrieve visitor information by ID:**
   ```sh
   http://localhost:5000/<entry_id>
   ```
   Replace `<entry_id>` with a valid visitor ID to fetch stored details.

## Stopping the Application
To stop and remove containers, run:
   ```sh
   docker compose down
   ```

## Project Structure
```
/
├── app.py               # Flask application
├── Dockerfile           # Docker setup for Flask
├── docker-compose.yml   # Defines services for the app and PostgreSQL for running locally
├── requirements.txt     # Python dependencies
├── local-start.sh       # Script to start the application locally with an optional port parameter
└── README.md            # This file
```
