## docker-compose 部署

```shell
docker build . interview_app:0.1
docker compose up -d

#初始化数据库
python manage.py makemigrations
python manage.py migrate
```