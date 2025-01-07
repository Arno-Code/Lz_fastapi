# 使用官方 Python 3.12 镜像
FROM python:3.12.8-bullseye

# 设置工作目录
WORKDIR /code

# 复制 requirements.txt 并安装依赖
COPY ./requirements.txt /code/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app

# 暴露端口 80
EXPOSE 80

#
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]