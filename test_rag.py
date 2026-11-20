
from app.services.invoice_rag import (
    index_all_invoices,
    search_invoices,
)

from app.services.qdrant_store import close_qdrant


def main():

    try:

        print("\nIndexing invoices...")

        indexed_count = index_all_invoices()

        print("Indexed:", indexed_count)

        query = "Find invoices from ABC Technology"

        print("\nSearch query:")
        print(query)

        results = search_invoices(
            query=query,
            limit=5,
        )

        print("\nSearch results:")

        if not results:
            print("No matching invoices found.")

        for index, result in enumerate(results, start=1):

            print(f"\nResult {index}")
            print("Score:", result["score"])
            print("Document:", result["document"])
            print("Metadata:", result["metadata"])

    finally:
        close_qdrant()


if __name__ == "__main__":
    main()
