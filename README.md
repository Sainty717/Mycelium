
# Mycelium Web Application
Hi There, I have built an app that allows you build your own super Dynamic Realationship graphs that link directly to docuementation, as an educational tool to better undrestand the realationship between complex topics products or concepts.


## Setup Guide

Follow these steps to set up and run the web application:

### Prerequisites

Make sure you have Docker and Docker Compose installed on your system.

- [Docker installation guide](https://docs.docker.com/get-docker/)
- [Docker Compose installation guide](https://docs.docker.com/compose/install/)

### Clone the Repository

Clone this repository to your local machine using Git:
```
git clone https://github.com/your_username/flask-streamlit-docker.git
```


### Run the Application

Navigate into the cloned repository directory:
```
cd Mycelium
```
Use Docker Compose to build and run the Docker containers:

```
docker-compose up -d --build
```



### Access the Applications

Once the containers are up and running, you can access the applications using the following URLs:

- **Web App (Flask)**: [http://localhost:8501](http://localhost:8501)
- **PDF Viewer**: [http://localhost:8502](http://localhost:8502)
- **Admin Panel (Streamlit)**: [http://localhost:8503](http://localhost:8503)

### Port Requirements

Ensure that the following ports are available on your system:

- **8501**: Flask web application
- **8502**: PDF viewer
- **8503**: Streamlit admin panel


