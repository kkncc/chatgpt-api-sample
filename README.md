# ChatGPT-API Sample
OpenAI GPT-3.5 Turbo API.

# Quick Start 
    git clone https://github.com/kkncc/chatgpt-api-sample.git
    cd chatgpt-api-sample/

### Copy config file
    
    mv sample-conf.ini prod-conf.ini
    
### Update api key
    
    OPENAI_API_KEY = 'your openai key'
    
## Usage
### Local
       
    apt install -y nginx supervisor
    pip install requirements.txt
    rm /etc/nginx/sites-enabled/default
    cp nginx_flask.conf /etc/nginx/sites-available/
    nginx -s reload
    mkdir -p /var/log/supervisor
    cp supervisord.conf /etc/supervisor/conf.d/supervisord.conf
    supervisord -c  /etc/supervisor/conf.d/supervisord.conf
    
### Docker
#### modify conf.ini file
    host = redis
#### run
    docker-compose up
    
     