For Running the project 
1.Create virtualenv :  sudo apt install python3;sudo apt install python3-venv;python3 -m venv .venv;source .venv/bin/activate
2. install flask packages :  pip install -r requirements.txt
3. Flask-server: port 7000 => click on run 
4. vue-js named front folder: port 8080 => cd front; npm run server; npm install axios (if not found in node modules)
5. install node modules : npm install
6. view images : python3 -m http.server 5000
7. view documents: python3 -m http.server 
8. celeryjobs:  celery -A app:celery_app worker --loglevel INFO; celery -A app:celery_app beat --loglevel INFO
9. for mailhog: ~/go/bin/MailHog  (in wsl terminal) => localhost:8025
