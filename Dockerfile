FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app
COPY . .

RUN pip install flask playwright openpyxl
RUN playwright install chromium

EXPOSE 5000
CMD ["python", "app.py"]