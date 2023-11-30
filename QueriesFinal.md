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
 ```bash
  #Inserta las consultas de Cassandra
  ```
## Neo4J

```bash
  #Inserta las consultas de Neo4J
```
