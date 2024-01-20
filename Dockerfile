FROM python:3.11-slim-bullseye

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

#create user and group
RUN groupadd -r ch && useradd --no-log-init -m -r -g ch ch

#update path env
ENV PATH="/home/ch/.local/bin:${PATH}"

# create working dir
RUN mkdir /app && chown ch:ch /app
RUN mkdir /app/temp && chown ch:ch /app/temp

# switch to non-root user
USER ch
WORKDIR /app

# copy files to workdir
COPY --chown=ch:ch . /app/
RUN chmod 755 /app

# Copy the application source code to the container and set the working directory
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
