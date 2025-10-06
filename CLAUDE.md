# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Django 5.2.6 web application for industrial safety, written in Russian. The project name is `indastrialSafety` (note the typo in the module name) and uses SQLite for the database.

## Key Commands

### Development Server
```bash
python manage.py runserver
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Django Shell
```bash
python manage.py shell
```

## Architecture

### Django Project Structure
- **Main project module**: `indastrialSafety` (settings.py, urls.py, wsgi.py, asgi.py)
- **Apps**:
  - `landing`: Homepage/landing page app that displays the latest 3 news items
  - `news`: News management app with list and detail views

### URL Routing
- `/` → Landing page (shows latest 3 news)
- `/news/` → Paginated news list (5 items per page)
- `/news/<id>/` → Individual news detail page
- `/admin/` → Django admin panel

### Models
- **News** (news/models.py:3): Main content model with fields:
  - title, description, image, category (seminar/career choices)
  - created_at timestamp with auto-ordering by newest first
  - Custom `russian_date()` method for Russian date formatting

### Static Files & Frontend
- Static files are stored in `landing/static/landing/`
- **SCSS source files**: `landing/static/landing/scss/` (organized into base/, index/, news/)
- **Compiled CSS**: `landing/static/landing/css/` (mirrors SCSS structure)
- When modifying styles, edit SCSS files and compile to CSS
- Static file structure:
  - `base/`: Header and footer styles
  - `index/`: Homepage-specific styles including news section
  - `news/`: List and detail page styles
  - `_variables.scss`: Shared SCSS variables

### Templates
- Each app uses its own templates directory:
  - `landing/templates/landing/`: base.html (base template), index.html
  - `news/templates/news/`: list.html, detail.html
- Base template provides common structure (header/footer) for inheritance

### Media Files
- User-uploaded files (news images) go to `/media/` directory
- News images specifically upload to `media/news/images/`

## Settings Notes
- Database: SQLite at `db.sqlite3`
- Settings module: `indastrialSafety.settings`
- Static files URL: `/static/`
- Media files URL: `/media/`
- DEBUG mode is currently ON (should be disabled in production)
- Language: Russian (models use Russian verbose names)
