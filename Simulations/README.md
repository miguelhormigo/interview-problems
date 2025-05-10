# Simulations

## Introduction

A backend service to schedule an specific IA Simulation to be run into some very big and expensive cloud machines.

## Architecture Overview

The application is designed using the FastAPI framework, leveraging its asynchronous capabilities to handle WebSocket connections and RESTful API endpoints efficiently.

### Components

1. **FastAPI Application**: It handles all HTTP and WebSocket requests. The application is divided into several modules, each responsible for a specific aspect of the functionality (e.g., simulations, machines, database).

2. **WebSocket**: A WebSocket endpoint is implemented to stream live simulation data to the frontend. This allows the frontend to display the convergence graph in real-time as the simulation progresses. The WebSocket also manages the simulation state, setting it to "running" when the simulation starts and "finished" when the connection is closed. A loop generates random convergence data points, simulating the progress of a running simulation

3. **Database**: The application interacts with a PostgreSQL database to store and retrieve data. The database schema includes tables for simulations, machines, and convergence data. The "asyncpg" library is used for asynchronous database operations.

4. **Dependency Injection**: FastAPI's dependency injection system is used to manage database connections. This makes it easy to override dependencies for testing purposes.

5. **Docker for Containerization**: The application and database are containerized using Docker.

6. **Tests**: The application includes some unit tests for the RESTful endpoints. These tests use FastAPI's "TestClient" and mock database connections.

## Setup

To set up the project locally, please follow these steps:

1. Clone the repository to your local machine.

2. Build and start the containers with the command "docker-compose up --build".

3. Access the application at http://localhost:8000. You can also access the automatic API documentation provided by FastAPI at http://localhost:8000/docs (Swagger UI) and http://localhost:8000/redoc (ReDoc).