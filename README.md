### TO DO

* improve login
  * implement forgot password and reset
  * implement login with linkedin
* improve video storage
  * when first apply, create a Submission
  * when post for question, add to Submission, don't upload directly to S3
* add personality test and english test to the flow and Submission
* improve design
* other misc
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



### Deploying Application Updates
> ssh louis@1024germany.de
$ cd project
$ source venv/bin/activate
(venv) $ git pull                              
(venv) $ sudo systemctl stop videocollect
(venv) $ flask db upgrade                      
(venv) $ sudo systemctl start videocollect    

