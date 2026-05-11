import chromadb
from uuid import uuid4


client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="startup_memory"
)


def store_startup_memory(idea: str, proposal: str):

    memory_text = f"""
    Startup Idea:
    {idea}

    Final Proposal:
    {proposal}
    """

    collection.add(
        documents=[memory_text],
        ids=[str(uuid4())]
    )


def retrieve_memories(query: str, n_results: int = 3):

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results["documents"][0]

    return "\n\n".join(documents)