### TO DO

* better app structure: refactor with blueprints
* deploy
* implement forgot password and reset
* when first apply, create a Submission
* when post for question, add to Submission, don't upload directly to S3
* replace usage of config.global_data by DB table Questions


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

5. Run the development server:
  ```
  $ export FLASK_APP=1024germany.py
  $ flask run
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)



  ```

