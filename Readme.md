```markdown
# Blog API Project

This project is designed to develop a RESTful API for a blog application. Users can create, edit, delete, and comment on blog posts.

## Features

- User registration and login (JWT authentication)
- Create, list, update, and delete blog posts
- Comment on blog posts and manage comments
- View and update user profiles

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/harnkya/Blog-Management-API
   cd Blog-Management-API
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create the database:
   ```bash
   python manage.py migrate
   ```

5. Start the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### User Operations
- **Register**: `POST /api/register/`
- **View Profile**: `GET /api/profile/`
- **Update Profile**: `PUT /api/profile/`

### Blog Operations
- **List Blogs**: `GET /api/blogs/`
- **Create Blog**: `POST /api/blogs/`
- **Blog Details**: `GET /api/blogs/<id>/`
- **Update Blog**: `PUT /api/blogs/<id>/`
- **Delete Blog**: `DELETE /api/blogs/<id>/`

### Comment Operations
- **List Comments**: `GET /api/blogs/<blog_id>/comments/`
- **Create Comment**: `POST /api/blogs/<blog_id>/comments/`
- **Comment Details**: `GET /api/comments/<id>/`
- **Update Comment**: `PUT /api/comments/<id>/`
- **Delete Comment**: `DELETE /api/comments/<id>/`

## Technologies Used

- **Django**: Web framework
- **Django REST Framework**: API development
- **JWT**: Authentication

## Contributing

If you would like to contribute, please submit a pull request.

## License

This project is licensed under the MIT License.
```