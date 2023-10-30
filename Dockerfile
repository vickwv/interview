FROM python:3.10.11

ARG ENV_ARG=prod
ENV PROJECT_ENV=$ENV_ARG

ADD ./ /interview
WORKDIR /interview
RUN pip install scrapy -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime

EXPOSE 8000

CMD ["./entrypoint.sh"]