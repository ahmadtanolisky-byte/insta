FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir flask playwright openpyxl

# Install Chromium browser
RUN playwright install chromium

# Expose port
EXPOSE 5000

# Start the app
CMD ["python", "app.py"]