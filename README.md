# Book Management System

A feature-rich FastAPI application for managing books with PostgreSQL backend.

## 🛠 Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: asyncpg
- **Migrations**: Alembic
- **Testing**: pytest
- **Containerization**: Docker

## 🏃‍♂️ Quick Start

### Prerequisites
- Docker
- Docker Compose

### Setup

```bash
# Clone repository
git clone <repository-url>
cd book_management_system
```

Set Up Environment Variables: Create a .env file in the project root with the following variables or download from the Google Drive:

```
DB_USER="book_admin"
DB_PASSWORD="secure_password_123"
DB_HOST="localhost"
DB_NAME="book_management_db"
DB_PORT="5432"
SECRET_KEY="mySuperSecretKey12345"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES="30"
REFRESH_TOKEN_EXPIRE_DAYS="7"
ENVIRONMENT="development"
```

# Build and run
```bash
docker-compose up --build
```

## 📚 Core Features

- User Authentication (JWT)
- Book CRUD Operations
- Author Management
- Genre Classification
- Search and Filtering

## 🗄 Database Setup

```bash
# Generate migration
alembic revision --autogenerate -m "description"

# Run migrations
alembic upgrade head
```

## 📝 Requirements

```
alembic==1.14.1
annotated-types==0.7.0
anyio==4.8.0
asyncpg==0.30.0
bcrypt==4.2.1
certifi==2024.12.14
click==8.1.8
colorama==0.4.6
fastapi==0.115.7
fuzzywuzzy==0.18.0
greenlet==3.1.1
h11==0.14.0
httpcore==1.0.7
httptools==0.6.4
httpx==0.28.1
idna==3.10
iniconfig==2.0.0
Mako==1.3.8
MarkupSafe==3.0.2
packaging==24.2
passlib==1.7.4
pluggy==1.5.0
pydantic==2.10.6
pydantic-settings==2.7.1
pydantic_core==2.27.2
PyJWT==2.10.1
pytest==8.3.4
python-dotenv==1.0.1
python-multipart==0.0.20
PyYAML==6.0.2
sniffio==1.3.1
SQLAlchemy==2.0.37
starlette==0.45.3
typing_extensions==4.12.2
uvicorn==0.34.0
watchfiles==1.0.4
websockets==14.2
```

## 🧪 Testing

Not implemented

