### TO DO
https://github.com/louisguitton/friendly-broccoli/projects/1

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

```bash
> ssh louis@personalityinterview.com
$ cd project
$ source venv/bin/activate
(venv) $ git pull                              
(venv) $ pip install -r requirements.txt
(venv) $ cd app/static
(venv) $ npm install
(venv) $ cd ../..
(venv) $ sudo systemctl stop videocollect
(venv) $ flask db upgrade                      
(venv) $ sudo systemctl start videocollect    
```

To start celery
```bash
→ redis-server
```
```bash
→ celery worker -A videocollect.celery --loglevel=info
```
```bash
→ celery beat -A videocollect.celery --loglevel=info
```

### Debugging
```
sudo cat /var/log/videocollect_access.log
sudo cat /var/log/videocollect_error.log
sudo journalctl -u videocollect
```