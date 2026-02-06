#!/usr/bin/env python3
"""
Weaviate Schema Migration Script for Project Chimera.

This script manages the schema lifecycle for the Weaviate vector database.
It ensures that the required classes (like AgentMemory) exist and have the correct
property definitions.

Usage:
    python scripts/db/weaviate_migrator.py check
    python scripts/db/weaviate_migrator.py migrate
"""

import sys
import os
import weaviate
from weaviate.util import generate_uuid5
from typing import Dict, Any, List

# Configuration would typically come from environment variables
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "")

# -----------------------------------------------------------------------------
# Schema Definitions
# -----------------------------------------------------------------------------

AGENT_MEMORY_CLASS: Dict[str, Any] = {
    "class": "AgentMemory",
    "description": "Semantic memory for agent experiences and task results.",
    "vectorizer": "text2vec-openai",  # Or whatever is configured in the Docker/Cluster
    "moduleConfig": {"text2vec-openai": {"model": "ada", "modelVersion": "002", "type": "text"}},
    "properties": [
        {
            "name": "content",
            "dataType": ["text"],
            "description": "The raw text of the observation, result, or interaction.",
            "moduleConfig": {"text2vec-openai": {"skip": False, "vectorizePropertyName": False}},
        },
        {
            "name": "tenant_id",
            "dataType": ["text"],
            "description": "Multi-tenancy isolation.",
            "moduleConfig": {"text2vec-openai": {"skip": True}},
        },
        {
            "name": "session_id",
            "dataType": ["text"],
            "description": "Context scoping.",
            "moduleConfig": {"text2vec-openai": {"skip": True}},
        },
        {
            "name": "agent_role",
            "dataType": ["text"],
            "description": "Source of the memory.",
            "moduleConfig": {"text2vec-openai": {"skip": True}},
        },
        {
            "name": "importance_score",
            "dataType": ["number"],
            "description": "Relevance weight.",
            "moduleConfig": {"text2vec-openai": {"skip": True}},
        },
        {
            "name": "created_at",
            "dataType": ["date"],
            "description": "Temporal ordering.",
            "moduleConfig": {"text2vec-openai": {"skip": True}},
        },
    ],
}

TARGET_SCHEMA = [AGENT_MEMORY_CLASS]


def get_client() -> weaviate.Client:
    """Returns a configured Weaviate client."""
    auth_config = None
    if WEAVIATE_API_KEY:
        auth_config = weaviate.auth.AuthApiKey(api_key=WEAVIATE_API_KEY)

    return weaviate.Client(url=WEAVIATE_URL, auth_client_secret=auth_config)


def check_schema(client: weaviate.Client) -> bool:
    """Checks if the current schema matches the target schema."""
    current_schema = client.schema.get()
    classes = {c["class"]: c for c in current_schema.get("classes", [])}

    all_good = True
    for target_class in TARGET_SCHEMA:
        class_name = target_class["class"]
        if class_name not in classes:
            print(f"[MISSING] Class '{class_name}' does not exist.")
            all_good = False
        else:
            # Simple check: do all properties exist?
            # In a real production script, we would check types and config deep equality.
            existing_props = {p["name"] for p in classes[class_name].get("properties", [])}
            target_props = {p["name"] for p in target_class.get("properties", [])}

            missing_props = target_props - existing_props
            if missing_props:
                print(f"[INCOMPLETE] Class '{class_name}' is missing properties: {missing_props}")
                all_good = False
            else:
                print(f"[OK] Class '{class_name}' exists and has all required properties.")

    return all_good


def migrate_schema(client: weaviate.Client):
    """Applies the target schema to Weaviate."""
    current_schema = client.schema.get()
    classes = {c["class"]: c for c in current_schema.get("classes", [])}

    for target_class in TARGET_SCHEMA:
        class_name = target_class["class"]

        if class_name not in classes:
            print(f"Creating class '{class_name}'...")
            client.schema.create_class(target_class)
            print(f"Created class '{class_name}'.")
        else:
            # Handle property additions (Weaviate allows adding properties to existing classes)
            existing_props = {p["name"] for p in classes[class_name].get("properties", [])}
            for prop in target_class.get("properties", []):
                if prop["name"] not in existing_props:
                    print(f"Adding property '{prop['name']}' to class '{class_name}'...")
                    client.schema.property.create(class_name, prop)

            print(f"Class '{class_name}' is up to date.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python weaviate_migrator.py [check|migrate]")
        sys.exit(1)

    command = sys.argv[1]

    try:
        client = get_client()
    except Exception as e:
        print(f"Error connecting to Weaviate: {e}")
        sys.exit(1)

    if command == "check":
        if check_schema(client):
            print("Schema is valid.")
            sys.exit(0)
        else:
            print("Schema validation failed.")
            sys.exit(1)
    elif command == "migrate":
        migrate_schema(client)
        print("Migration complete.")
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
