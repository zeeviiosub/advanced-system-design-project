#stop and remove all containers
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q) 

#remove all images
docker rmi $(docker images -a -q)  

#kill hung processes
killall python
