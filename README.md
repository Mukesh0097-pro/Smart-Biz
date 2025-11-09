# 🚀 SmartBiz AI - MSME Co-Pilot

> AI-powered business management assistant for Indian MSMEs

SmartBiz AI is an intelligent co-pilot that helps small and medium businesses automate invoicing, GST filing, compliance, and gain business insights through natural language conversations.

## ✨ Features

- 🤖 **AI Chat Assistant** - Natural language interface for business operations
- 📄 **Invoice Management** - Create, track, and send invoices automatically
- 📊 **Dashboard Analytics** - Real-time business insights and metrics
- 🏛️ **GST Automation** - Simplified GST filing and compliance
- 👥 **Customer Management** - Centralized database for customers and vendors
- 🔒 **Secure & Private** - All data encrypted and processed locally
- 🌐 **Multilingual Support** - English, Hindi, Tamil, and more
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 🛠️ Tech Stack

### Frontend
- **React** with TypeScript
- **Tailwind CSS** for styling
- **Axios** for API calls
- **React Router** for navigation

### Backend
- **FastAPI** (Python 3.10+)
- **PostgreSQL** with SQLAlchemy ORM
- **OpenAI API** for AI capabilities
- **Redis** for caching
- **Firebase Auth** for authentication

### Deployment
- **Vercel** for frontend
- **AWS/GCP/Render** for backend
- **Docker** for containerization

## 📁 Project Structure

```
SmartBiz/
├── backend/                 # FastAPI application
│   ├── api/                # API routes
│   ├── core/               # Config, security, database
│   ├── models/             # SQLAlchemy models
│   ├── services/           # Business logic
│   ├── orchestrator/       # AI task routing
│   ├── memory/             # Context management
│   └── main.py            # Entry point
│
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── services/      # API integration
│   │   └── styles/        # CSS files
│   └── package.json
│
├── .vscode/               # VS Code configuration
├── docker-compose.yml     # Docker setup
├── Dockerfile            # Backend container
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 16+
- PostgreSQL 15+
- Redis (optional, for caching)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Mukesh0097-pro/Smart-Biz.git
cd Smart-Biz
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

3. **Install backend dependencies**
```bash
cd backend
pip install -r requirements.txt
```

4. **Install frontend dependencies**
```bash
cd frontend
npm install
```

5. **Set up the database**
```bash
# Make sure PostgreSQL is running
# Create database: smartbiz
```

### Running the Application

#### Option 1: Using VS Code Tasks (Recommended)

1. Open the project in VS Code
2. Press `Ctrl+Shift+B` (or `Cmd+Shift+B` on Mac)
3. Select **"Run Both (SmartBiz Fullstack)"**

#### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

#### Option 3: Using Docker

```bash
docker-compose up --build
```

### Access the Application

- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/api/docs

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📚 API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### Main Endpoints

- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `POST /api/chat/query` - Send query to AI assistant
- `GET /api/dashboard/overview` - Get dashboard metrics
- `POST /api/invoices/create` - Create new invoice
- `GET /api/invoices/list` - List invoices
- `GET /api/gst/summary` - Get GST summary

## 🔧 Configuration

### Backend Configuration

Edit `backend/core/config.py` or set environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key
- `SECRET_KEY` - JWT secret key
- `REDIS_URL` - Redis connection string

### Frontend Configuration

Edit `frontend/src/services/api.ts`:

- `REACT_APP_API_URL` - Backend API URL

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- **Mukesh** - [Mukesh0097-pro](https://github.com/Mukesh0097-pro)

## 🙏 Acknowledgments

- OpenAI for GPT models
- FastAPI framework
- React and Tailwind CSS communities
- Indian MSME community for inspiration

## 📞 Support

For support, email support@smartbiz.ai or open an issue on GitHub.

---

**Made with ❤️ for Indian MSMEs**
