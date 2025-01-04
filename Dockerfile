# Dockerfile
FROM python:3.9-slim

# 必要なシステムパッケージをインストール
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmariadb-dev gcc pkg-config && \
    rm -rf /var/lib/apt/lists/*

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージリストをコピー
COPY requirements.txt requirements.txt

# Pythonパッケージをインストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# Gunicorn起動コマンド
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi:application"]

