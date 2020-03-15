# Provision verify infra

## first time steps

You will need to init the python apps with a hello world type nginx server then import them, 
or else you will not be able to pass the health check the first time. This is a hack to workaround not
being able to determine the HOSTNAME of the container instance. This is needed in the ALLOWED_HOSTS
django config. This is possible with IAM permissions of the running instance.. but it was taking too long!

Build this remotely:

```
$ cd ./init
$ gcloud builds submit --tag gcr.io/bigcatdog/nginx-helloworld
```

And deploy the image to the namespaces that will be occupied by  each of the python apps

```
$ # verify-block deploy
$ gcloud beta run deploy verify-block --image gcr.io/bigcatdog/nginx-helloworld --platform=managed --region=europe-west1 --allow-unauthenticated
$ # verify-core deploy
$ gcloud beta run deploy verify-core --image gcr.io/bigcatdog/nginx-helloworld --platform=managed --region=europe-west1 --allow-unauthenticated
```

Make note of the hostname in the output of the above commands.

Now deploy the real apps

```
$ BLOCK_HOSTNAME=<hostname captured from verify-block deploy above>
$ CORE_HOSTNAME=<hostname captured from verify-core deploy above>

$ # verify-block deploy 
$ gcloud beta run deploy verify-block --image gcr.io/bigcatdog/verify-block --platform=managed --region=europe-west1 --allow-unauthenticated \
  --update-env-vars=HOSTNAME=${BLOCK_HOSTNAME}
$ # verify-block-frontend deploy 
$ gcloud beta run deploy verify-block-frontend --image gcr.io/bigcatdog/verify-block-frontend --platform=managed --region=europe-west1 --allow-unauthenticated \
   --update-env-vars=BLOCK_ENDPOINT=https://${BLOCK_HOSTNAME}
$ # verify-core deploy 
$ gcloud beta run deploy verify-core --image gcr.io/bigcatdog/verify-core --platform=managed --region=europe-west1 --allow-unauthenticated \
   --update-env-vars=BLOCK_ENDPOINT=https://${BLOCK_HOSTNAME},HOSTNAME=${CORE_HOSTNAME}
```

From now on the apps should deploy as a result of pushing changes to git. See cloudbuild.yaml
