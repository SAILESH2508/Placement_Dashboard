# 🎓 Placement Portal

A comprehensive AI-powered placement management system for educational institutions built with Django REST Framework and React.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)
![React](https://img.shields.io/badge/React-19.2-61DAFB.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

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

## 📋 Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- npm or yarn

## 🚀 Quick Start

### Backend Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/placement-portal.git
cd placement-portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Train ML model
python ml_model/train_model.py

# (Optional) Load sample data
python manage.py populate_sample_data

# Run development server
python manage.py runserver
```

Backend will be available at: http://127.0.0.1:8000

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# Start development server
npm start
```

Frontend will be available at: http://localhost:3000

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

## 🔑 Default Credentials

### Sample Users (after loading sample data)
- **Username**: student1, student2, etc.
- **Password**: password123

### Admin Panel
- Create your own superuser with: `python manage.py createsuperuser`
- Access at: http://127.0.0.1:8000/admin/

## 📊 ML Model

The placement prediction model uses Random Forest classification with:
- **Accuracy**: 75%
- **Features**: CGPA, Internships, Projects, Communication Skills
- **Training Data**: 200+ samples

### Training the Model

```bash
python ml_model/train_model.py
```

### Making Predictions

Navigate to the AI Predictor page or use the API:

```bash
POST /api/ml/predict/
{
    "cgpa": 8.5,
    "internships": 2,
    "projects": 3,
    "communication": 8
}
```

## 🎨 Screenshots

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)

### AI Predictor
![AI Predictor](docs/screenshots/ml-predictor.png)

### Dark Mode
![Dark Mode](docs/screenshots/dark-mode.png)

## 📚 API Documentation

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/me/` - Get current user

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student

### Companies
- `GET /api/companies/` - List all companies
- `POST /api/companies/` - Create company
- `GET /api/companies/top/` - Get top recruiting companies

### Placements
- `GET /api/placements/` - List all placements
- `POST /api/placements/` - Create placement
- `GET /api/placements/{id}/` - Get placement details

### ML Predictions
- `POST /api/ml/predict/` - Single prediction
- `POST /api/ml/batch-predict/` - Batch predictions
- `GET /api/ml/model-info/` - Model information

For complete API documentation, visit: http://127.0.0.1:8000/swagger/

## 🌐 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure email settings
- [ ] Set up static file serving
- [ ] Enable HTTPS
- [ ] Configure CORS properly

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## 🔒 Security

- JWT-based authentication
- Password hashing with Django's built-in system
- CORS protection
- CSRF protection
- SQL injection prevention (Django ORM)
- XSS protection
- Environment variable management

See [SECURITY.md](SECURITY.md) for security guidelines.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- Your Name - [GitHub](https://github.com/yourusername)

## 🙏 Acknowledgments

- Django REST Framework team
- React team
- scikit-learn contributors
- All open-source contributors

## 📞 Support

For issues and questions:
- Create an issue on [GitHub](https://github.com/yourusername/placement-portal/issues)
- Email: your.email@example.com

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
