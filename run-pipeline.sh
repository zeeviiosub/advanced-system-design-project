docker run -d -p 5672:5672 rabbitmq
docker run -d -p 6379:6379 redis
scripts/install.sh
python api.py &
sleep 3
python web/app.py &
sleep 3
python -m server run-server localhost &
sleep 3
python -m saver run-saver save_user &
sleep 3
python -m saver run-saver save_pose &
sleep 3
python -m saver run-saver save_feelings &
sleep 3
python -m saver run-saver save_color_image &
sleep 3
python -m saver run-saver save_depth_image &
sleep 3
python -m parsers run-parser user localhost &
sleep 3
python -m parsers run-parser pose localhost &
sleep 3
python -m parsers run-parser feelings localhost &
sleep 3
python -m parsers run-parser color_image localhost &
sleep 3
python -m parsers run-parser depth_image localhost &
