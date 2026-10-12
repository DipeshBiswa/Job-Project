"""Check MongoDB connectivity and verify a temporary record's write/read/delete."""

import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

# Put .env beside this file, outside your .venv directory.
load_dotenv(Path(__file__).with_name(".env"))

uri = os.environ.get("MONGODB_URI")
if not uri:
    raise RuntimeError("Add MONGODB_URI to the .env file beside this script.")

with MongoClient(uri, serverSelectionTimeoutMS=5000) as client:
    # Creating a MongoClient alone does not verify connectivity; ping does.
    client.admin.command("ping")
    print("Python successfully connected to MongoDB!")

    database = client["job_autofill"]
    collection = database["connection_checks"]

    # Use fictional data and remember its ID so only this record is removed.
    result = collection.insert_one({
        "message": "Fictional connection test"
    })

    try:
        saved = collection.find_one({"_id": result.inserted_id})

        if saved is None or saved["message"] != "Fictional connection test":
            raise RuntimeError("Read verification failed")

        print("Write and read successful!")
    finally:
        # Attempt cleanup even if the read verification fails.
        deleted = collection.delete_one({"_id": result.inserted_id})

        if deleted.deleted_count != 1:
            raise RuntimeError("Cleanup failed")

        print("Test record deleted!")