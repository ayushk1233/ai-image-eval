FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source, static files, and initial database
COPY backend /app/backend
COPY docs /app/docs
COPY reports /app/reports
COPY data /app/data
COPY generated_images /app/generated_images


# Expose port and start script
EXPOSE 8000
CMD ["/app/backend/start.sh"]
