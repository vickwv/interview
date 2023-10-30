## docker-compose 部署

```shell
docker build . interview_app:0.1
docker compose up -d

#初始化数据库
docker compose exec -it app bash
python manage.py makemigrations
python manage.py migrate
```

## 接口
### 注册
```shell
curl --location --request POST 'localhost:8000/signup/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test2@qq.com",
    "password": "1jsdf.Bessss"
}'
```

### 登录
```shell
curl --location --request POST 'localhost:8000/signin/' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email": "test2@qq.com",
    "password": "1jsdf.Bessss"
}'
```

### 用户信息
```shell
curl --location --request GET 'localhost:8000/me/' \
--header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkZW50aWZpZXIiOjIsImV4cCI6MTcwMTI2NjY3OCwiaWF0IjoxNjk4Njc0Njc4LjM4MzgyLCJ0b2tlbl90eXBlIjoiYWNjZXNzIn0.KiAeghsEGrySF2mBSHJMcLRI_yKyKW7Rh4qwb_vHAGs'
```