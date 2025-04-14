image_id=$( cat ./image_id.cfg ) 

docker run  -p 8080:8080 -p 8443:8443 -p 9990:9990 $image_id
