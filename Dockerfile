FROM python:3.7.4-slim

RUN adduser --system --no-create-home --group genop-demo

WORKDIR /app

RUN chown genop-demo .

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=genop-demo . .

USER genop-demo

ENTRYPOINT ["python", "main.py"]
