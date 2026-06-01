FROM python:3.8

ADD requirements.txt .

RUN pip3 install --upgrade pip && \
pip3 install --no-cache-dir -r requirements.txt

RUN mkdir /usr/share/elasticsearch /usr/share/elasticsearch/searchqa /usr/share/elasticsearch/searchqa/data

ADD *.py /usr/share/elasticsearch/searchqa/
ADD data/hansche-qa-arbeitsrecht-id.csv /usr/share/elasticsearch/searchqa/data
#ADD *.whl /usr/share/elasticsearch/searchqa/
#RUN pip3 install /usr/share/elasticsearch/searchqa/tensorflow-2.4.1-cp38-cp38-linux_x86_64.whl
#RUN pip3 install /usr/share/elasticsearch/searchqa/tensorflow_text-2.4.3-cp38-cp38-linux_x86_64.whl
#RUN pip3 install elasticsearch==7.13.1
#RUN pip3 install tensorflow-hub==0.12.0

WORKDIR /usr/share/elasticsearch/searchqa/

RUN chown -R 1001:0 /usr/share/elasticsearch/searchqa && \
    chmod -R g=u /usr/share/elasticsearch/searchqa

USER 1001

CMD /bin/bash -c "python3 indexES.py"
