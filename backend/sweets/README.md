# 🍬 Sweet Shop Management System

A full-stack web application for managing a sweet shop with user authentication, inventory management, and admin features.

## 🎯 Features

- **User Authentication**: Register, login with JWT tokens
- **Browse Sweets**: View all available sweets with details
- **Search & Filter**: Search by name or category
- **Purchase**: Buy sweets and track inventory
- **Admin Features**:
  - Add new sweets
  - Edit existing sweets
  - Delete sweets
  - Restock inventory
- **Responsive Design**: Beautiful UI with Tailwind CSS

## 🛠️ Tech Stack

### Backend
- **Django 4.2.7**: Web framework
- **Django REST Framework**: API development
- **Django Simple JWT**: Authentication
- **SQLite**: Database
- **pytest**: Testing

### Frontend
- **React 18**: UI library
- **Vite**: Build tool
- **Tailwind CSS**: Styling
- **Lucide React**: Icons
- **Fetch API**: HTTP requests

## 📦 Installation & Setup

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Backend Setup
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Backend runs at: `http://localhost:8000`

### Frontend Setup
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs at: `http://localhost:5173`

## 🧪 Running Tests

### Backend Tests
```bash
cd backend
pytest -v
pytest --cov=. --cov-report=html
```

### Test Coverage
After running tests with coverage, open `htmlcov/index.html` in your browser.

## 📸 Screenshots

### Login Page
![Login Page](screenshots/login.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Admin Features
![Admin Panel](screenshots/admin.png)

## 🔑 API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login user
- `POST /api/auth/token/refresh/` - Refresh JWT token

### Sweets (Protected)
- `GET /api/sweets/` - List all sweets
- `POST /api/sweets/` - Create sweet (Admin only)
- `GET /api/sweets/:id/` - Get sweet details
- `PUT /api/sweets/:id/` - Update sweet (Admin only)
- `DELETE /api/sweets/:id/` - Delete sweet (Admin only)
- `GET /api/sweets/search/` - Search sweets
- `POST /api/sweets/:id/purchase/` - Purchase sweet
- `POST /api/sweets/:id/restock/` - Restock sweet (Admin only)

## 👥 User Roles

### Regular User
- View all sweets
- Search sweets
- Purchase sweets

### Admin User
- All regular user permissions
- Add new sweets
- Edit existing sweets
- Delete sweets
- Restock inventory

## 🤖 My AI Usage

This project was developed with assistance from AI tools as part of a TDD (Test-Driven Development) kata assignment.

### AI Tools Used
- **Claude (Anthropic)**: Primary AI assistant for code generation, debugging, and architecture decisions
- **GitHub Copilot**: Code completion and suggestions

### How AI Was Used

1. **Project Architecture**
   - Used Claude to design the overall project structure
   - Got suggestions for Django app organization and React component hierarchy
   - Discussed best practices for REST API design

2. **Backend Development**
   - AI helped generate initial Django models, serializers, and views
   - Used AI to write test cases following TDD principles
   - Got assistance with JWT authentication setup and CORS configuration

3. **Frontend Development**
   - Claude generated the initial React component structure
   - AI helped with Tailwind CSS styling and responsive design
   - Used AI for state management patterns and API integration

4. **Testing**
   - AI assisted in writing comprehensive pytest test cases
   - Got help structuring tests for different user roles and permissions
   - Used AI to ensure good test coverage

5. **Debugging**
   - AI helped troubleshoot migration issues
   - Got assistance with CORS errors and authentication problems
   - Used AI to fix styling issues with Tailwind CSS

6. **Documentation**
   - AI helped structure this README
   - Got assistance with clear setup instructions
   - Used AI to document API endpoints and features

### My Contributions
While AI provided significant assistance, I was responsible for:
- Understanding and implementing the TDD workflow
- Making architectural decisions and choosing technologies
- Manually testing all features in the browser
- Debugging and fixing issues that AI-generated code had
- Customizing the UI design and user experience
- Managing the Git workflow and commits
- Understanding how all pieces fit together

### Reflection on AI Usage
Using AI significantly accelerated development, especially for boilerplate code and test generation. However, I still needed to:
- Understand the code being generated
- Debug issues when AI suggestions didn't work
- Make decisions about what suggestions to accept or modify
- Test thoroughly to ensure everything worked correctly
- Learn the underlying technologies and concepts

AI was a powerful tool, but understanding the fundamentals remained essential for successful project completion.

## 🚀 Deployment

### Backend Deployment (Heroku)
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create new app
heroku create sweet-shop-backend

# Add PostgreSQL
heroku addons:create heroku-postgresql:mini

# Set environment variables
heroku config:set DJANGO_SETTINGS_MODULE=sweet_shop.settings
heroku config:set SECRET_KEY=your-secret-key

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Frontend Deployment (Vercel)
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel

# Follow prompts and deploy
```

## 📁 Project Structure
```
sweet-shop/
├── backend/
│   ├── authentication/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   ├── sweets/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── permissions.py
│   │   └── tests/
│   ├── sweet_shop/
│   │   ├── settings.py
│   │   └── urls.py
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── index.html
│   └── package.json
└── README.md
```

## 🐛 Known Issues
- None currently

## 🔮 Future Enhancements
- Shopping cart functionality
- Order history
- Payment integration
- Email notifications
- Advanced analytics dashboard
- Multi-language support

## 👨‍💻 Author
[Your Name]

## 📄 License
MIT License

## 🙏 Acknowledgments
- Anthropic Claude for AI assistance
- Django and React communities
- TDD kata assignment for the project idea