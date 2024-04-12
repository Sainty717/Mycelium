# Use Ubuntu as base image
FROM ubuntu:latest

# Update packages and install Python
RUN apt-get update && \
    apt-get install -y python3 python3-pip

# Set working directory to /User
WORKDIR /User

# Copy necessary files
COPY pdf-viewer.py .
COPY templates ./templates
COPY pdfs ./pdfs
COPY web-app.py .
COPY admin.py .
COPY path1.png .
COPY nodes.json .
COPY links.json .
# Install Flask and Streamlit
RUN pip3 install flask streamlit

# Expose ports
EXPOSE 8501 8502 8503

# Command to run the applications
CMD ["sh", "-c", "python3 web-app.py & python3 pdf-viewer.py & streamlit run admin.py --server.port 8503"]
