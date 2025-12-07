@echo off
REM Placement Portal Setup Script for Windows
REM This script sets up the development environment

echo ==========================================
echo Placement Portal Setup
echo ==========================================

REM Check Python version
echo Checking Python version...
python --version

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing Python dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo WARNING: Please edit .env file with your configuration
)

REM Create logs directory
if not exist "logs" mkdir logs

REM Run migrations
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Train ML model
echo Training ML model...
python ml_model\train_model.py

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file with your configuration
echo 2. Create a superuser: python manage.py createsuperuser
echo 3. (Optional) Load sample data: python manage.py populate_sample_data
echo 4. Run the server: python manage.py runserver
echo.
echo Frontend setup:
echo 1. cd frontend
echo 2. npm install
echo 3. Copy .env.example to .env and configure
echo 4. npm start
echo.
pause
