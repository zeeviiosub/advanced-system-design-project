FROM python
WORKDIR /home/user/advanced-system-design-project/web
ADD . /home/user/advanced-system-design-project/web
RUN pip install virtualenv
RUN pip install click
RUN pip install flask
RUN pip install redis
RUN pip install pika
RUN pip install pillow
RUN pip install google
RUN pip install protobuf
EXPOSE 7000
ENV NAME web
CMD ["python",  "app.py"]
