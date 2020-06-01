FROM python
WORKDIR /home/user/advanced-system-design-project/Parsers
ADD . /home/user/advanced-system-design-project/Parsers
RUN pip install virtualenv
RUN pip install click
RUN pip install flask
RUN pip install redis
RUN pip install pika
RUN pip install pillow
RUN pip install google
RUN pip install protobuf
EXPOSE 8000
ENV NAME depth_image_parser
CMD ["python", "-m",  "parsers", "run-parser", "depth_image", "localhost"]

