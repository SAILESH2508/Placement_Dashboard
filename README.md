# 🎓 Placement Portal - Comprehensive Documentation

A comprehensive AI-powered placement management system for educational institutions built with Django REST Framework and React.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![React](https://img.shields.io/badge/React-19.2-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## 📑 Table of Contents
1. [Overview & Features](#-features)
2. [Tech Stack](#-tech-stack)
3. [Project Structure](#-project-structure)
4. [Quick Start Guide](#-quick-start-guide)
5. [Deployment Guide](#-deployment-guide)
6. [Security Policy](#-security-policy)
7. [Contributing](#-contributing)
8. [Changelog](#-changelog)
9. [API Documentation](#-api-documentation)

---

## ✨ Features

### Core Features
- 🔐 **JWT Authentication** - Secure user authentication and authorization
- 👨‍🎓 **Student Management** - Track student profiles and academic records
- 🏢 **Company Database** - Maintain recruiting company information
- 📊 **Placement Tracking** - Record and monitor placement offers
- 📈 **Analytics Dashboard** - Real-time statistics and visualizations
- 📢 **Notifications** - Broadcast important updates

### Advanced Features
- 🤖 **AI Placement Predictor** - ML-powered placement probability predictions
- 💬 **Smart Chatbot** - Interactive placement assistant
- 🌓 **Dark Mode** - Complete theme support
- 📱 **Responsive Design** - Works on all devices
- 🎨 **Modern UI** - Beautiful, intuitive interface

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Django 5.0 + Django REST Framework
- **Authentication**: JWT (Simple JWT)
- **Database**: SQLite (dev) / PostgreSQL (production)
- **ML**: scikit-learn, pandas, numpy

### Frontend
- **Framework**: React 19.2
- **Routing**: React Router v7
- **Charts**: Chart.js, Recharts
- **HTTP Client**: Axios
- **Icons**: React Icons, Lucide React

---

## 📁 Project Structure

```
placement_portal/
├── core/                      # Main Django app
│   ├── models.py             # Database models
│   ├── views.py              # API views
│   ├── serializers.py        # DRF serializers
│   ├── auth_api.py           # Authentication endpoints
│   └── utils.py              # Utility functions
├── ml_model/                  # ML prediction app
│   ├── train_model.py        # Model training script
│   ├── views.py              # Prediction endpoints
│   └── placement_model.pkl   # Trained model
├── placement_portal/          # Django project settings
│   ├── settings.py           # Configuration
│   └── urls.py               # Main URL routing
├── frontend/                  # React application
│   ├── src/
│   │   ├── components/       # Reusable components
│   │   ├── pages/            # Page components
│   │   └── api.js            # API client
│   └── package.json
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 🚀 Quick Start Guide

Get the Placement Portal up and running in 5 minutes!

### Prerequisites
- Python 3.10 or higher
- Node.js 16 or higher
- npm or yarn

### automated Setup (Windows)
```bash
# Run setup script
setup.bat
```

### Manual Backend Setup (5 minutes)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Train ML model
python ml_model/train_model.py

# 7. Create admin user
python manage.py createsuperuser

# 8. Start server
python manage.py runserver
```

✅ Backend running at: http://127.0.0.1:8000

### Manual Frontend Setup (3 minutes)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
copy .env.example .env

# 4. Start development server
npm start
```

✅ Frontend running at: http://localhost:3000

---

## 🌐 Deployment Guide

This guide covers deploying the Placement Portal to production environments.

### Prerequisites (Production)
- Linux server (Ubuntu 20.04+ recommended)
- Domain name & SSL certificate
- PostgreSQL database
- Nginx & Gunicorn

### Production Configuration

1. **Environment Variables**: Update `.env` with production values:
   ```env
   SECRET_KEY=your-secure-secret-key
   DEBUG=False
   ALLOWED_HOSTS=yourdomain.com
   DATABASE_URL=postgresql://user:pass@localhost:5432/db
   ```

2. **Gunicorn Service**:
   Create `/etc/systemd/system/gunicorn.service`:
   ```ini
   [Service]
   User=www-data
   WorkingDirectory=/var/www/placement_portal
   ExecStart=/var/www/placement_portal/venv/bin/gunicorn --workers 3 --bind unix:/var/www/placement_portal/gunicorn.sock placement_portal.wsgi:application
   ```

3. **Nginx Configuration**:
   Create `/etc/nginx/sites-available/placement_portal`:
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com;
       location / { root /var/www/placement_portal/frontend_build; try_files $uri $uri/ /index.html; }
       location /api/ { proxy_pass http://unix:/var/www/placement_portal/gunicorn.sock; }
   }
   ```

See [DEPLOYMENT.md](DEPLOYMENT.md) (archived) for full details.

---

## 🔒 Security Policy

### Best Practices

1. **Never commit sensitive data** (API keys, passwords, .env files).
2. **Use environment variables** for all configuration.
3. **Keep dependencies updated** (`pip list --outdated`, `npm outdated`).
4. **Set DEBUG=False** in production.
5. **Use HTTPS** for all traffic.

### Known Security Considerations

- **JWT Tokens**: Stored in localStorage (consider httpOnly cookies for high security).
- **CORS**: Restricted in production.
- **Rate Limiting**: Recommended for production.

### Reporting Vulnerabilities
Email security@placementportal.com with details.

---

## 🤝 Contributing

We welcome contributions!

1. **Fork the repository**
2. **Create a branch** (`git checkout -b feature/AmazingFeature`)
3. **Make your changes**
4. **Test thoroughly**
5. **Commit** (`git commit -m 'Add AmazingFeature'`)
6. **Push** (`git push origin feature/AmazingFeature`)
7. **Open a Pull Request**

---

## 📝 Changelog

### [1.1.0] - 2025-11-30

#### Added
- ✅ Comprehensive error handling across all API endpoints
- ✅ Input validation for all models and serializers
- ✅ Environment variable management with python-decouple
- ✅ Security enhancements (CORS, CSRF, secure headers)
- ✅ ML model caching & enhanced prediction with confidence scores
- ✅ Pagination, search, and filtering
- ✅ Notification system

#### Changed
- 🔧 Enhanced authentication & settings configuration
- 🔧 Improved ML model training & evaluation
- 🔧 Refactored frontend API client

#### Fixed
- 🐛 Duplicate REST_FRAMEWORK config
- 🐛 ML model path resolution
- 🐛 CORS configuration

### [1.0.0] - Initial Release
- Basic student/company/placement management
- Statistics dashboard
- ML-based placement prediction
- JWT authentication

---

## 📚 API Documentation

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get current user

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get details

### Companies
- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create company

### ML Predictions
- `POST /api/ml/predict/` - Single prediction
- `GET /api/ml/model-info/` - Model information

For complete API documentation, visit: http://127.0.0.1:8000/swagger/

---

## 👥 Authors
- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments
- Django REST Framework team
- React team
- scikit-learn contributors
- All open-source contributors

## 🗺️ Roadmap

- [ ] Email notifications
- [ ] PDF report generation
- [ ] Advanced analytics
- [ ] Mobile application
- [ ] Interview scheduling
- [ ] Document management
- [ ] Multi-language support
- [ ] Role-based access control

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---
**Made with ❤️ for educational institutions**
