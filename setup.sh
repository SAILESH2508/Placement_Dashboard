#!/bin/bash

# Placement Portal Setup Script
# This script sets up the development environment

echo "=========================================="
echo "Placement Portal Setup"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python --version

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your configuration"
fi

# Create logs directory
mkdir -p logs

# Run migrations
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Train ML model
echo "Training ML model..."
python ml_model/train_model.py

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo ""
echo "=========================================="
echo "✅ Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Create a superuser: python manage.py createsuperuser"
echo "3. (Optional) Load sample data: python manage.py populate_sample_data"
echo "4. Run the server: python manage.py runserver"
echo ""
echo "Frontend setup:"
echo "1. cd frontend"
echo "2. npm install"
echo "3. Copy .env.example to .env and configure"
echo "4. npm start"
echo ""
