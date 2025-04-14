image_id=$( cat ./image_id.cfg ) 
docker_registry="local.docker.registry:5000"

if [ $# -ne 1 ]
then
	echo "Usage: $0 <version>"
	exit 1
fi
version=$1

docker tag $image_id:latest $docker_registry/$image_id:$version

docker push $docker_registry/$image_id:$version
