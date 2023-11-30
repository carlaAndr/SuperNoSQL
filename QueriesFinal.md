## Mongo

Busco al 'mejor'  superhéroe según su calificación en 'Powerstats'. Los criterios evaluados son:
- Intelligence
- Strength
- Speed
- Durability
- Power
- Combat
 ```bash
db.supers.aggregate([
    {$project: {name: 1,totalScore: {
        $sum:["$powerstats.intelligence","$powerstats.strength","$powerstats.speed","$powerstats.durability","$powerstats.power", "$powerstats.combat"] }}}, 
    {$sort: { totalScore: -1 }},{$limit: 1}])
  ```
¿A qué se dedican los hombre superhéroes de ambas casas de Cómics?

 ```bash
  db.supers.aggregate([
    {$match: { "appearance.gender": "Male"}},
    {$project: {_id: 0, occupation: "$work.occupation"}},
    {$unwind: "$occupation"},
    {$group: {_id: "$occupation",count: { $sum: 1 }}},
    {$sort: { count: -1 }}])
  ```
¿Cuántos son Aventurero, estudiantes, profesores, ingenieros o científicos?

 ```bash
db.supers.aggregate([
  { $match: { "work.occupation": { $exists: true } } },
  { $project: { _id: 0, occupation: "$work.occupation" } },
  { $unwind: "$occupation" },
  {
    $group: {
      _id: {
        $cond: {
          if: {
            $regexMatch: {input: "$occupation", regex: /(Adventurer|Professor|Engineer|Student|Scientist)/i, },
          },
          then: {
            $regexFind: { input: "$occupation", regex: /(Adventurer|Professor|Engineer|Student|Scientist)/i, },
          },
          else: "Other",
        },
      },
      count: { $sum: 1 },
    },
  },
  {
    $group: {
      _id: "$_id.match", // Agrupar por la profesión, ignorando el idx
      count: { $sum: "$count" },
    },
  },
  {
    $sort: { count: -1 },
  },
]);
  ```
Las mujeres de DC cuya inteligencia y poder de combate sea mayor a la media.
 ```bash
db.supers.aggregate([
  {
    $match: {
      "biography.publisher": "DC Comics",
      "appearance.gender": "Female"
    }
  },
  {
    $group: {
      _id: "$name",
      averageIntelligence: { $avg: "$powerstats.intelligence" },
      averageCombat: { $avg: "$powerstats.combat" }
    }
  },
  {
    $project: {
      _id: 1,
      averageIntelligence: 1,
      averageCombat: 1
    }
  }
])
  ```

## Cassandra

¿Quiénes son los villanos mas peligrosos? Es decir, villanos que superan al promedio de inteligencia y fuerza de los que son buenos
 ```bash
  SELECT AVG(intelligence) AS avg_intelligence FROM superheros  WHERE alignment ='Good' ALLOW FILTERING;

  SELECT AVG(strength) AS avg_strength FROM superheros WHERE alignment ='Good' ALLOW FILTERING;

  SELECT name, intelligence, strength, alignment FROM superheros WHERE intelligence > 29 AND strength > 44 AND alignment = 'Bad' ALLOW FILTERING;
  ```
¿Quién ganaría una pelea entre DC y Marvel? Es decir, en promedio de sus stats quien tiene un promedio mas alto.
```bash
  SELECT publisher, (AVG(combat) + AVG(durability) + AVG(intelligence) + AVG(power) + AVG(speed) + AVG(strength)) / 6 AS avg_values FROM superheros WHERE publisher =  'Marvel comics' ALLOW FILTERING;

  SELECT publisher, (AVG(combat) + AVG(durability) + AVG(intelligence) + AVG(power) + AVG(speed) + AVG(strength)) / 6 AS avg_values FROM superheros WHERE publisher = 'Dc comics' ALLOW FILTERING;
  ```
¿Entre mujeres y hombres humanos quién en promedio es mas alto?
```bash
  SELECT gender, AVG(height) AS average_height FROM superheros WHERE race = 'Human' AND gender = 'Female' ALLOW FILTERING;

  SELECT gender, AVG(height) AS average_height FROM superheros WHERE race = 'Human' AND gender = 'Male' ALLOW FILTERING;
  ```

## Neo4J

Los superhéroes que tienen más o iugal a 80 de durabilidad y sea de Marvel Comics
```bash
MATCH (c:Character)-[:HAS_POWERSTATS]->(p:Powerstats)
MATCH (c:Character)-[:HAS_BIOGRAPHY]->(b:Biography)
where p.`powerstats.power`>'80' AND b.`biography.publisher`= 'Marvel Comics'
RETURN c.name AS heroName, p.`powerstats.power` AS heroPower, b.`biography.publisher` AS Publisher
```
Se buscará los superhéroes que cumplan: durabilidad >=50 y tengan los ojos azules
```bash
MATCH (character:Character)-[:HAS_POWERSTATS]->(powerstats:Powerstats)
MATCH (character:Character)-[:HAS_APPEARANCE]->(appearance:Appearance)
where powerstats.`powerstats.durability`>='50' AND appearance.`appearance.eye-color`='Blue'
RETURN character.name AS heroName, powerstats.`powerstats.durability` AS heroDurability, appearance.`appearance.eye-color` as heroEyeColor
```
Dar el número de superhéroes que tienen los ojos azules agrupados por quién lo publicó.
```bash
MATCH (c:Character)-[:HAS_APPEARANCE]->(a:Appearance)
MATCH (c)-[:HAS_BIOGRAPHY]->(b:Biography)
WHERE toLower(a.`appearance.eye-color`) = 'blue'
RETURN b.`biography.publisher` AS comicBookPublisher, count(c) AS numberOfBlueEyedHeroes
