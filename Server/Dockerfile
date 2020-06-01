FROM python
WORKDIR /home/user/advanced-system-design-project/Server
ADD . /home/user/advanced-system-design-project/Server
RUN pip install virtualenv
RUN pip install click
RUN pip install pika
RUN pip install pillow
RUN pip install google
RUN pip install protobuf
RUN pip install matplotlib
EXPOSE 8000
ENV NAME server
CMD ["python",  "-m", "server", "run-server", "127.0.0.1"]
