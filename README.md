Запуск приложения:
1) С помощью Dockerfile:  
    1) `docker build -t app .`  

    2) Запуск
    ```
    docker run -p 8080:8080 \
    -e POSTGRES_DATABASE='tender' \
    -e POSTGRES_HOST='localhost' \
    -e POSTGRES_USERNAME='postgres' \
    -e POSTGRES_PASSWORD='postgres' \
    -e POSTGRES_PORT='5432' \
    app
    ```

    Либо с помощью .env файла:
    `docker run --env-file .env -p 8080:8080 app`

2) Бэк вне docker-контейнера:  

    Первоначально необходимо выолнить `poetry install`, `poetry shell`

    (Если нужна база локально:  
    Чтобы создать базу и заполнить ее тестовыми данными: `make db`, `make migrate`, `make insert`)

    Чтобы запустить приложение, необходимо выполнить: `make run`

 

При запуске приложения автоматически выполняются миграции

Выполнены все доп. требования  

В качестве линтера и форматтера использовался ruff со стандартными настройками  

Запуск форматтера: `make format`  
Запуск линтера: `make lint`

Swagger доступен по адресу: `/api/docs`