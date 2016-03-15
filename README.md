# MaveServer

A continuation of [mave-app](https://github.com/CenterForTheBuiltEnvironment/mave-app) by Tyler Hoyt

### Requirements

* Redis (`apt-get install redis-server`)
* pip (`apt-get install python-pip`)

Use virtualenv for the python packages
```
pip install virtualenv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

Install client package dependencies with [bower](http://bower.io/). (requires [npm](https://www.npmjs.com/package/npm))
```
bower install
```

## To Run

You need 3 "tabs", as follows. For simplicity, run all of these in the maveserver folder

```
# handles the job queue
redis-server 

# runs the jobs
rq worker # run within the virtual env! 

# runs the web server
python app.py # run within the virtual env!
```

Then navigate to port 5000
