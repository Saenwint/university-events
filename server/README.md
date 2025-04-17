### PostgreSQL
```bash
sudo apt-get install libpq-dev
pip install psycopg2
```

### PyZBAR
```bash
sudo apt install libzbar0 libzbar-dev
```

### Структура сервера

```
.
├── analytics - здесь будет аналитика по посещению мероприятий
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── app - главное приложение
│   ├── admin_access_middleware.py
│   ├── asgi.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── events - мероприятия
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── main - это для отрисовки главной страницы
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── __pycache__
│   ├── templates
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── media - здесь хранятся картинки для мероприятий
│   └── events
├── tickets - здесь должны генерироваться билеты и рассылаться по почтам пользователей при регистрации на мероприятие
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── users - здесь логика авторизации и регистрации пользователя с отправкой на почту пользователя email
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── __init__.py
    ├── migrations
    ├── models.py
    ├── __pycache__
    ├── templates
    ├── tests.py
    ├── tokens.py
    ├── urls.py
    ├── utils.py
    └── views.py
```