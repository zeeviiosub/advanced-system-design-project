docker run -d -p 5672:5672 rabbitmq
docker run -d -p 6379:6379 redis
sleep 10
python -m api run-server &
sleep 1
python -m gui run-server &
sleep 1
python -m server run-server 127.0.0.1 &
sleep 1
python -m saver run-saver redis://127.0.0.1:6379 rabbitmq://127.0.0.1:5672 &
sleep 1
python -m parsers run-parser user 127.0.0.1 &
sleep 1
python -m parsers run-parser pose 127.0.0.1 &
sleep 1
python -m parsers run-parser feelings 127.0.0.1 &
sleep 1
python -m parsers run-parser color_image 127.0.0.1 &
sleep 1
python -m parsers run-parser depth_image 127.0.0.1 &
