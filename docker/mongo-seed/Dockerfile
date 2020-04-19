FROM mongo

COPY users.json /users.json
COPY devs.json /devs.json
CMD mongoimport --host mongodb --db MLAI --collection users --type json --file /users.json
CMD mongoimport --host mongodb --db MLAI --collection devs --type json --file /devs.json
