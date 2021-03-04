# Discord Bot - Valheim Server Control

This bot allows for sending slash commands in discord to control a valheim server hosted on AWS EC2 via API Gateway and Lambda functions

## Install app dependencies

```bash
source .venv/bin/activate
pip instal -r requirements.txt
```

## Installing Lambda Dependencies before build

```bash
cd lambda
docker run -v "$PWD":/var/task "lambci/lambda:build-python3.8" /bin/sh -c "pip install -r requirements.txt -t .; exit"
```

## Deploy

```bash
cdk deploy
```
