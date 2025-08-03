FROM python:3.12-slim

WORKDIR /forex

# Copy requirements first for caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY Invest_iq_APP ./Invest_iq_APP

ENV PORT=8080
EXPOSE $PORT

ENV FLASK_APP=Invest_iq_APP/app.py

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
