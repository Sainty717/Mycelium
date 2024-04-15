
# Mycelium Web Application
Hi There, I have built an app that allows you build your own super Dynamic Realationship graphs that link directly to docuementation, as an educational tool to better undrestand the realationship between complex topics products or concepts.

Tested and running on Pi 4 and Pi 5 
# Mycelium Web App
![](https://github.com/Sainty717/Mycelium/blob/main/ui.gif?raw=true)
# Admin Pannel
![](https://github.com/Sainty717/Mycelium/blob/main/M-admin.png?raw=true)

## Setup Guide

Follow these steps to set up and run the web application:

### Prerequisites

Make sure you have Docker,Docker Compose and apache2-utils installed on your system.

- [Docker installation guide](https://docs.docker.com/get-docker/)
- [Docker Compose installation guide](https://docs.docker.com/compose/install/)
- apache2-utils for setting the password
  ``` sudo apt install apache2-utils ```

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
Set Admin Pannel Username and Password

```
htpasswd -c ./htpasswd/.htpasswd <your new username>
```

Use Docker Compose to build and run the Docker containers:

```
docker-compose up -d --build
```



### Access the Applications

Once the containers are up and running, you can access the applications using the following URLs:

- **Mycelium App (Flask)**: [http://localhost](http://localhost)
- **PDF Viewer**: [http://localhost/pdf](http://localhost/pdfs)
- **Mycelium Admin Panel**: [http://localhost/admin](http://localhost/admin)


### Enable HTTPS (in progress)

 - Replace the Nginx conf with nginx-https.conf
 - Replace The docker-compose.yaml with docker-compose-https.yaml
 - Edit the nginx-https.conf with your Domain Name  (If your new to this process you need a domain name, exposed port to the server and a certificate. I personally reccommend Certbot for certificates and cheapname.com for a domain name register)
 - Add certificate.pem and privatekey.pem to the Mycelium git Directory
 - ```
   docker compose up -d
   ```
   



