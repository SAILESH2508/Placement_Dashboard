# 🚀 Quick Start Guide

Get the Placement Portal up and running in 5 minutes!

## Prerequisites Check

```bash
# Check Python (need 3.10+)
python --version

# Check Node.js (need 16+)
node --version

# Check npm
npm --version
```

## Option 1: Automated Setup (Recommended)

### Windows
```bash
# Run setup script
setup.bat

# Follow the prompts
```

### Linux/Mac
```bash
# Make script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

## Option 2: Manual Setup

### Step 1: Backend Setup (5 minutes)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 5. Run migrations
python manage.py migrate

# 6. Train ML model
python ml_model/train_model.py

# 7. Create admin user
python manage.py createsuperuser
# Enter username, email, and password when prompted

# 8. (Optional) Load sample data
python manage.py populate_sample_data

# 9. Start server
python manage.py runserver
```

✅ Backend running at: http://127.0.0.1:8000

### Step 2: Frontend Setup (3 minutes)

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install

# 3. Create .env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac

# 4. Start development server
npm start
```

✅ Frontend running at: http://localhost:3000

## 🎉 You're Done!

### Access Points

1. **Frontend Application**
   - URL: http://localhost:3000
   - Login with created user or sample data users

2. **Backend API**
   - URL: http://127.0.0.1:8000/api/
   - Swagger Docs: http://127.0.0.1:8000/swagger/

3. **Admin Panel**
   - URL: http://127.0.0.1:8000/admin/
   - Login with superuser credentials

### Sample Data Credentials

If you loaded sample data:
- **Username**: student1, student2, student3, ...
- **Password**: password123

## 🧪 Quick Test

### Test Backend API

```bash
# Test login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"student1\",\"password\":\"password123\"}"
```

### Test ML Prediction

```bash
# Get token first (from login response)
# Then test prediction
curl -X POST http://127.0.0.1:8000/api/ml/predict/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"cgpa\":8.5,\"internships\":2,\"projects\":3,\"communication\":8}"
```

## 🐛 Common Issues

### Issue: "Module not found: decouple"
```bash
pip install python-decouple
```

### Issue: "Port already in use"
```bash
# Backend (use different port)
python manage.py runserver 8001

# Frontend (will prompt for different port)
# Press 'Y' when asked
```

### Issue: "Database locked"
```bash
# Close any other Django processes
# Delete db.sqlite3 and run migrations again
python manage.py migrate
```

### Issue: "ML model not found"
```bash
# Train the model
python ml_model/train_model.py
```

### Issue: "CORS error in frontend"
```bash
# Check backend is running
# Check CORS settings in settings.py
# Ensure frontend is using correct API URL
```

## 📚 Next Steps

1. **Explore the Application**
   - Browse students, companies, placements
   - Try the ML prediction feature
   - Check statistics dashboard

2. **Read Documentation**
   - [README.md](README.md) - Full documentation
   - [API_DOCUMENTATION.md](API_DOCUMENTATION.md) - API reference
   - [SECURITY.md](SECURITY.md) - Security guidelines

3. **Customize**
   - Update .env with your settings
   - Modify branding in frontend
   - Add your institution's data

4. **Deploy**
   - Read [DEPLOYMENT.md](DEPLOYMENT.md)
   - Set up production environment
   - Configure domain and SSL

## 🆘 Need Help?

1. Check [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for detailed changes
2. Review [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for API details
3. Check logs in `logs/django.log`
4. Review browser console for frontend errors

## 🎯 Quick Commands Reference

### Backend
```bash
# Run server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py populate_sample_data

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Train ML model
python ml_model/train_model.py

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check
```

### Frontend
```bash
# Start dev server
npm start

# Build for production
npm run build

# Run tests
npm test

# Check for updates
npm outdated
```

## ✅ Verification Checklist

- [ ] Backend server running on port 8000
- [ ] Frontend server running on port 3000
- [ ] Can access admin panel
- [ ] Can login to frontend
- [ ] Can view students list
- [ ] Can view companies list
- [ ] Can view placements
- [ ] ML prediction works
- [ ] Statistics dashboard loads

---

**Estimated Setup Time**: 5-10 minutes

**Status**: Ready to use! 🎉

For detailed information, see [README.md](README.md)
