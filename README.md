# zrch-assignment
# Car Platform API

This repository contains the API services for managing car listings in the platform.

## Getting Started

### Prerequisites

Make sure you have the following installed on your machine:

- Docker
- MongoDB (for local development)

### Installation and Setup

1. Clone this repository:

    ```bash
    git clone https://github.com/prghpk/zrch-assignment.git
    ```

2. Navigate to the project directory:

    ```bash
    cd zrch-assignment
    ```

3. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

4. Access the API at [http://0.0.0.0:8000](http://0.0.0.0:8000).

### Local Development

For local development, follow these steps:

1. Install and run MongoDB.

2. Replace the `MONGO_URL` with your local MongoDB URL. You can do this in the `docker-compose.yml` file.

3. Run the FastAPI server:

    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    ```

4. Access the API at [http://localhost:8000](http://localhost:8000).

## Unit Testing

To run unit tests, use the following command:

```bash
pytest
```
## API Documentation

The API documentation is available when the server is running. Follow the steps below to access the documentation:

1. Make sure the FastAPI server is running.
2. Open your web browser.
3. Visit [http://localhost:8000/docs](http://localhost:8000/docs) or [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) to access the API documentation.
