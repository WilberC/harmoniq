# Harmoniq

A music playlist management web application with a macOS Finder-like interface, built with Django, Tailwind CSS, and Unpoly for progressive enhancement.

## Features

- 🎵 Music playlist management with drag-and-drop functionality
- 🖥️ macOS Finder-inspired interface
- 🔄 Progressive enhancement with Unpoly
- 🎨 Modern UI with Tailwind CSS
- 🔐 OAuth integration with Tidal and Spotify
- 📱 Responsive design
- ⚡ AJAX-based navigation

## Tech Stack

- **Backend**: Django 5.0 with Django REST Framework
- **Database**: SQLite
- **Frontend**: Tailwind CSS, Unpoly, Sortable.js
- **Package Management**: Poetry
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

6. Install and build Tailwind CSS:
```bash
python manage.py tailwind install
python manage.py tailwind build
```

7. Run the development server:
```bash
python manage.py runserver
```

8. In a separate terminal, run Tailwind in watch mode:
```bash
python manage.py tailwind start
```

### Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Music API Credentials
TIDAL_CLIENT_ID=your-tidal-client-id
TIDAL_CLIENT_SECRET=your-tidal-client-secret
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret
```

## Project Structure

```
harmoniq/
├── harmoniq/                 # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── music/                    # Music app
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── api.py
│   └── templates/
├── static/                   # Static files
│   ├── css/
│   ├── js/
│   └── images/
├── templates/                # Base templates
├── manage.py
├── pyproject.toml
└── README.md
```

## Usage

1. Visit `http://localhost:8000` to access the application
2. Create playlists and add tracks
3. Use drag-and-drop to reorder tracks within playlists
4. Move tracks between playlists by dragging them
5. Connect to music services via OAuth

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black .
```

### Linting
```bash
flake8
```

## License

MIT License