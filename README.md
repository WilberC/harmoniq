# Harmoniq

A music playlist management web application with a macOS Finder-like interface, built with Django, Tailwind CSS, and Unpoly for progressive enhancement.

## Features

- 🎵 Music playlist management with drag-and-drop functionality
- 🖥️ macOS Finder-inspired interface
- 🔄 Progressive enhancement with Unpoly
- 🎨 Modern UI with Tailwind CSS
- 🔐 OAuth integration with streaming services such as: Tidal, Spotify, Apple Music
- 📱 Responsive design
- ⚡ Seamless navigation with Unpoly (no page reloads)

## Tech Stack

- **Backend**: Django 5.0
- **Database**: SQLite
- **Frontend**: Tailwind CSS, Unpoly, Sortable.js
- **Package Management**: Poetry (Python), npm (Tailwind CSS)
- **Authentication**: OAuth for music services

## Setup

### Prerequisites

- Python 3.11+
- Poetry
- Node.js (for Tailwind CSS build)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd harmoniq
```

2. Install Python dependencies:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

4. Run database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Install Node.js dependencies for Tailwind CSS:
```bash
npm install
```

7. Build Tailwind CSS:
```bash
npm run build:css
```

8. Run the development server:
```bash
python manage.py runserver
```

9. In a separate terminal, run Tailwind in watch mode:
```bash
npm run watch:css
```

### Environment Variables

Create a `.env` file in the project root:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

**Note**: API credentials for music services (Tidal, Spotify, Apple Music) are stored securely in the database with proper hashing, not in environment variables.

## Project Structure

```
harmoniq/
├── harmoniq/                 # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── static/                   # Static files
│   ├── src/
│   │   └── index.css        # Tailwind CSS source
│   └── dist/
│       └── index.css        # Compiled Tailwind CSS
├── templates/                # Base templates
├── manage.py
├── pyproject.toml           # Python dependencies (Poetry)
├── package.json             # Node.js dependencies (Tailwind CSS only)
└── README.md
```

## Usage

1. **Add Streaming Accounts**: Connect your music streaming services (Tidal, Spotify, Apple Music) via OAuth
2. **View Current Playlists**: Browse and manage your existing playlists from connected services
3. **Search and Add Music**: Search for tracks across your connected services and add them to playlists
4. **Organize Playlists**: Use drag-and-drop to reorder tracks within playlists
5. **Cross-Platform Management**: Move tracks between playlists and across different streaming services

### Health Check

The application provides a health check endpoint at `/health/` that returns the service status:

```bash
curl http://localhost:8000/health/
```

Response:
```json
{
    "status": "healthy",
    "service": "harmoniq",
    "version": "1.0.0"
}
```

## Development

### Setup Development Environment

1. Install pre-commit hooks:
```bash
pre-commit install
```

2. Install all development dependencies:
```bash
poetry install --with dev
```

### Running Tests
```bash
pytest
```

### Code Quality Tools

#### Code Formatting
```bash
# Format code with Black
black .

# Sort imports with isort
isort .
```

#### Linting
```bash
# Run flake8
flake8
```

#### Pre-commit (Recommended)
```bash
# Run pre-commit on all files
pre-commit run --all-files

# Run pre-commit on staged files only
pre-commit run
```

### Tailwind CSS Development
```bash
# Watch for changes and rebuild CSS
npm run watch:css

# Build CSS for production
npm run build:css
```

## License

MIT License