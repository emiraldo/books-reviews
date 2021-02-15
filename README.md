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


## Demo

### Url
http://http://13.58.116.139/

### Admin

http://13.58.116.139/admin

### Swagger

http://13.58.116.139/swagger/

### Payload examples

* create reviews
```json
{
    "reviews": [
        {
            "book_id": "QnghAQAAIAAJ",
            "user_id": "864eb77b-b2f7-4268-8402-42eaac4b43f0",
            "review": "my review"
        }
    ]
}
```

### QueryParams format

#### /book-review/
* book_id : str
* user_id : uuid4
* start_date : YYYY-MM-DD
* ned_date : YYYY-MM-DD
* date : YYYY-MM-DD

### Params format

#### /book-review/tracking/{task_id}
* task_id : uuid4

### Test data

* user admin : demo:password1234
* reviewer_id (user_id) : 80b4b634-e831-4b6b-9789-15741683178c (create reviewers http://13.58.116.139/admin/reviews/reviewer/add/)
