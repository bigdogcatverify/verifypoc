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

#### To load test data
```shell script
python manage.py loaddata homer
```

### To Run
```
python manage.py runserver
```

## Deploy

### build image

```bash
docker build -t verify-poc .
```

### publish image
```bash
AWS_ACCOUNT_NO=xxxxxxxxxxxx
docker tag verify-poc ${AWS_ACCOUNT_NO}.dkr.ecr.eu-west-2.amazonaws.com/verify-poc
$(aws ecr get-login --no-include-email)
docker push ${AWS_ACCOUNT_NO}.dkr.ecr.eu-west-2.amazonaws.com/verify-poc
```

### deploy image
