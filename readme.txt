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