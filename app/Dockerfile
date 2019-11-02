FROM alpine:3.10
RUN apk add --no-cache \
        uwsgi-python3 \
        python3
COPY . /app
WORKDIR /app
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["./run.sh"]
