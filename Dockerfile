FROM alpine

RUN apk add python3 py3-pip py3-cffi
RUN pip install --upgrade wheel
RUN pip install --upgrade setuptools
RUN pip install cryptography
RUN pip install bcrypt

EXPOSE 5067


COPY . /app
WORKDIR /app




#FROM alpine


#clear

#
#COPY ./ /app
#WORKDIR /app