# Блог 

## Локальное окружение разработки
В качестве интерпертатора IDE используется docker-compose:
* сервис - web
* интерпертатор - python
### Консольные команды для управления разработкой
* первичный запуск проект
```commandline
docker-compose up -d --build
```
* каждый последующий запуск проекта
```commandline
docker-compose up -d
```
* пересобрать, например для установки новой библиотеки, указанной в requirements.txt
```commandline
docker-compose up -d --no-deps --build web
```
* Посмотреть запущенные контейнеры
```commandline
docker ps
```
* Войти внутрь контейнера, например в консоль сервиса web
```commandline
docker exec -it blog_api_web_1 bash
```
