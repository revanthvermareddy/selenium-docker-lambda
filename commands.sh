# Test lambda function using the docker build and docker run commands

# configure the aws cli using the below command
aws configure

# for public repository access w.r.t pull/push of docker 
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/c4y0h3b9

# To build docker image:
docker build --platform=linux/amd64 -t selenium_docker:latest .

# To run docker image locally:
docker run -p 9000:8080 -d -it selenium_docker:latest

# In a separate terminal, you can then locally invoke the function using cURL:
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!","url":"https://example.com/"}'


# steps to push to a private repository
# aws ecr create-repository --repository-name selenium_docker --region us-east-1 --image-scanning-configuration scanOnPush=true --image-tag-mutability MUTABLE
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 281790222696.dkr.ecr.us-east-1.amazonaws.com/selenium_docker
docker build --platform=linux/amd64 -t selenium_docker:latest .
docker tag selenium_docker:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/selenium_docker:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/selenium_docker:latest


# push to a public repository
# docker tag selenium_docker:latest public.ecr.aws/c4y0h3b9/selenium_docker:latest
# docker push public.ecr.aws/c4y0h3b9/selenium_docker:latest

# Access keys for aawscli configuration
# Access Key: 
# Secret Access Key: 

##########################
# For AWS Lambda
# use architecure as: x86_64
# set your timeout as per the requirement

aws lambda invoke --function-name selenium-webcrawler --region us-east-1 out --log-type Tail