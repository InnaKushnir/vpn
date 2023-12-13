#### vpn-service

API for VPN service.

 #### Features
* Users can register, login  in the vpn_service using username and password.
* The API provides the opportunity to use a proxy server, receive information from sites through a proxy server
 and navigate through site pages.
* The API allows to receive statistics on website visits.
* The API allows by referring to api/statics/user/user_id, get the number of visits to each page and the amount
of information received.
* The API provides the Swagger documentation.

#### Installation
##### Python3 must be already installed.
```
git clone https://github.com/InnaKushnir/vpn
cd vpn
python -m venv venv
venv/Scripts/activate
pip install -r requirements.txt
```
* Copy .env.sample -> .env and populate with all required data.

#### Run the following necessary commands
```
python manage.py migrate
```


* Register on the website using the link.

`http://127.0.0.1:8000/user/register/`

* Get the token using the link. 

`http://127.0.0.1:8000/user/login/`



### How to run with Docker:

- Copy .env.sample -> .env and populate with all required data
- `docker-compose up --build`
- `docker exec -it <number of web-container> /bin/bash`
- Create admin user with command:
- python manage.py createsuperuser
