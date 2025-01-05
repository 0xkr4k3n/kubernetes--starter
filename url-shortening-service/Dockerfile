FROM python:3.9-slim 

RUN useradd -ms /bin/bash appuser
USER appuser


WORKDIR /home/appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

ENV PATH="/home/appuser/.local/bin:${PATH}"

CMD ["python","app.py"]
