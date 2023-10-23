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
RUN sudo apt-get -y install netcat

RUN #sudo apt-get install cron
#COPY jupyter/cron_app /etc/cron.d/cron_app
#RUN chmod 0777 /etc/cron.d/cron_app
#ADD crontab /etc/cron.d/cron_app
#RUN crontab /etc/cron.d/cron_app


COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

#CMD ["cron", "-f"]