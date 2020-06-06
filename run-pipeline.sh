source cleanup.sh
docker run -d --net host rabbitmq
docker run -d --net host redis
docker build -t api -f Dockerfile.api .
docker build -t gui -f Dockerfile.gui .
docker build -t server -f Dockerfile.server .
docker build -t saver -f Dockerfile.saver .
docker build -t user-parser -f Dockerfile.parsers.user .
docker build -t pose-parser -f Dockerfile.parsers.pose .
docker build -t feelings-parser -f Dockerfile.parsers.feelings .
docker build -t color-image-parser -f Dockerfile.parsers.color_image .
docker build -t depth-image-parser -f Dockerfile.parsers.depth_image .
docker run -d --net host api
docker run -d -v `pwd`/web/static:/web/static --net host gui
docker run -d -v `pwd`/web/static:/web/static --net host server
docker run -d --net host saver
docker run -d --net host user-parser
docker run -d --net host pose-parser
docker run -d --net host feelings-parser
docker run -d --net host color-image-parser
docker run -d --net host depth-image-parser
