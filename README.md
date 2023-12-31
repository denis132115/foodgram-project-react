# praktikum_new_diplom
#### Проект «FOODGRAM»

"FOODGRAM" - это онлайн-сервис, созданный на базе Django Rest Framework, который предоставляет удобное пространство для обмена кулинарными рецептами и управления списками продуктов для приготовления блюд. Основная задача проекта - объединить любителей готовки и помочь им находить, сохранять и делиться своими любимыми кулинарными рецептами.

### Основные функции

-Рецепты в общем доступе: На платформе есть возможность создавать и делиться своими кулинарными рецептами, дополняя их красочными фотографиями и подробными описаниями. Это позволяет пользователям обмениваться кулинарными идеями и вдохновлять друг друга.

-Любимые рецепты: Пользователи могут добавлять рецепты других авторов в свой список избранных, чтобы легко находить их в будущем и сохранять самые понравившиеся кулинарные находки.

-Подписки на авторов: Сервис предоставляет возможность подписываться на других авторов, что позволяет пользователям быть в курсе обновлений и новых рецептов от своих любимых кулинаров.

-Список покупок: Один из важных функциональных элементов - это возможность создавать список продуктов, необходимых для приготовления выбранных блюд. Пользователи могут легко составлять список и загружать его в формате PDF, что делает покупки продуктов более удобными.

### Технологии

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=blue) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

### Создание Docker-образов

1.  Соберите образы локально(вместо username подставить логин Dockerhub):

    bash
    cd ../backend
    docker build -t username/foodgram_backend .
    cd frontend
    docker build -t username/foodgram_frontend .
    

2. Загрузите образы на DockerHub(вместо username подставить логин Dockerhub):

    bash
    docker push username/kittygram_backend
    docker push username/kittygram_frontend
    

_
### Деплой на сервере

1. Подключитесь к удаленному серверу

    bash
    ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера 
    

2. Создайте на сервере директорию foodgram через терминал

    bash
    mkdir foodgram
    

3. Установка docker compose на сервер:

    bash
    sudo apt update
    sudo apt install curl
    curl -fSL https://get.docker.com -o get-docker.sh
    sudo sh ./get-docker.sh
    sudo apt-get install docker-compose-plugin
    

4. В директорию foodgram/ скопируйте файлы docker-compose.production.yml и .env:

    bash
    scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
    * ath_to_SSH — путь к файлу с SSH-ключом;
    * SSH_name — имя файла с SSH-ключом (без расширения);
    * username — ваше имя пользователя на сервере;
    * server_ip — IP вашего сервера.
    

5. Запустите docker compose в режиме демона:

    bash
    sudo docker compose -f docker-compose.production.yml up -d
    

6. Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/static/:

    bash
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
    sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
    sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/static/
    

7. На сервере в редакторе nano откройте конфиг Nginx:

    bash
    sudo nano /etc/nginx/sites-enabled/default
    

8. Измените настройки location в секции server:

    bash
    server {

    location / {
        proxy_set_header Host $http_host;
        proxy_pass http://127.0.0.1:8000;
    }
    }

9. Проверьте работоспособность конфига Nginx:

    bash
    sudo nginx -t
    
    Если ответ в терминале такой, значит, ошибок нет:
    bash
    nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
    nginx: configuration file /etc/nginx/nginx.conf test is successful
    

10. Перезапускаем Nginx
    bash
    sudo service nginx reload

-После запуска проект будут доступен по адресу: http://localhost/    

## Доступ в админку
https://foodeat.ddns.net
login - admin
пароль - admin