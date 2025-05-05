from dataclasses import dataclass


#! class based on DB Driver class
@dataclass
class Replica(DatabaseDriver):
    replica_db: Database = None
    replica_name: str

    def __post_init__(self):
        self.replica_db = self._client[
            REPLICA_NAME
        ]

    def get_replica_documents(self, collection_name="users"):
        return list(self.replica_db[collection_name].find({}))

   

    def replicate_collection(self, collection_name: str = "users"):
        """replicates users or versions collection"""
        existing_documents = self.get_all_users()

        if collection_name == "versions":
            existing_documents = self.get_all_versions()

        replica_collection = self.replica_db[collection_name]

        # ? clear replica
        replica_collection.delete_many({})
        replica_collection.insert_many(existing_documents)

        print(f"Коллекция {collection_name} успешно реплицирована 🐱‍🐉")


    def load_replica(self, collection_name: str = "users"):
        collection_to_erase = self.database[collection_name]
        collection_to_erase.delete_many({})

        new_documents = self.get_all_documents(
            database_name="replica", collection_name=collection_name
        )

        collection_to_erase.insert_many(new_documents)

        print(
            f"Коллекция {collection_name} успешно восстановлена из реплики в основную базу данных! 🐱‍🐉"
        )
