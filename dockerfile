FROM python:3.11

WORKDIR /usr/src/app
COPY . .

RUN apt-get update && apt-get install -y cron tzdata

# Set the timezone
ENV TZ=America/Chicago
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD crontab /etc/cron.d/my-crontab
RUN chmod 0644 /etc/cron.d/my-crontab
RUN crontab /etc/cron.d/my-crontab

RUN touch /var/log/cron.log

RUN pip install --no-cache-dir -r requirements.txt

CMD cron && tail -f /var/log/cron.log
