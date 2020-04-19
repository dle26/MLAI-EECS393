FROM mongo

COPY dev.json /dev.json
CMD mongoimport --host mongodb --db MLAI --collection devs --type json --file /dev.json

