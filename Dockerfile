# Use an official Python 3.9 image as the base
FROM python:3.9-slim

WORKDIR /app

# Copy only the requirements.txt first so we can layer-caching dependencies
COPY requirements.txt ./

# Install dependencies with pip
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your source code
COPY . .

EXPOSE 8000

CMD ["fastapi", "run", "app/main.py"]
