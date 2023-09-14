FROM selenium/standalone-chrome:latest
WORKDIR /app
COPY . /app

USER root
RUN apt-get update && \
    apt-get install -y python3.7 python3-pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Run your script
CMD ["python3", "script.py"]
