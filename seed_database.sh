#!/bin/bash

rm db.sqlite3
rm -rf ./witchesapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations witchesapi
python3 manage.py migrate witchesapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata avatars
python3 manage.py loaddata witches
python3 manage.py loaddata witchesInventory
python3 manage.py loaddata ingredientTypes
python3 manage.py loaddata ingredients
python3 manage.py loaddata witchesInventoryIngredient
python3 manage.py loaddata equipment
python3 manage.py loaddata spells
python3 manage.py loaddata spellsEquipment
python3 manage.py loaddata spellsIngredients




