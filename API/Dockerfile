FROM python
WORKDIR /home/user/advanced-system-design-project/API
ADD . /home/user/advanced-system-design-project/API
RUN pip install virtualenv
RUN pip install click
RUN pip install flask
RUN pip install redis
RUN pip install pika
RUN pip install pillow
RUN pip install google
RUN pip install protobuf
EXPOSE 9000
ENV NAME api
CMD ["python",  "api.py"]

