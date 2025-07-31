# Base image
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Copy only requirements.txt first for caching layer efficiency
COPY Invest_iq_APP/requirements.txt .

# Copy files
#COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose configurable port
ENV PORT=8080
EXPOSE $PORT

# Copy the rest of the application files
COPY Invest_iq_APP/ .

# Start the Flask app
#CMD ["python", "app.py"]

# Use 0.0.0.0 so Flask can be accessed outside container
ENV FLASK_APP=app.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
