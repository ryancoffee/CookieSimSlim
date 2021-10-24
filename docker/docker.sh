#!/bin/bash
base_img="hdag-redhat-dockerfile"
container_name="hdag-redhat-dev"
working_dir=$(pwd)
stop_container=$(docker container stop $container_name 2>/dev/null)
remove_container=$(docker container rm $container_name 2>/dev/null)
inspect_con=$(docker container inspect $container_name 2>/dev/null)
inspect_run=$(docker container inspect -f '{{.State.Running}}' $container_name 2>/dev/null)
for i in "$@"
do
    case $i in
    -b|--build)
        if [[ $inspect_cmd == "" ]]; then
        echo "Stopping and removing old HDAG container."
        if [[ $stop_container == "" ]]; then
            echo "Successfully stopped "${container_name}"."
        fi
        if [[ $remove_container == "" ]]; then
            echo "Successfully removed "${container_name}"."
        fi
#        echo "Stopping and removing docker image: "${base_img}"."
#        docker stop $base_img
#        docker image rm $base_img
        fi
#        echo "Pulling docker image: "${base_img}"."
#        docker pull $base_img
    esac
done
if [[ $inspect_con==[] ]] || [[ $inspect_run != "true" ]]; then
    docker build --no-cache - < $base_img -t $container_name
    docker run -d \
       --name $container_name \
       --mount type=bind,source=$working_dir,target=/hdag \
       -it $container_name
fi
docker exec -it $container_name /bin/sh
