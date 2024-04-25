DELETE FROM witchesapi_spellingredient
WHERE id = 63;

INSERT INTO witchesapi_unit (label)
VALUES ("item(s)");

INSERT INTO witchesapi_spellingredient (measurement, ingredient_id, spell_id)
VALUES ("one", 3, 2);


-- SELECT 
-- i.label
-- from witchesapi_ingredient i
-- where i.healing_property LIKE "protection";