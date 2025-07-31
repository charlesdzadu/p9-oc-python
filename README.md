# Books Review - Django Web Application

A comprehensive book review platform built with Django that allows users to request and share book reviews in a social networking environment.

## 📖 Overview

Books Review is a social platform where users can:
- Create review requests ("tickets") for books they want others to review
- Write detailed reviews with star ratings for any book ticket
- Follow other users to stay updated on their reviews
- Manage their content through a personal dashboard
- Interact with a community of book enthusiasts

## ✨ Features

### 🔐 Authentication System
- User registration and login
- Secure authentication with Django's built-in system
- Custom user model for extensibility
- Protected routes requiring authentication

### 📚 Ticket System
- Create review requests with book title, description, and optional cover image
- Edit and delete your own tickets
- Browse all community tickets
- Image upload support for book covers

### ⭐ Review System
- Write reviews with 1-5 star ratings
- Add headlines and detailed review text
- Create standalone reviews (ticket + review in one step)
- Edit and delete your own reviews
- One review per user per book ticket

### 👥 Social Features
- Follow/unfollow other users
- View followers and following lists
- Social feed showing all community activity
- User subscriptions management

### 📊 Dashboard
- Personal dashboard showing your tickets and reviews
- Chronological timeline of your activity
- Easy access to edit/delete your content

## 🛠 Tech Stack

- **Backend**: Django 5.2.4
- **Frontend**: Django Templates with HTML/CSS
- **Database**: SQLite (development)
- **Image Processing**: Pillow
- **Dependency Management**: Poetry
- **Python**: 3.12+

## 📋 Prerequisites

- Python 3.12 or higher
- Poetry (for dependency management)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd p9-oc-python
   ```

2. **Install dependencies using Poetry:**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment:**
   ```bash
   poetry shell
   ```

4. **Navigate to the Django project directory:**
   ```bash
   cd books_review
   ```

5. **Apply database migrations:**
   ```bash
   poetry run python manage.py migrate
   ```

6. **Create a superuser (optional):**
   ```bash
   poetry run python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   poetry run python manage.py runserver
   ```

8. **Open your browser and navigate to:**
   ```
   http://127.0.0.1:8000
   ```

## 📁 Project Structure

```
books_review/
├── authentication/           # User authentication app
│   ├── models.py            # Custom User model
│   ├── views.py             # Auth views (login, register, follow)
│   ├── forms.py             # Authentication forms
│   ├── urls.py              # Auth URL patterns
│   └── templates/           # Auth templates
├── reviews/                 # Main reviews app
│   ├── models.py            # Ticket, Review, UserFollows models
│   ├── views.py             # CRUD views for tickets and reviews
│   ├── forms.py             # Review and ticket forms
│   ├── urls.py              # Review URL patterns
│   └── templates/reviews/   # Review templates
├── books_review/            # Django project settings
│   ├── settings.py          # Main settings
│   ├── urls.py              # Root URL configuration
│   └── wsgi.py              # WSGI configuration
├── media/                   # User uploaded images
│   └── ticket_images/       # Book cover images
├── manage.py                # Django management script
└── db.sqlite3              # SQLite database (created after migration)
```

## 📱 Usage

### Getting Started
1. **Register an account** or log in if you already have one
2. **Explore the feed** to see what books others are discussing
3. **Create a ticket** to request a review for a book you want opinions on
4. **Write reviews** for books that interest you
5. **Follow users** whose opinions you value

### Creating Content

**Create a Ticket (Review Request):**
- Click "Créer un ticket" on the home page
- Add book title, description, and optional cover image
- Submit to share with the community

**Write a Review:**
- Find a ticket you want to review
- Click "Créer une critique" 
- Rate the book (1-5 stars) and write your review
- Or create a standalone review with both ticket and review

**Manage Your Content:**
- Visit your dashboard to see all your posts
- Edit or delete your tickets and reviews
- Track your activity over time

### Social Features

**Following Users:**
- Go to "Abonnements" to manage subscriptions
- Search for users by username to follow them
- View your followers and who you're following
- Unfollow users when needed

## 🔧 Development

### Running Tests
```bash
poetry run python manage.py test
```

### Creating Migrations
```bash
poetry run python manage.py makemigrations
poetry run python manage.py migrate
```

### Collecting Static Files (for production)
```bash
poetry run python manage.py collectstatic
```

### Admin Interface
Access the Django admin at `http://127.0.0.1:8000/admin/` with your superuser credentials.

## 📊 Database Models

### User
- Extends Django's AbstractUser
- Used for authentication and content ownership

### Ticket
- Book review requests
- Contains title, description, image, and timestamps
- Linked to User (owner)

### Review
- Book reviews with star ratings
- Contains headline, body text, rating (0-5)
- Linked to Ticket and User

### UserFollows
- Manages user-to-user following relationships
- Prevents duplicate follows with unique constraints

## 🎨 Frontend

The application uses Django templates with a clean, responsive design:
- Bootstrap-based styling (based on template structure)
- Mobile-friendly responsive layout
- French language interface
- Intuitive navigation and user experience

## 🔒 Security Features

- CSRF protection on all forms
- User authentication required for all main features
- Authorization checks (users can only edit/delete their own content)
- Secure file upload handling for images
- Django's built-in security features

## 🌐 URLs

### Authentication
- `/auth/login/` - User login
- `/auth/register/` - User registration
- `/auth/logout/` - User logout
- `/auth/dashboard/` - User dashboard
- `/auth/subscriptions/` - Manage user follows

### Reviews
- `/` - Home feed
- `/ticket/create/` - Create ticket
- `/ticket/<id>/edit/` - Edit ticket
- `/ticket/<id>/delete/` - Delete ticket
- `/review/<ticket_id>/create/` - Create review for ticket
- `/review/create/` - Create standalone review
- `/review/<id>/edit/` - Edit review
- `/review/<id>/delete/` - Delete review

## 🚀 Deployment

For production deployment:

1. Update `settings.py` for production:
   - Set `DEBUG = False`
   - Configure `ALLOWED_HOSTS`
   - Use a production database (PostgreSQL recommended)
   - Set up proper static file serving

2. Set environment variables:
   - `SECRET_KEY`
   - Database credentials
   - Static/media file storage settings

3. Use a production WSGI server like Gunicorn
4. Set up a reverse proxy (Nginx)
5. Configure HTTPS

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is part of an OpenClassrooms Bachelor program (Project P9).


