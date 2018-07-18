### TO DO

* improve login
  * right now can't apply because the app thinks the user is not logged in
  * associate application data to Auth0-authenticated users: For example, you could have a Users table that lists each user authenticated by Auth0. Every time a users logs in, you could search the table for that user. If the user does not exist, you would create a new record. If they do exist, you would update all fields, essentially keeping a local copy of all user data. [Session Management](https://auth0.com/docs/architecture-scenarios/web-app-sso/part-3): don't use Flask Login anymore 
* improve video storage
  * check that you can upload 30 seconds videos
  * when first apply, create a Submission
  * when post for question, add to Submission, don't upload directly to S3
* add personality test and english test to the flow and Submission
* improve design
* other misc
  * get additional scopes from the linkedin API (r_fullprofile and r_network) through their partner program
  * [Call the Linkedin API](https://auth0.com/docs/connections/calling-an-external-idp-api) with the received token to get a more complete user profile 
  * deploy using a PaaS like GCP instead of managing a Linux server (relevant for the DB mainly?) (or with Docker + Kubernetes)
  * replace usage of config.global_data by DB table Questions
  * add a few tests
  * translate to spanish, french, egyptian if that makes sense using [this article](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xiii-i18n-and-l10n) 

### Quick Start

1. Clone the repo

2. Initialize and activate a virtualenv:
  ```
  $ python3 -m  venv venv
  $ source venv/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```
  ```
  $ cd app/static
  $ npm install
  ```

5. Run the development server:
  ```
  $ export FLASK_APP=videocollect.py
  $ flask run
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

7. During development
```
flask db migrate -m "users table"
flask db upgrade
```


### Deploying Application Updates
> ssh louis@1024germany.de
$ cd project
$ source venv/bin/activate
(venv) $ git pull                              
(venv) $ sudo systemctl stop videocollect
(venv) $ flask db upgrade                      
(venv) $ sudo systemctl start videocollect    

