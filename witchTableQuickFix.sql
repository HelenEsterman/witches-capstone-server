DELETE FROM witchesapi_spellingredient
WHERE id = 63;

INSERT INTO witchesapi_unit (label)
VALUES ("item(s)");


UPDATE witchesapi_witch
SET avatar_id = 1
WHERE id = 6;

INSERT INTO witchesapi_spellingredient (measurement, ingredient_id, spell_id)
VALUES ("one", 3, 2);