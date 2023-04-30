FROM python:3
ENV PYTHONUNBUFFERED 1

# /appを作業ディレクトリに設定
WORKDIR /app
# 作業ディレクトリを作成
RUN mkdir WORKDIR
# ソースをコンテナにコピー
COPY . /app
# pipインストール
RUN pip install -r requirements.txt
