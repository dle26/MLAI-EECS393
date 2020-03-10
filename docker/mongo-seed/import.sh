#! /bin/bash

mongoimport -d MLAI -c 'users' --type json --file ./data/users.json 
