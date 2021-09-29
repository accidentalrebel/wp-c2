#!/bin/bash
cd ../test/wordpress

if [[ $1 = "up" ]]
then
    sudo docker compose up -d
else
    sudo docker compose stop
fi    
