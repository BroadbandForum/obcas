#container_id=$( docker container ls -n 1 -q )

container_id=$( docker container ls | grep " "$(cat image_id.cfg)" "  | sed 's/ .*//' )
if [ -z "$container_id" ]
then
	echo "Error: Cannot get container id for image "$(cat image_id.cfg)
	exit 1
fi

docker stop $container_id

