# Inventory Management & POS System with B2B Marketplace

A lightweight, POS-integrated inventory management system for retail stores and manufacturers, focusing on essential features for a quick and effective launch.

## Features

### Core Features (MVP)
- 📦 Inventory & POS Essentials
  - Barcode Scanning
  - Stock Tracking
  - User Roles & Access
- 🛒 B2B Marketplace
  - Product Listings
  - Direct Ordering
  - Order Management
- 📊 Business Insights & Reporting
  - Simple Dashboard
  - Basic Sales Reports
- 🔗 Integrations & Accessibility
  - POS System Compatibility
  - Cloud-Based Access

## Tech Stack
- Backend: Python with FastAPI
- Frontend: React with TypeScript
- Database: PostgreSQL
- Authentication: JWT
- ORM: SQLAlchemy

## Project Structure
```
inventory-pos-b2b/
├── backend/                 # FastAPI backend
│   ├── app/                # Application code
│   ├── tests/              # Backend tests
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend
│   ├── src/               # Source code
│   ├── public/            # Static files
│   └── package.json       # Node.js dependencies
└── docker/                # Docker configuration
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL 13+
- Docker (optional)

### Installation

#### Option 1: Using Docker (Recommended)
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd inventory-pos-b2b
   ```

2. Create a `.env` file in the backend directory:
   ```bash
   cp backend/.env.example backend/.env
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up -d
   ```

4. Run database migrations:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

The application will be available at:
- Backend API: http://localhost:8000
- Frontend: http://localhost:3000
- API Documentation: http://localhost:8000/docs

#### Option 2: Manual Installation

1. Set up the backend:
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Create and configure the database:
   ```bash
   createdb inventory_pos_b2b
   ```

3. Run database migrations:
   ```bash
   alembic upgrade head
   ```

4. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Set up the frontend:
   ```bash
   cd frontend
   npm install
   ```

6. Start the frontend development server:
   ```bash
   npm start
   ```

### Default Users
The system comes with three default users for testing:

1. Admin User
   - Email: admin@example.com
   - Password: admin123
   - Role: Admin

2. Store User
   - Email: store@example.com
   - Password: store123
   - Role: Store

3. Manufacturer User
   - Email: manufacturer@example.com
   - Password: manufacturer123
   - Role: Manufacturer

## API Documentation
Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Development

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Database Migrations
```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the LICENSE file for details. 