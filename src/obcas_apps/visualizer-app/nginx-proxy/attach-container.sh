#container_id=$( docker container ls -n 1 -q )
container_id=$( docker container ls | grep " "$(cat image_id.cfg)" "  | sed 's/ .*//' )
docker exec -it $container_id bash
