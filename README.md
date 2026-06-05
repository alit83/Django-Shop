# Django Shop

A rendering web shop built with Django.

## Features

* Product management
* Category management
* User authentication
* Shopping cart
* Order management
* Admin dashboard
* Secure authentication and permissions

## Tech Stack

* Python
* Django
* PostgreSQL
* Docker
* Redis
* Celery
* gunicorn
* nginx


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

### Environment Variables

Create a `.env` file in Django-Shop:

```env
DEBUG=False
SHOW_DEBUGGER_TOOLBAR=False
ALLOWED_HOSTS=*
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'example@example.com'
EMAIL_HOST_PASSWORD = 'password'
EMAIL_USE_TLS=True
PGDB_NAME="postgres"
PGDB_USER="postgres"
PGDB_PASSWORD="postgres"
PGDB_HOST='db'
POSTGRES_PASSWORD='postgres'
```

### Start Docker Compose

```bash
docker compose -f docker-compose-prod.yml up -d
```


### Apply Migrations

```bash
docker compose -f docker-compose-prod.yml exec backend sh -c "python manage.py migrate"
```

### Create Superuser

```bash
docker compose -f docker-compose-prod.yml exec backend sh -c "python manage.py createsuperuser"
```



## Documentation

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

## License

MIT License

## Author

Ali Toosi

GitHub: https://github.com/alit83
