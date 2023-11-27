uri = "bolt://localhost:7687"
username = "neo4j"
password = "12345678"
# Function to insert the data from CSV into Neo4j
def insert_data(tx, data):
    query = """
    CREATE (hero:Superhero {
        _id: $id,
        name: $name,
        powerstats: {
            intelligence: $intelligence,
            strength: $strength,
            speed: $speed,
            durability: $durability,
            power: $power,
            combat: $combat
        },
        biography: {
            full_name: $full_name,
            alter_egos: $alter_egos,
            aliases: $aliases,
            place_of_birth: $place_of_birth,
            first_appearance: $first_appearance,
            publisher: $publisher,
            alignment: $alignment
        },
        appearance: {
            gender: $gender,
            race: $race,
            height: $height,
            weight: $weight,
            eye_color: $eye_color,
            hair_color: $hair_color
        },
        work: {
            occupation: $occupation,
            base: $base
        },
        connections: {
            group_affiliation: $group_affiliation,
            relatives: $relatives
        },
        image: {
            url: $url
        }
    })
    """
    tx.run(query, **data)
# Load data from CSV
csv_file_path = 'superheroes.csv'
with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        data = {
            'id': row['_id'],
            'name': row['name'],
            'intelligence': row['powerstats.intelligence'],
            'strength': row['powerstats.strength'],
            'speed': row['powerstats.speed'],
            'durability': row['powerstats.durability'],
            'power': row['powerstats.power'],
            'combat': row['powerstats.combat'],
            'full_name': row['biography.full-name'],
            'alter_egos': row['biography.alter-egos'],
            'aliases': row['biography.aliases'],
            'place_of_birth': row['biography.place-of-birth'],
            'first_appearance': row['biography.first-appearance'],
            'publisher': row['biography.publisher'],
            'alignment': row['biography.alignment'],
            'gender': row['appearance.gender'],
            'race': row['appearance.race'],
            'height': row['appearance.height'],
            'weight': row['appearance.weight'],
            'eye_color': row['appearance.eye-color'],
            'hair_color': row['appearance.hair-color'],
            'occupation': row['work.occupation'],
            'base': row['work.base'],
            'group_affiliation': row['connections.group-affiliation'],
            'relatives': row['connections.relatives'],
            'url': row['image.url']
        }
        # Establish connection to the Neo4j database and insert data
        driver = GraphDatabase.driver(uri, auth=(username, password))
        with driver.session() as session:
            session.write_transaction(insert_data, data)
