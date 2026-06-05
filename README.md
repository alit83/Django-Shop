# Django Shop

A modern e-commerce backend built with Django and Django REST Framework.

## Features

* Product management
* Category management
* User authentication
* Shopping cart
* Order management
* RESTful API
* Admin dashboard
* Secure authentication and permissions

## Tech Stack

* Python
* Django
* Django REST Framework
* PostgreSQL
* Docker
* Redis
* Celery

## API Features

* User registration and authentication
* Product CRUD operations
* Category CRUD operations
* Shopping cart management
* Order creation and tracking
* Search and filtering
* Pagination

## Project Structure

```text
core/
├── accounts/
├── core/
├── shop/
├── dashboard/
├── media/
├── order/
├── payment/
├── cart/
├── review/
├── staticfiles/
├── templates/
├── website/
└── manage.py
```

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/Django-Shop.git
cd Django-Shop
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file:

```env
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://user:password@localhost/dbname
```

### Apply Migrations

```bash
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

### Run Development Server

```bash
python manage.py runserver
```

## API Documentation

Available at:

```text
/api/docs/
```

## Admin panel



https://github.com/user-attachments/assets/bd2d5ace-760e-48d1-b303-2bbbe747cec7



## Testing

```bash
pytest
```

## Future Improvements

* Payment gateway integration
* Wishlist
* Product reviews
* Email notifications
* Docker deployment
* CI/CD pipeline

## License

MIT License

## Author

Ali Toosi

GitHub: https://github.com/alit83
