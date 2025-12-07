# Deployment Guide

This guide covers deploying the Placement Portal to production environments.

## Prerequisites

- Linux server (Ubuntu 20.04+ recommended)
- Domain name
- SSL certificate
- PostgreSQL database
- Python 3.10+
- Node.js 16+
- Nginx
- Git

## Server Setup

### 1. Update System

```bash
sudo apt update
sudo apt upgrade -y
```

### 2. Install Dependencies

```bash
# Python and pip
sudo apt install python3.10 python3.10-venv python3-pip -y

# PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Nginx
sudo apt install nginx -y

# Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y

# Git
sudo apt install git -y
```

### 3. Create Database

```bash
sudo -u postgres psql

CREATE DATABASE placement_portal;
CREATE USER placement_user WITH PASSWORD 'your_secure_password';
ALTER ROLE placement_user SET client_encoding TO 'utf8';
ALTER ROLE placement_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE placement_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE placement_portal TO placement_user;
\q
```

## Backend Deployment

### 1. Clone Repository

```bash
cd /var/www
sudo git clone <repository-url> placement_portal
cd placement_portal
sudo chown -R $USER:$USER /var/www/placement_portal
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
pip install gunicorn
```

### 4. Configure Environment

```bash
cp .env.example .env
nano .env
```

Update `.env` with production values:

```env
SECRET_KEY=your-very-long-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DATABASE_URL=postgresql://placement_user:your_secure_password@localhost:5432/placement_portal

CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. Update settings.py for PostgreSQL

Add to `placement_portal/settings.py`:

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600
    )
}
```

### 6. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### 7. Train ML Model

```bash
python ml_model/train_model.py
```

### 8. Create Gunicorn Service

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:

```ini
[Unit]
Description=Gunicorn daemon for Placement Portal
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/placement_portal
Environment="PATH=/var/www/placement_portal/venv/bin"
ExecStart=/var/www/placement_portal/venv/bin/gunicorn \
    --workers 3 \
    --bind unix:/var/www/placement_portal/gunicorn.sock \
    placement_portal.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 9. Start Gunicorn

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```

## Frontend Deployment

### 1. Build Frontend

```bash
cd frontend
npm install
npm run build
```

### 2. Copy Build Files

```bash
sudo mkdir -p /var/www/placement_portal/frontend_build
sudo cp -r build/* /var/www/placement_portal/frontend_build/
```

## Nginx Configuration

### 1. Create Nginx Config

```bash
sudo nano /etc/nginx/sites-available/placement_portal
```

Add:

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        root /var/www/placement_portal/frontend_build;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://unix:/var/www/placement_portal/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Admin
    location /admin/ {
        proxy_pass http://unix:/var/www/placement_portal/gunicorn.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/placement_portal/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /var/www/placement_portal/media/;
    }
}
```

### 2. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/placement_portal /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL Certificate (Let's Encrypt)

### 1. Install Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Obtain Certificate

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 3. Auto-renewal

```bash
sudo certbot renew --dry-run
```

## Monitoring and Maintenance

### 1. Setup Logging

```bash
# View Gunicorn logs
sudo journalctl -u gunicorn -f

# View Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# View Django logs
tail -f /var/www/placement_portal/logs/django.log
```

### 2. Backup Script

Create `/var/www/placement_portal/backup.sh`:

```bash
#!/bin/bash

BACKUP_DIR="/var/backups/placement_portal"
DATE=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump placement_portal > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/placement_portal/media/

# Keep only last 7 days of backups
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

Make executable and add to cron:

```bash
chmod +x /var/www/placement_portal/backup.sh
sudo crontab -e

# Add daily backup at 2 AM
0 2 * * * /var/www/placement_portal/backup.sh
```

### 3. Update Application

```bash
cd /var/www/placement_portal
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## Performance Optimization

### 1. Enable Gzip Compression

Add to Nginx config:

```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### 2. Browser Caching

Add to Nginx config:

```nginx
location ~* \.(jpg|jpeg|png|gif|ico|css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

### 3. Database Connection Pooling

Install pgbouncer:

```bash
sudo apt install pgbouncer -y
```

## Troubleshooting

### Gunicorn not starting

```bash
sudo journalctl -u gunicorn -n 50
```

### Nginx errors

```bash
sudo nginx -t
sudo tail -f /var/log/nginx/error.log
```

### Database connection issues

```bash
sudo -u postgres psql
\l  # List databases
\du # List users
```

### Static files not loading

```bash
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

## Security Hardening

### 1. Firewall

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2. Fail2ban

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 3. Regular Updates

```bash
sudo apt update && sudo apt upgrade -y
```

## Monitoring Tools

Consider installing:

- **Sentry** - Error tracking
- **New Relic** - Performance monitoring
- **Prometheus + Grafana** - Metrics and dashboards
- **ELK Stack** - Log aggregation

---

**Need Help?** Contact the development team or refer to the main README.md
