FROM python:3.10.5
WORKDIR /app
COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# CMD python app.py
ENTRYPOINT ["sh", "/entrypoint.sh"]