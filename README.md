# Shopify Winter API Challenge
## Gabriel Alacchi

### Overview

My challenge submission is built using Django 2.1.1 with python 3.5+. You may run it on its own or by building a docker image.
I've provided some fixtures which can be used to populate the SQLLite3 database with some raw data.

#### Users

To perform any write operations to the API you'll have to be logged in. I've created 4 users all with the same password
`ShopifyChallenge`. The usernames are
```
max
rajesh
kiara
susan
```

#### Navigating the API

Once you have the API up in running (see the Usage section below) navigate to `/docs/`. 
There you will find the Swagger documentation for the API, it will list all the routes available 
and allow you to interact with them. You can log in and log out of different user accounts there.

#### Permissions

I've implemented security validation rules. For instance,
shops have owners, and only the owner is permitted to add/update/delete products, update the store's name, etc...
So if you'd like to test modifying a shop you need to sign in as the owner.
The docs will specify the permissions for each route (if applicable).

#### Kubernetes

While I did not get the API running on any cloud environment, I have included some configuration files that package this API as a Pod with two containers.
The worker container uses gunicorn to serve the API as a WSGI application. The second container uses Nginx to serve static files and proxy pass
API requests back to the worker. This is what `Dockerfile.nginx` in the root is for, as well as the `default.conf` file.

### Usage
#### Install the requirements

This api is built using Django 2.1.1 with python 3.5+ in mind

```
pip install -r requirements.txt
```

#### Running the development server

Once the requirements are installed you need to run the migrations, 
install the fixtures into the database
and finally you can run the server.

```
python manage.py migrate
python manage.py loaddata shop_api/fixtures/*.json
python manage.py runserver
```

### Docker Usage

Alternatively you can run the API using docker.

```
docker build -t shopify-challenge .
docker run -d -p80:80 --name shop-api shopify-challenge
```
