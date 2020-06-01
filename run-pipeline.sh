docker run -d -p 5672:5672 rabbitmq
docker run -d -p 6379:6379 redis
scripts/install.sh
python api.py &
sleep 2
python web/app.py &
sleep 2
python -m server run-server localhost &
sleep 2
python -m saver run-saver save_user &
sleep 2
python -m saver run-saver save_pose &
sleep 2
python -m saver run-saver save_feelings &
sleep 2
python -m saver run-saver save_color_image &
sleep 2
python -m saver run-saver save_depth_image &
sleep 2
python -m parsers run-parser user localhost &
sleep 2
python -m parsers run-parser pose localhost &
sleep 2
python -m parsers run-parser feelings localhost &
sleep 2
python -m parser run-parser color_image localhost &
sleep 2
python -m parser run-parser depth_image localhost &
