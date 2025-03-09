# Spirit11 Fantasy Cricket - Backend API

This repository contains the backend API service for the Spirit11 Fantasy Cricket application. The backend is built using FastAPI and provides the necessary endpoints to power the fantasy cricket platform.

## Tech Stack

- Python 3.13
- FastAPI
- MongoDB (via motor)
- OpenAI API integration

## Prerequisites

- Python 3.13 or higher
- uv
- MongoDB instance (local or remote)
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/SpiritX_CodeChefs_02.git
cd SpiritX_CodeChefs_02/backend
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
uv sync
```

## Environment Setup

1. Create a .env file by copying the example:

```bash
cp .env.example .env
```

2. Update the .env file with your configuration:

```bash
OPENAI_API_KEY=your_openai_api_key
# Add other environment variables as needed
```

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
