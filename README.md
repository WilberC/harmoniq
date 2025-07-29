# Harmoniq

A music streaming application with FastAPI backend and Vue frontend, featuring Tidal API integration.

## Project Structure

```
harmoniq/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── db/             # Database models and migrations
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI application entry point
│   ├── requirements.txt    # Python dependencies
│   └── alembic.ini        # Database migration configuration
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/     # Vue components
│   │   ├── views/          # Page views
│   │   ├── router/         # Vue router configuration
│   │   ├── store/          # Vuex store
│   │   └── main.js         # Vue application entry point
│   ├── package.json        # Node.js dependencies
│   └── vite.config.js      # Vite configuration
├── venv/                   # Python virtual environment
└── README.md              # This file
```

## Prerequisites

- Python 3.9.18
- Node.js 16+ and npm
- SQLite3

## Setup Instructions

### Backend Setup

1. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On macOS/Linux
   # or
   .\venv\Scripts\activate   # On Windows
   ```

2. Install Python dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Initialize the database:
   ```bash
   alembic upgrade head
   ```

4. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`
API documentation at `http://localhost:8000/docs`

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## Environment Variables

Create a `.env` file in the backend directory with:

```env
DATABASE_URL=sqlite:///./harmoniq.db
TIDAL_CLIENT_ID=your_tidal_client_id
TIDAL_CLIENT_SECRET=your_tidal_client_secret
SECRET_KEY=your_secret_key_here
```

## Features

- FastAPI backend with SQLite database
- Vue.js frontend with Vite
- Tidal API integration (to be implemented)
- RESTful API design
- Modern UI/UX

## Development

- Backend API runs on port 8000
- Frontend development server runs on port 5173
- Database file: `harmoniq.db` (created automatically) 