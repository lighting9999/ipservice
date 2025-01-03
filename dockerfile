# 使用官方 Python 运行时作为父镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到容器中的 /app 目录
COPY . /app

# 安装任何所需的包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 443

# 启动命令
CMD ["python", "app.py"]
