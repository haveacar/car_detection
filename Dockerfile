# Use a slim version of Python 3.11 as the base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Combine apt-get update, package installation, and cleanup into a single RUN to reduce layers and remove cache files to save space
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libx11-xcb1 \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-randr0 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    xkb-data \
    libxkbcommon-x11-0 \
    libxkbcommon0 \
    libxcb1 \
    libqt5widgets5 \
    libqt5gui5 \
    libqt5core5a \
    xauth \
    xvfb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Update pip, setuptools, and wheel with a single RUN command to reduce layers
RUN pip install --upgrade pip setuptools wheel

# Copy only the requirements.txt file initially to cache the dependencies layer
COPY requirements.txt ./

# Install Python dependencies from requirements.txt
# Use --no-cache-dir to avoid storing unnecessary files, helping to save space
RUN pip install --no-cache-dir -r requirements.txt


# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Create .Xauthority file is necessary for X11 forwarding
RUN touch /root/.Xauthority

# Set environment variables for Qt and X11
ENV DISPLAY=:0

# Expose port 80 and any other necessary ports to the world outside this container
EXPOSE 80 18975

# Use a more compact CMD to start Xvfb and your application
CMD Xvfb :0 -screen 0 1024x768x16 & \
    sleep 5 && \
    xauth add :0 . $(mcookie) && \
    echo "Xvfb started" && \
    python ./application.py