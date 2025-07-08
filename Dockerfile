# 使用官方的、包含完整构建工具的Python 3.10镜像作为基础
FROM python:3.10-slim-buster

# 在容器内设置一个工作目录
WORKDIR /app

# 将我们的需求文件复制到容器中
COPY requirements.txt .

# 更新系统包列表，并安装Playwright浏览器所需要的所有系统依赖
# 这一步是在拥有root权限的构建环境中执行的，所以不会再失败
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    --no-install-recommends

# 安装所有Python库
RUN pip install --no-cache-dir -r requirements.txt

# 核心步骤：安装Playwright的浏览器。因为系统依赖已经装好，这里会顺利完成
RUN playwright install --with-deps

# 将我们项目中的所有文件复制到容器的工作目录中
COPY . .

# 暴露Gunicorn将要监听的5000端口
EXPOSE 5000

# 容器启动时要执行的命令
# 使用Gunicorn来运行我们的Flask应用 (app.py里的app变量)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]# 使用官方的、包含完整构建工具的Python 3.10镜像作为基础
FROM python:3.10-slim-buster

# 在容器内设置一个工作目录
WORKDIR /app

# 将我们的需求文件复制到容器中
COPY requirements.txt .

# 更新系统包列表，并安装Playwright浏览器所需要的所有系统依赖
# 这一步是在拥有root权限的构建环境中执行的，所以不会再失败
RUN apt-get update && apt-get install -y \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    --no-install-recommends

# 安装所有Python库
RUN pip install --no-cache-dir -r requirements.txt

# 核心步骤：安装Playwright的浏览器。因为系统依赖已经装好，这里会顺利完成
RUN playwright install --with-deps

# 将我们项目中的所有文件复制到容器的工作目录中
COPY . .

# 暴露Gunicorn将要监听的5000端口
EXPOSE 5000

# 容器启动时要执行的命令
# 使用Gunicorn来运行我们的Flask应用 (app.py里的app变量)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]