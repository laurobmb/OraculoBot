FROM centos:8
LABEL maintainer="Lauro Gomes <laurobmb@gmail.com>"

LABEL www.laurodepaula.com.br="10.0.0-beta"
LABEL vendor="Bot Python"

ARG TOKEN=868879441:AAEEG-7rd7SmeSWZ3aZpJ6qS4Xc
ENV TOKEN="${TOKEN}"

ARG NOMEBOT=Magali
ENV NOMEBOT="${NOMEBOT}"

ADD app.py /bot/
COPY arquivos/* /bot/arquivos/
COPY imagens/* /bot/imagens/
COPY requirements.txt /bot/
WORKDIR /bot/

RUN dnf -y install python3
RUN dnf -y install python3-pip.noarch
RUN dnf install glibc-langpack-pt  -y
RUN dnf clean all

ENV LANG pt_BR.utf8
ENV LANGUAGE pt_BR.utf8
ENV LC_ALL pt_BR.utf8
ENV TZ=America/Recife

RUN python3 --version
RUN ln -s /usr/bin/python3 /usr/bin/python
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt 

#ENTRYPOINT ["python", "/bot/app.py"]
CMD ["python", "/bot/app.py"]
