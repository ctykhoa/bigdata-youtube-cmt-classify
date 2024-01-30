FROM jupyter/minimal-notebook:python-3.10.8

USER root

ENV APP_VERSION="3.3.3" \
    BITNAMI_APP_NAME="spark" \
    JAVA_HOME="/bitnami/java" \
    LD_LIBRARY_PATH="/bitnami/python/lib:/bitnami/spark/venv/lib/python3.8/site-packages/numpy.libs:$LD_LIBRARY_PATH" \
    LIBNSS_WRAPPER_PATH="/bitnami/common/lib/libnss_wrapper.so" \
    NSS_WRAPPER_GROUP="/bitnami/spark/tmp/nss_group" \
    NSS_WRAPPER_PASSWD="/bitnami/spark/tmp/nss_passwd" \
    PYTHONPATH="/bitnami/spark/python/:$PYTHONPATH" \
    SPARK_HOME="/bitnami/spark" \
    SPARK_USER="spark"

RUN sudo apt-get update
RUN sudo apt-get -y install netcat cron

#RUN touch /var/log/cron.log
#RUN crontab -l | { cat; echo "* * * * * /opt/conda/bin/python /home/jovyan/work/comment-youtube/self/app.py >> /cron-log/cron_log_$(date +\%Y\%m\%d).log 2>&1"; } | crontab -
#RUN crontab -l | { cat; echo "* * * * * date >> /var/log/cron.log 2>&1"; } | crontab -
#RUN crontab -l | { cat; echo "* * * * * /home/script.sh >> /var/log/cron.log 2>&1"; } | crontab -

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

CMD ["python", "cons.py"]
# tail -f /var/log/cron.log