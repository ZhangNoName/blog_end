FROM python:3.10-slim

WORKDIR /app



# 复制 requirements.txt 文件到工作目录
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
