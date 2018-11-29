FROM joyzoursky/python-chromedriver:latest

RUN pip install --upgrade pip
RUN pip install selenium
RUN pip install beautifulsoup4
RUN pip install cachetools
RUN pip install flask

RUN mkdir -p /dupl

ADD *.py /dupl/

CMD [ "/usr/local/bin/python3.7" ,"/dupl/service.py" ]
