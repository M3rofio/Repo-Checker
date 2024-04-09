# Dockerized Flask Application

This is a simple Flask application dockerized along with a Redis server using Docker Compose.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose

### Running the Application

1. Clone the repository:

   ```bash
   git clone https://github.com/M3rofio/Repo-Checker.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Repo-Checker
   ```

3. Run the following command to build and start the Docker containers:

   ```bash
   docker-compose up --build
   ```

4. Access the application in your web browser at [http://localhost:5000/](http://localhost:5000/).

### Customizing the Application

You can customize the Flask application by modifying the `app.py` file and templates located in the `templates` directory.

### Adding Repositories via Web GUI

To add repositories to watch for new releases, access the web GUI by visiting [http://localhost:5000/](http://localhost:5000/) and inputting the repository details.

## Authors

- [M3rofio](https://github.com/M3rofio/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

