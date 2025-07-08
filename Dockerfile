# 步骤 1: 使用Playwright官方的Python镜像
# 这个镜像已经包含了所有我们需要的系统依赖和浏览器！
# 我们选用基于Ubuntu Jammy的1.44.0版本
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# 步骤 2: 设置工作目录
WORKDIR /app

# 步骤 3: 复制需求文件并安装我们的Python库 (Flask, Gunicorn)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 步骤 4: 复制我们应用的所有代码到容器中
COPY . .

# 步骤 5: 暴露Gunicorn将要监听的5000端口
EXPOSE 5000

# 步骤 6: 设置容器启动时要执行的命令
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]