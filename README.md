# «Продуктовый помощник» — сайт Foodgram

![foodgram_workflow](https://github.com/bitcoineazy/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)
![Project website](https://img.shields.io/website-up-down-green-red/http/51.250.0.13.svg)

## Описание

- Проект <b>Foodgram</b> позволяет постить рецепты, делиться и скачивать списки продуктов

## Технологии
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)](https://nginx.org/ru/)
[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)](https://www.django-rest-framework.org/)
[![GitHub_Actions](https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)

## Установка и запуск
Проект разбит на 4 docker-контейнера:
- backend — бэкенд проекта
- frontend — фронтенд проекта
- postgres — образ базы данных PostgreSQL
- nginx — web-сервер nginx

1. Склонировать репозиторий: ```git clone git@github.com:bitcoineazy/foodgram-project-react.git```
2. Установить: [docker](https://www.docker.com/get-started), [docker-compose](https://docs.docker.com/compose/install/)
3. Перейти в директорию infra cобрать проект и запустить: ```sudo docker-compose up --build``` 
4. Собрать базу данных на основе ресурсов: ```sudo docker-compose exec backend python manage.py makemigrations && sudo docker-compose exec backend python manage.py migrate```
5. Создать профиль администратора: ```sudo docker-compose exec web python manage.py createsuperuser```
6. Собрать статику: ```sudo docker-compose exec web python manage.py collectstatic``` 

Для сборки и использования своего контейнера backend:
1. В директории backend/foodgram - ```sudo docker build -t username/container .```
2. Запушить образ на свой dockerhub - ```sudo docker push username/container```
3. Модифицировать infra/docker-compose.yml на свой контейнер

## Доступ к сайту и админке

- Foodgram находится по адресу: [51.250.0.13](http://51.250.0.13)
- Админ-зона находится на сервере [51.250.0.13/admin/](http://51.250.0.13/admin/) или локально [0.0.0.0/admin](https://0.0.0.0/admin)
- Данные для входа в админку ```login: admin@admin.com password: admin```

## Документация

- Находится на сервере [51.250.0.13/api/docs/redoc.html](http://51.250.0.13/api/docs/redoc.html) или локально [0.0.0.0//api/docs/redoc.html](https://0.0.0.0/api/docs/redoc.html)
- Каждый ресурс описан в документации: указаны эндпоинты (адреса, по которым можно сделать запрос), разрешённые типы запросов, права доступа и дополнительные параметры, если это необходимо.

## Автор

- Матвей Туголуков
- Задание было выполнено в рамках курса python-разработчик от Yandex.Praktikum 
