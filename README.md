# Books Reviews

Api to massively create book reviews (taken as reference from
the google api), search for reviews by user filtering, date of
exact or by range and by book.

## Run project

* Copy and paste .env.example file and rename for .env
* Modify the SECRET_KEY value in your .env
* Run commands
``` bash
docker-compose build
docker-compose up
```

## MakeFile

The principals commands in the Makefile

* migrate -> create the database schema from migrations
* superuser -> create a superuser for access in admin site
* test -> run unit tests

To know the other commands check the Makefile file.

## Api Doc

After run the project, ingress in http://localhost:8000/swagger
