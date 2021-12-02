KiskaURL Server-side
============
<!-- [![GitHub Stars](https://img.shields.io/github/stars/IgorAntun/node-chat.svg)](https://github.com/IgorAntun/node-chat/stargazers) [![GitHub Issues](https://img.shields.io/github/issues/IgorAntun/node-chat.svg)](https://github.com/IgorAntun/node-chat/issues) [![Current Version](https://img.shields.io/badge/version-1.0.7-green.svg)](https://github.com/IgorAntun/node-chat) [![Live Demo](https://img.shields.io/badge/demo-online-green.svg)](https://igorantun.com/chat) [![Gitter](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/IgorAntun/node-chat?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge) -->

Server-side application for URL shortening web service that shortens long messy URLs into more managable and shorter URL. <br/>
Built in <a href="https://en.wikipedia.org/wiki/Representational_state_transfer" target="_blank">REST</a> architecture using <a href="https://www.django-rest-framework.org/" target="_blank">Django REST Framework</a>.


![Chat Preview](https://i.imgur.com/ibdQ7ra.png)

---
## Request Flow for Shortening the URL
![Chat Preview](https://i.imgur.com/5mUbTPr.jpeg)


#### User must be authenticated in order to make `POST, UPDATE, PATCH and DELETE` requests
1. User inserts URL to shorten and makes `POST` request to the server
2. Server checks the inserted URL if it was shortened before (Checks the Database if it already exists)
3. If inserted URL is shortened before (already exists in DB), the short url will returned to the user (client) from Database
4. If it is not in Database, the inserted URL will be passed for Hashing (Encoding)
5. Hashing uses MD5 Hashing Algorithm to hash the inserted URL and returns Hashed value
  <br/> Hashed value will be used for making a short url to navige the user to the original url:
```
Same URLs should yield same Short URL for the SAME user
But same URLs should yield DIFFERENT Short URLs for DIFFERENT users
```
`Hashing Algorithm:` <br/>
<img src="https://i.imgur.com/qDRJ0Mb.png" width="600" heigh="600"/> <br/>
```
- Appends Hash value: 'hu7d34' to 'domain name' and saves it in Database
- Short URL:    'kiska.com/hu7d34'
- Map the Short URL to Original URL
Whenever user make a request to Short URL, Short URL redirects the user to Original URL
```

---
## Demo
<p><a href="https://kiska.herokuapp.com/" target="_blank">Here</a> you can explore the live Swagger documented API</p>

---

## Features
- User Registration
- Password Change
- Password Reset through Email verification

---
## Technologies
- Python 3.9
- Django 3.2.9
- Django REST Framework 3.12.4

---

## Setup
To run the app in your own local machine, first of all, clone this repo to your local machine and install all of the dependecies by going to its root directory and on the terminal run the command below:
```bash
$ pip install -r requirements.txt
```
---

## Usage
Once the dependencies are installed, you can start the application by running the command below : 
```bash 
$ python manage.py runserver
``` 
You will then be able to access it at `127.0.0.1:8000` or `localhost:8000`

To give yourself administrator permissions, you will have to create a superuser account (Admin User) using the command below:
```bash
$ python manage.py createusuperuser
```

---

## License
>You can check out the full license [here](https://github.com/javokhirbek1999/kiska-url-server-side/blob/main/LICENSE)

This project is licensed under the terms of the **MIT** license.
