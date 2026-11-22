
from app.agents.workflow import invoice_workflow
from app.services.qdrant_store import close_qdrant


def test_workflow_compiles():
    try:
        assert invoice_workflow is not None

        print("\nWorkflow compilation test passed!")
        print("LangGraph workflow is ready.")

    finally:
        close_qdrant()


if __name__ == "__main__":
    test_workflow_compiles()
