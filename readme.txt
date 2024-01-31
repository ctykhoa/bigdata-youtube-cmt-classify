### install docker and docker-compose
## ubuntu
https://www.theserverside.com/blog/Coffee-Talk-Java-News-Stories-and-Opinions/How-to-install-Docker-and-docker-compose-on-Ubuntu
## windows
https://linuxhint.com/install-docker-compose-windows/

### add youtube api key at:
work/comment-youtube/self/youtube.py line 8 => DEVELOPER_KEY = 'xxxxxxxxxx'
### build and run all containers:
docker-compose up -d
### access and work in container:
docker exec -it -u root jupyter_notebook bash
### move to working directory:
cd ~/work/comment-youtube/self

### run app with streamlit:
streamlit run app.py
### access web app at: http://localhost:8503/


(### to run with python:
python app.py)



----
grant user permissions mysql

mysql -p (pw: pass)
grant ALL PRIVILEGES ON final_project.* TO 'cons';
flush privileges;
show grants for "cons"

-- if data auto fetch load the same old data -> set auto commit = true

## run app to crawl and insert data to db
docker exec -it -u root jupyter_notebook python app.py

## run dashboard
docker exec -it -u root jupyter_notebook python cons.py

## list topic
# access to kafka container:
$docker exec -it -u root kafka bash

$/opt/bitnami/kafka/bin/kafka-topics.sh --list --bootstrap-server 172.18.0.4:9092

## subscribe
/opt/bitnami/kafka/bin/kafka-console-consumer.sh --bootstrap-server 172.18.0.4:9092 --topic youtube_comments --from-beginning
