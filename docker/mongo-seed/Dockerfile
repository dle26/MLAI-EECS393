FROM mongo:4.2

COPY users.json /users.json
CMD mongoimport --host mongodb -d MLAI -c 'users' --type json --file /users.json
