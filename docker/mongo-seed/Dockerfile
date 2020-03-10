FROM mongo

COPY users.json /users.json
CMD mongoimport --host mongodb --db MLAI --collection users --type json --file /users.json
