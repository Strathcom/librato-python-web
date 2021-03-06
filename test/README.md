## Testing postgres
* Install the prerequisites.

`sudo apt-get install libpq-dev python-dev`
`pip install postgres`

* Launch a postgres instance using the docker run command below.

`docker run -d --name postgres-test-server -p 5432:5432 -e POSTGRES_DB=test postgres`

* Launch the test, e.g. as shown.

`python -m unittest instrumentor_.test_psycopg2`


## Testing mysql
* Install the prerequisites.

`sudo apt-get install libmysqlclient-dev`
`pip install mysql-python`

* Launch a mysql instance using the docker run command below. Remember to edit bind-address in mysql_test.conf to the host's docker IP address.

`docker run -d --name mysql-test-server -p 3306:3306 -e MYSQL_ROOT_PASSWORD=root -e MYSQL_DATABASE=test -v $PWD/instrumentor_/mysql_test.cnf  mysql:5.6`

* Launch the test, e.g. as shown below.

`python -m unittest instrumentor_.test_mysql`

## Testing web frameworks
* To test Django or Flask, cd to the respective directory and run unittest.
```
cd flask_    # or django_
python -m unittest discover
```
* To test CherryPy use nose.
```
cd cherrypy_
nosetests
```
