from neo4j import GraphDatabase

def main():
    # Neo4j connection parameters
    uri = "bolt://neo4j:7687"
    username = "neo4j"
    password = "12345678"
    
    #column_list = df['column_name'].tolist()
    import pandas as pd
    column_list = pd.read_csv('https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/character.txt')['_id'].tolist()

    # Example usage:
    # Function to load CSV data into Neo4j
    def load_csv(url, node_label):
        query = (
            f"LOAD CSV WITH HEADERS FROM '{url}' AS row "
            f"CREATE (n:{node_label}) SET n = row"
        )
        return query
    def setRel(character_id):
        query = (
            f"MATCH (character:Character {{_id: '{character_id}'}})"
            f"MATCH (appearance:Appearance {{_id: '{character_id}'}})"
            f"MATCH (image:Image {{_id: '{character_id}'}})"
            f"MATCH (connections:Connections {{_id: '{character_id}'}})"
            f"MATCH (biography:Biography {{_id: '{character_id}'}})"
            f"MATCH (powerstats:Powerstats {{_id: '{character_id}'}})"
            f"MATCH (work:Work {{_id: '{character_id}'}})"
            f"MERGE (character)-[:HAS_POWERSTATS]->(powerstats)"
            f"MERGE (character)-[:HAS_CONNECTIONS]->(connections)"
            f"MERGE (character) -[:WORKS_IN]->(work)"
            f"MERGE (character) -[:LOOKS_LIKE]->(image)"
            f"MERGE (character) -[:HAS_APPEARANCE]->(appearance)"
            f"MERGE (character) -[:HAS_BIOGRAPHY]->(biography)"
        )
        return query
    # Load CSV files into Neo4j
    csv_files = ['https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/appearance.txt',
                'https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/biography.txt',
                'https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/character.txt',
                'https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/connections.txt',
                'https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/image.txt',
                'https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/powerstats.txt',
                'https://raw.githubusercontent.com/carlaAndr/SuperNoSQL/main/csv/work.txt']
    node_labels = ['Appearance', 'Biography', 'Character', 'Connections', 'Image', 'Powerstats', 'Work']

    with GraphDatabase.driver(uri, auth=(username, password)) as driver:
        print("Loading data into Neo4j...")
        for csv_file, node_label in zip(csv_files, node_labels):
            with driver.session() as session:
                query = load_csv(csv_file, node_label)
                session.run(query)
                for i in column_list:
                    session.run(setRel(i))
        print("Data loaded successfully")
                
if __name__ == "__main__":
    main()
