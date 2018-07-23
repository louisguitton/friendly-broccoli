### TO DO

* improve video storage
  * make admin dashboard beautiful [see here](https://www.reddit.com/r/flask/comments/7tr82o/example_integrating_flask_admin_into_flask_webapp/)
  * control video uploads from questions table
  * add video table
  * when first apply, create a Submission
  * when post for question, add to Submission, don't upload directly to S3
  * use celery for background jobs, architecture is decribed for Ruby here https://twin.github.io/file-uploads-asynchronous-world/
* add personality test and english test to the flow and Submission
* other misc
  * do a proper json API (maybe using Marshmallow) so that later the frontend can be done in React
  * [Call the Linkedin API](https://auth0.com/docs/connections/calling-an-external-idp-api) with the received token to get a more complete user profile 
  * deploy using a PaaS like GCP instead of managing a Linux server (relevant for the DB mainly?) (or with Docker + Kubernetes)
  * replace usage of config.global_data by DB table Questions
  * get additional scopes from the linkedin API (r_fullprofile and r_network) through their partner program
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

