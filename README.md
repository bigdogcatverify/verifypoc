# Verify POC stuff...

### To start all the apps
```shell script
./startall.sh
```
This should start the frontend on 3000
Blockchain on 8000
and core on 8001

### To stop all the apps
```shell script
./stopall.sh
```

### To clean and setup the db again
#### Warning this will wipe your db
```shell script
./cleandb.sh
```

## Docker compose
to run everything with compose:
```shell script
docker-compose build
docker-compose up
```

## Deployment
See [infra](infra/README.md) readme
