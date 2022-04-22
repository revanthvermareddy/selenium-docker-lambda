## About
This is a web crawler built using selenium, firefox and geckodriver and is compatible as a docker-on-lambda. The built lambda docker image is pushed to a private AWS ECR (Elastic Container Registry) repo. Then an AWS Lambda is built using this image, the flow is deployed on my personal AWS lambda account and verified.

### Requirements
To re-create the AWS Lambda docker image, make sure you have the following pre-requisites set up:
- [git](https://git-scm.com/downloads)
- [docker](https://docs.docker.com/get-docker/)
- [aws-cli](https://awscli.amazonaws.com/AWSCLIV2.msi)
- [python-3.6 or higher](https://www.python.org/downloads/)

## Usage

First, clone this repository
```
git clone https://github.com/revanthvermareddy/selenium-docker-lambda
```

Then, checkout the relevant branch like main

```
git checkout main
```

To configure the aws cli use the below command and provide necessary details like Access Key and Secret Access Key etc when prompted
```
aws configure
```

To configure docker cli use the below command and provide password when prompted
```
docker login --username <your username>
```

To build docker image use
```
docker build --platform=linux/amd64 -t selenium_docker:latest .
```

To run docker image locally
```
docker run -p 9000:8080 -d -it selenium_docker:latest
```

In a separate terminal, you can then locally invoke the function using cURL
```
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!","url":"https://example.com/"}'
```
or you can import the below postman request onto postman client to test the same
```
curl --location --request POST 'http://localhost:9000/2015-03-31/functions/function/invocations' \
--header 'Content-Type: application/json' \
--data-raw '{
    "payload": "hello world!",
    "url": "https://example.com/"
}'
```

To create a private repository
```
aws ecr create-repository --repository-name selenium_docker --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
```

To push to a private repository
```
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS ACCOUNT NUM>.dkr.ecr.us-east-1.amazonaws.com/selenium_docker

docker build --platform=linux/amd64 -t selenium_docker:latest .

docker tag selenium_docker:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/selenium_docker:latest

docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/selenium_docker:latest
```

Once after you've pushed the image, use the image while creating a lambda function.
Configure the timeout and memory accordingly.

### Lambda configurations:
Below are the lambda configurations taht worked out in my case and hope the same should work in your case too. But you may require to twak them if there be a need.
```
timeout: 3 sec
memory: 128 MB
architecure: x86_64
```

## Next Steps (TODO)
After the local development need to automate the deployment onto AWS Lambda using aws-sam-cli

## Contributions
You may customize the code based on your requirements for web crawling. And contributers are encouraged to enhance the code and raise PR's. You may reach out to me anytime at vermareddyrevanth@gmail.com in case of queries.

