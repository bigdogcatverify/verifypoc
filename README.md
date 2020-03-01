# verifypoc
Simple Django app at this stage

Before you can run the server you will 
need to run the migrations

## Get started

### Install Dependencies
```shell script
pip install -r requirements.txt
```

### Setup DB

#### Create Migrations
```
python manage.py makemigrations verify
```

#### To run Migrations
```shell script
python manage.py migrate
```

### To Run
```
python manage.py runserver
```
