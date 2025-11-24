"""
Utility helpers for optional MongoDB access.
"""
import os
from functools import lru_cache
from typing import Optional

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError


def _mongo_config() -> Optional[dict]:
    """Return Mongo configuration if fully specified."""
    uri = os.environ.get('MONGODB_URI')
    db_name = os.environ.get('MONGO_DB')
    collection = os.environ.get('PATIENTS_COLLECTION')

    if not (uri and db_name and collection):
        return None

    return {
        'uri': uri,
        'db_name': db_name,
        'collection': collection
    }


@lru_cache(maxsize=1)
def get_mongo_client() -> Optional[MongoClient]:
    """Return a cached Mongo client if configuration exists."""
    config = _mongo_config()
    if not config:
        return None

    try:
        client = MongoClient(config['uri'], serverSelectionTimeoutMS=5000)
        # Trigger a lightweight server selection to validate connectivity.
        client.server_info()
        return client
    except PyMongoError as exc:
        print(f"[MongoDB] Connection error: {exc}")
        return None


def get_patient_collection() -> Optional[Collection]:
    """Get the patients collection if MongoDB is configured and reachable."""
    config = _mongo_config()
    client = get_mongo_client()

    if not (config and client):
        return None

    return client[config['db_name']][config['collection']]

