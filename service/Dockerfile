FROM joyzoursky/python-chromedriver:latest

RUN pip3 install selenium
RUN pip3 install beautifulsoup4
RUN pip3 install cachetools
RUN pip3 install flask
RUN pip3 install flask_restplus 
RUN pip3 install marshmallow

RUN mkdir -p /dupl

ADD *.py /dupl/

CMD [ "/usr/local/bin/python3.7" ,"/dupl/service.py" ]
