# Toman Task

## Description

API for

* transaction
* get wallet balance
* schedule priodic transaction

# Install project dependencies:

Creating a Virtual Environment

1. Open your terminal.
2. Navigate to the directory where you want to create the virtual environment:
   ```bash
   cd /path/to/your/project
   ```

### macOS and Linux

```bash
    python3 -m venv myenv
    source myenv/bin/activate
    python -m pip install -r requirements.txt
```

### Windows

```bash
    python -m venv myenv
    myenv\Scripts\activate
    python -m pip install -r requirements.txt
```

# Installing RabbitMQ

RabbitMQ is a message broker that facilitates communication between distributed components. It's commonly used to manage
and deliver messages across applications. This guide provides instructions for installing RabbitMQ on various operating
systems.

## Prerequisites

Ensure that you have administrative privileges on your system before proceeding with the installation.

## Installation

### macOS

1. Open your terminal.

2. Install RabbitMQ:

```bash
brew install rabbitmq
```

3. Start the RabbitMQ server:

```bash
brew services start rabbitmq
```

### Linux (Ubuntu)

1. Open your terminal.
2. Update the package index:

```bash
sudo apt update
```
3. Install RabbitMQ:
```bash
sudo apt install rabbitmq-server
```
4. Start the RabbitMQ server:
```bash
sudo systemctl start rabbitmq-server
```

# Apply migrations:

```bash
python manage.py migrate
```

# load data

```bash
python manage.py loaddata transfer/fixtures/wallets_data.json
```

# Run project

1. Start the Django development server:

```bash
python manage.py runserver
```

2. Start Gunicorn with your Django application:

```bash
gunicorn toman_task.wsgi:application
```

3. Run Celery worker for handling asynchronous tasks:

```bash
celery -A toman_task worker -l info
```

4. Run Celery worker for handling asynchronous tasks:

```bash
celery -A toman_task beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

5. Run Celery worker for handling asynchronous tasks:

```bash
celery -A toman_task flower
```

# Using Postman Collection to Test the Project

To simplify the process of testing API endpoints and interactions in your project, we provide a Postman collection that
you can import and use. Postman is a popular tool for testing and documenting APIs.

## Prerequisites

- [Postman](https://www.postman.com/downloads/) installed on your system.

## Importing the Postman Collection

1. Download the provided Postman collection JSON file from the repository.

2. Open Postman.

3. Click the "Import" button on the top-left corner.

4. Choose the downloaded JSON file and import it.

## Configuring Environment Variables

1. In Postman, click the gear icon (top-right corner) and select "Manage Environments."

2. Click "Add" to create a new environment. Give it a name, for example, "Project Environment."

3. Add environment variables such as `BASE_URL` and other relevant variables required for your project. These variables
   will allow you to switch between different environments easily.

## Running Requests

1. With the Postman collection imported and the environment set up, you can start running requests.

2. Select the desired request from the imported collection.

3. Choose the desired environment from the environment dropdown in the top-right corner.

4. Fill in the necessary request parameters and headers.

5. Click the "Send" button to execute the request.

## Provided test file 
