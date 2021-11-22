# Blue-Green Deployment on MiniKube and Docker-Compose

## Introduction

This repository contains a proof-of-concept of blue-green deployment af an
application to Minikube and Docker-compose.
`sk` script in the root stands for "Swiss Knife" is inspired by
make(file) and contains all commands necessary to manage code and deployment.


## Requirements (tested versions)
1. Linux (Arch)
2. VirtualBox 6.1.28 r147628
3. Minikube v1.24.0
4. Kubernetes / kubectl v1.22.4
5. Docker 20.10.10
6. Python3 3.9.7
7. Jq 1.6


## Development


### Developing and running locally

1. Initialize environment:

        ./sk init-venv

2. Run locally:

        ./sk run-dev
        # or
        ./sk run-gunicorn

3. Build docker image:
        
        ./sk build

4. Run in docker:
        
        ./sk run-docker

5. Run tests (infrastructure ones, in Docker):

        ./sk test-docker


## Deployment to Minikube


### Setup environment


1. Start minikube. For instance:

        minikube start --kubernetes-version v1.22.4 --vm-driver=virtualbox

        #or 

        ./sk mk-init

3. Switch to minikube's docker:

        minikube docker-env | source


### Build and release

4. Build few docker images' versions:

        VERSION=0.0.1 ./sk build
        # change the code
        VERSION=0.0.2 ./sk build

5. Deploy

        VERSION=0.0.1 ./sk mk-deploy-all
        VERSION=0.0.2 ROLE=green ./sk mk-deploy-deployment
        ./sk mk-get-public-url

6. Start continuous role switching:

        ./sk mk-role-blink

7. Run benchmark testing (in separate console):

        ./sk mk-test-ab


## Deployment to Docker-Compose

Possible and tested, but is out of scope.


## Conclusion

This solution is over-simplified and could work only as PoC. Real application production usage would require an infrastructure management code (Terraform, etc.), package manager for Kubernetes (e.g. Helm), code tests, fully-featured ingress-controller and many other important features.

Nevertheless, it was possible to achieve seamless switching between blue and
green environments both with Minikube and Docker-compose setups (i.e. get zero failed requests in Apache Benchmark report):

        ...
        Server Software:        gunicorn
        Server Hostname:        192.168.59.108
        Server Port:            30998

        Document Path:          /api/
        Document Length:        20 bytes

        Concurrency Level:      1
        Time taken for tests:   18.867 seconds
        Complete requests:      9999
        Failed requests:        0
        Total transferred:      1649835 bytes
        HTML transferred:       199980 bytes
        Requests per second:    529.98 [#/sec] (mean)
        Time per request:       1.887 [ms] (mean)
        Time per request:       1.887 [ms] (mean, across all concurrent requests)
        Transfer rate:          85.40 [Kbytes/sec] received
        ...
