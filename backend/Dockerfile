FROM python:3.11-slim

WORKDIR /app

# Install dependencies first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source and static files
COPY backend /app/backend
COPY docs /app/docs
COPY reports /app/reports

# Expose port and start script
EXPOSE 8000
CMD ["/app/backend/start.sh"]
