# Setting up an OB-CAS App Environment

When running an App on the OB-CAS environment, first this OB-CAS App environment needs to be set-up. 
This section helps the user/developer to understand the hardware & software requirements for running such an OB-CAS app.


<a id="platform" />

##  Platform Requirements for Running OB-CAS App

This section of the document provides the platform requirements needed to run OB-CAS App regardless 
if the developer requires source code access or simply downloads the image from the docker artifactory.

Assumption for below requirements is that OB-BAA is used as reference platform for the OB-CAS sandbox.


### Server Requirements
OB-CAS App can be deployed in either a Bare Metal or a VM.

#### Bare Metal based

No specific requirements on Bare Metal Server type.

Minimum resource requirement of server would be: 4 cores, 16 GB RAM and
80 GB HDD

#### VM based

No specific requirement on Hyper-visor. It could be a Virtual Box, VMWare or any others.

##### Production

Minimum resource requirement of VM would be: 4 vCPUs, 16 GB RAM and 80
GB HDD

##### Lab Trial

Minimum resource requirement of VM would be: 1 vCPUs, 4 GB RAM and 40 GB
HDD

### Operating System (OS) Requirements

While there isn\'t a strict requirement on the OS needed for the
project, Ubuntu is the OS in which the core development team uses.
For the Guest OS in a VM: 64bit Ubuntu 18.04 is the recommended
and either server or desktop versions are supported.

### Network Requirements

Build and deployment of OB-CAS Apps pulls several artifacts (including source
code) from public network. So access to Internet is mandatory.

**Info:** This document assumes that the server is directly connected to Internet with no network proxy. If proxies are part of your network then appropriate proxy settings need to be made for artifact access, docker & maven (instructions available in Internet).

**Warning:** Shell commands used in this page are in bash syntax. If you are using other shells, specific adaption in command would be required.

### Docker

OB-CAS App is realized as micro-services under the docker engine and requires docker to be installed.

```
Install docker:
  apt-get install -y curl
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  sudo apt-get update
  apt-cache policy docker-ce
  sudo apt-get install -y docker-ce
  sudo usermod -aG docker ${USER}
Install Docker Compose:
  sudo apt-get install docker-compose
```


<a id="artifactory" />


<a id="source" />

## Building OB-CAS App Using the Source Code
This section of the document describes how to obtain access to the source code repository for OB-CAS App and then use the source code to build the corresponding app image.

**Warning:** When building OB-CAS App from the Source Code, the build of the obcas-sdk image is required prior to building app

### Platform Requirements
#### Git

Git is the versioning and source code control used for OB-CAS. Git
version 2.7.4 or above should be installed in the system.

```
  sudo apt-get install git
```

### Source Code Access

#### Repositories

The OB-CAS code is maintained in Github within the [Broadband Forum\'s
repositories](http://www.github.com/BroadbandForum).

The code base:

-   obcas - OB-CAS main repository which contains SDK code and sample_apps code



##### Clone OB-CAS repository

```
  git clone git@github.com:BroadbandForum/obcas.git
```


### Build OB-CAS

Building OB-CAS to generate the docker image along with its compose file is
done in two steps:

-   Compilation of Code to generate necessary library files

-   Build a docker image out of the library files

#### Compilation:

For compilation the sequence is to first compile the OB-CAS SDK and
then app module.

```
Build OB-CAS SDK
    Change directory to ~/obcas/src/obcas_sdk/
    make distclean
    make dist   
```
