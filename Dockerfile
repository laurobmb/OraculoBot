FROM centos:centos7
MAINTAINER Lauro de Paula 

LABEL www.laurodepaula.com.br="10.0.0-beta"
LABEL vendor="Bot Python"

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV TZ=America/Recife

RUN yum -y update 
RUN yum -y install epel-release 
RUN yum -y install python-pip 
RUN yum -y install python36 
RUN yum -y groupinstall "Development Tools" 
RUN yum clean all

ADD . /bot/
	
RUN python3 -m pip install --upgrade && \
	cd /bot; python3 -m pip install -r requirements.txt

WORKDIR /bot/

RUN touch /var/log/shared/oraculo.log
RUN chmod 777 /var/log/shared/oraculo.log

CMD ["python3", "/bot/app.py"]
