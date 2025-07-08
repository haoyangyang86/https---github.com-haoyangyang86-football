# 核心修改：将基础镜像的版本从 v1.44.0 更新到 v1.53.0
FROM mcr.microsoft.com/playwright/python:v1.53.0-jammy

# 后续所有步骤保持不变
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]