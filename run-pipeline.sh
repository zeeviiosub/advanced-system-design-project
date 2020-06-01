scripts/install.sh
python -m saver run-saver save_user &
python -m saver run-saver save_pose &
python -m saver run-saver save_feelings &
python -m saver run-saver save_color_image &
python -m saver run-saver save_depth_image &
python -m server run-server localhost &
python -m saver run-saver user &
python -m saver run-saver pose &
python -m saver run-saver feelings &
python -m saver run-saver color_image &
python -m saver run-saver depth_image &
python api.py &
python web/app.py &
