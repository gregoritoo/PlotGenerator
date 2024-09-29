FROM python:3.11-slim

WORKDIR /app

# Update the package list and install the required packages
RUN apt-get update --fix-missing 

RUN   apt-get install -y --no-install-recommends \
    libgtk2.0-dev \
    bzip2 \
    ca-certificates \
    curl \
    git \
    vim \
    g++ \
    gcc \
    zip \
    lrzip \
    unzip \
    graphviz \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libhdf5-dev \
    openmpi-bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* \
    build-essential \
    python3-dev \
    setuptools \
    cmake \
    wget 

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server script
COPY server.py .

# Expose port 1000
EXPOSE 1000

# Command to run the application
CMD ["python", "server.py", "1000"]
