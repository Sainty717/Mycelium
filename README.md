Here’s the entire page formatted in markdown so you can copy it directly:

# Mycelium Web Application (NGINX Plus Demo)

Hi there! I have built an app that allows you to build your own super dynamic relationship graphs that link directly to documentation. It serves as an educational tool to better understand the relationships between complex topics, products, or concepts.

Tested and running on Pi 4 and Pi 5

## Mycelium Web App
![Mycelium Web App](https://github.com/Sainty717/Mycelium/blob/main/ui.gif?raw=true)

## Admin Panel
![Admin Panel](https://github.com/Sainty717/Mycelium/blob/main/M-admin.png?raw=true)

## Setup Guide

Follow these steps to set up and run the web application:

### Prerequisites

Make sure you have Docker, Docker Compose, and apache2-utils installed on your system.

- [Docker installation guide](https://docs.docker.com/get-docker/)
- [Docker Compose installation guide](https://docs.docker.com/compose/install/)
- Apache2-utils for setting the password:
  ```bash
  sudo apt install apache2-utils
  ```

### Clone the Repository

Clone this repository to your local machine using Git:
```bash
wget https://codeload.github.com/Sainty717/Mycelium/zip/refs/heads/Nginx-Plus-Demo
unzip Nginx-Plus-Demo.zip
```

### Run the Application

Navigate into the cloned repository directory:
```bash
cd Mycelium-Nginx-Plus-Demo
```

Set Admin Panel Username and Password:
```bash
htpasswd -c ./htpasswd/.htpasswd <your_new_username>
```

## NGINX Plus Setup

1. Sign up for the [NGINX Plus free trial](https://www.f5.com/trials/free-trial-nginx-plus-and-nginx-app-protect).
2. After registering, you’ll receive two emails. Follow the instructions in the second email to activate your trial.
3. Once activated, you’ll obtain 3 essential files: the certificate,WJT (we will use this one later) and private key.
4. Save these files in the following directory within your project:

   ```/Mycelium/ssl/```

   Name the files:

   - `nginx-repo.crt` certificate
   - `nginx-repo.key` private key

### Docker Image Repository Login and Image Pull

1. Open the JWT previously downloaded from the MyF5 customer portal (e.g., `nginx-repo-12345abc.jwt`) and copy its contents.

2. Log in to the Docker registry using the contents of the JSON Web Token file:

   ```bash
   docker login private-registry.nginx.com --username=<output_of_jwt_token> --password=none
   ```

3. Next, pull the image you need from `private-registry.nginx.com`.

   ```bash
   docker pull private-registry.nginx.com/nginx-plus/base:r32-debian
   ```

### Build and Run the Application

Use Docker Compose to build and run the Docker containers:
```bash
docker-compose up -d --build
```

> **Note:** If you encounter an error, it might be due to incorrect Docker permissions. You can fix this by following the [Docker post-installation guide](https://docs.docker.com/engine/install/linux-postinstall/). Alternatively, you can prepend `sudo` to the command, though this is not recommended for security reasons.

### Access the Applications

Once the containers are up and running, you can access the applications using the following URLs:

- **Mycelium App (Flask)**: [http://localhost](http://localhost)
- **PDF Viewer**: [http://localhost/pdf](http://localhost/pdfs)
- **Mycelium Admin Panel**: [http://localhost/admin](http://localhost/admin)

### Admin Features

The admin panel offers complete control over the graph and customization options, including:

- **Security**: User and Password setup
- **Customization**:
  - Colors
  - Logo
  - Favicon
  - Title
  - Visibility of Control Panel
```

This should be fully copyable for your markdown-based README.
