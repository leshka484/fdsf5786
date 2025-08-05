# Развёртывание Django проекта на сервере с использованием Nginx и uWSGI

## 1. Установка зависимостей

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx uwsgi uwsgi-plugin-python3 -y
```

## 2. Клонирование проекта и установка Python-зависимостей

```bash
git clone https://github.com/leshka484/fdsf5786.git
cd fdsf5786
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Конфигурация переменных окружения

Создайте файл `.env` в корне проекта:

```
DB_NAME= Название БД
DB_USER= Имя пользователя БД
DB_PASSWORD= Пароль БД
DB_HOST=localhost
SECRET_KEY= Секретный ключ для Django
```

## 4. Создание миграций в БД

```bash
python manage.py migrate
```

## 5. Сборка статических файлов

```bash
python manage.py collectstatic
```

## 6. Настройка uWSGI

Создайте файл `/etc/uwsgi/apps-available/jsonloader.ini`:

```ini
[uwsgi]
chdir = Путь к проекту
module = jsonloader.wsgi:application
home = Путь к виртуальному окружению

master = true
processes = 5
enable-threads = true
plugin = python3

uid = www-data
gid = www-data

socket = /run/uwsgi/jsonloader.sock
chown-socket = www-data:www-data
chmod-socket = 660
vacuum = true

die-on-term = true
```

Создайте символическую ссылку:

```bash
sudo ln -s /etc/uwsgi/apps-available/jsonloader.ini /etc/uwsgi/apps-enabled/
sudo systemctl restart uwsgi
```
Опционально можно проверить создался ли сокет:

```bash
ls -l /run/uwsgi/jsonloader.sock
```

## 7. Настройка Nginx

Создайте файл `/etc/nginx/sites-available/jsonloader`:

```nginx
server {
    listen 80;
    server_name localhost;

    location /static/ {
        alias папка_проекта/static/;
    }

    location /media/ {
        alias папка_проекта/media/;
    }

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/run/uwsgi/jsonloader.sock;
    }
}
```

Активируйте сайт:

```bash
sudo ln -s /etc/nginx/sites-available/jsonloader /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

## Дополнительно

Также пользователь или группа www-data должны иметь доступ на чтение и выполнение файлов конфигурации nginx и uwsgi, а также файлов проекта Django 

---

Теперь Django-проект доступен по IP-адресу или домену, настроенному в конфиге Nginx.
