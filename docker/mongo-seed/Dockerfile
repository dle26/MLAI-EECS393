FROM mongo:4.2

COPY users.json /users.json
CMD mongoimport --host mongodb --db MLAI --collection users --type json --file ../data/users.json
