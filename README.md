# Library Backend NFact

This project is a backend application for managing a library system.

## Features

- **API**: Contains the API endpoints for the application.
- **Core**: Includes the core functionalities and business logic.
- **Media**: Stores media files related to books.

## Getting Started

### Prerequisites

- Python 3.x
- [Poetry](https://python-poetry.org/) for dependency management
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/zhalgas-seidazym/library_backend_nfact.git
   cd library_backend_nfact
   ```

2. **Set up the environment**:

   - Copy the example environment file and modify it as needed:

     ```bash
     cp .env.example .env
     ```

3. **Install dependencies**:

   ```bash
   poetry install
   ```

4. **Apply migrations**:

   ```bash
   poetry run python manage.py migrate
   ```

5. **Run the development server**:

   ```bash
   poetry run python manage.py runserver
   ```

   The application will be available at `http://127.0.0.1:8000/`.

### Docker Deployment

1. **Build the Docker image**:

   ```bash
   docker build -t library_backend_nfact .
   ```

2. **Run the Docker container**:

   ```bash
   docker run -d -p 8000:8000 --env-file .env library_backend_nfact
   ```

   The application will be accessible at `http://127.0.0.1:8000/`.

## Project Structure

- **`api/`**: Contains the API endpoints.
- **`core/`**: Core application logic.
- **`medias/book/`**: Directory for book-related media files.
- **`.env.example`**: Example environment configuration file.
- **`Dockerfile`**: Docker configuration for containerizing the application.
- **`manage.py`**: Django's command-line utility for administrative tasks.
- **`pyproject.toml`**: Configuration file for Poetry and project metadata.

