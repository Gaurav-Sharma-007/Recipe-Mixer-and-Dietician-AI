# Recipe Remix API

An AI-powered recipe suggestion backend that helps you create meals based on the ingredients you have in your pantry.

## Features

- **Authentication**: Secure user registration and login.
- **Pantry Management**: Keep track of ingredients you currently have.
- **Recipe Suggestions**: Get AI-powered recipe ideas based on your available ingredients.
- **Meal Planning**: Plan your meals for the week.
- **Shopping List**: Automatically generate shopping lists for missing ingredients.
- **Nutrition Information**: Access nutritional data for suggested recipes.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.11
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Containerization**: Docker & Docker Compose

## Prerequisites

- Docker and Docker Compose
- Or Python 3.11+ and a running PostgreSQL instance

## Getting Started (Docker)

The easiest way to run the API is using Docker Compose.

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd "Recipe Remix API"
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```
   *Edit `.env` to add your specific configuration (like API keys if needed).*

3. Start the application:
   ```bash
   docker-compose up --build
   ```

4. The API will be available at `http://localhost:8000`.
   - Interactive API documentation (Swagger UI): `http://localhost:8000/docs`
   - ReDoc documentation: `http://localhost:8000/redoc`

## Getting Started (Local Development)

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your `.env` file and ensure your local PostgreSQL database is running with credentials matching `DATABASE_URL` in `.env`.

4. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Project Structure

```text
.
├── app/
│   ├── main.py          # FastAPI application instance and routing
│   ├── config.py        # Environment variables and settings
│   ├── database.py      # SQLAlchemy setup
│   ├── models/          # Database models
│   ├── routers/         # API endpoints (auth, pantry, recipes, etc.)
│   ├── schemas/         # Pydantic models for validation
│   ├── services/        # Business logic and external API integrations
│   └── utils/           # Helper functions
├── Dockerfile           # Docker configuration for the API
├── docker-compose.yml   # Multi-container orchestration
├── requirements.txt     # Python dependencies
└── tests/               # Test suite
```

## API Endpoints

Once the application is running, check the `/docs` route for a comprehensive and interactive list of all available endpoints. Key routing prefixes include:

- `/auth` - User authentication
- `/pantry` - Manage user pantry items
- `/recipes` - Discover and manage recipes
- `/nutrition` - Nutritional analysis
- `/shopping-list` - Manage shopping lists
- `/meal-plan` - User meal planning
