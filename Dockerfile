FROM python:3.8.12-alpine

WORKDIR /app
COPY . .

# install requirements
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/workdir
CMD [ "python", "../src/main.py" ]
