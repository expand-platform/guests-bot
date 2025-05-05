from dataclasses import dataclass


@dataclass
class Versions:

    # ? Versions
    def get_latest_versions_info(self, versions_limit: int = 3):
        self.versions_collection = self.database["versions"]
        latest_versions = list(
            self.versions_collection.find({}).sort("id", -1).limit(versions_limit)
        )

        latest_versions.reverse()
        print("🐍 latest_versions from mongo: ", latest_versions)

        return latest_versions


    def send_new_version_update(self, version_number: int, changelog: str):
        now = datetime.now()

        if ENVIRONMENT == "production":
            now = now + timedelta(hours=3)

        #! 
        current_time = now.strftime(f"%d {MONTHS_RU[now.month]}, %H:%M")

        versions_count = self.versions_collection.count_documents({})

        new_update = {
            "id": versions_count + 1,
            # "date": current_time,
            "version": version_number,
            "changelog": changelog,
        }

        self.versions_collection.insert_one(new_update)

        print(f"⌛ New version { version_number } published! ")

