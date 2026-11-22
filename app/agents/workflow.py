
from langgraph.graph import StateGraph, START, END

from app.agents.state import InvoiceState

from app.agents.extraction_agent import extraction_agent
from app.agents.validation_agent import validation_agent
from app.agents.duplicate_agent import duplicate_agent
from app.agents.storage_agent import storage_agent
from app.agents.indexing_agent import indexing_agent


# --------------------------------------------------
# Conditional routing functions
# --------------------------------------------------

def route_after_extraction(state: InvoiceState) -> str:
    if state.get("status") == "failed":
        return "failed"

    return "validation"


def route_after_validation(state: InvoiceState) -> str:
    validation_result = state.get("validation_result", {})

    if not validation_result.get("is_valid", False):
        return "invalid"

    return "duplicate"


def route_after_duplicate(state: InvoiceState) -> str:
    duplicate_type = state.get(
        "duplicate_result", {}
    ).get("duplicate_type")

    if duplicate_type in ("exact", "normalized"):
        return "duplicate"

    if duplicate_type == "potential":
        return "manual_review"

    if state.get("status") == "failed":
        return "failed"

    return "storage"


def route_after_storage(state: InvoiceState) -> str:
    if state.get("status") != "stored":
        return "failed"

    return "indexing"


def route_after_indexing(state: InvoiceState) -> str:
    if state.get("status") != "indexed":
        return "failed"

    return "success"


# --------------------------------------------------
# Build LangGraph workflow
# --------------------------------------------------

def build_workflow():

    graph = StateGraph(InvoiceState)

    # Register agents as nodes
    graph.add_node("extraction", extraction_agent)
    graph.add_node("validation", validation_agent)
    graph.add_node("duplicate_detection", duplicate_agent)
    graph.add_node("storage", storage_agent)
    graph.add_node("indexing", indexing_agent)

    # Start -> Extraction
    graph.add_edge(START, "extraction")

    # Extraction -> Validation or END
    graph.add_conditional_edges(
        "extraction",
        route_after_extraction,
        {
            "validation": "validation",
            "failed": END,
        },
    )

    # Validation -> Duplicate Detection or END
    graph.add_conditional_edges(
        "validation",
        route_after_validation,
        {
            "duplicate": "duplicate_detection",
            "invalid": END,
        },
    )

    # Duplicate Detection -> Storage or END
    graph.add_conditional_edges(
        "duplicate_detection",
        route_after_duplicate,
        {
            "storage": "storage",
            "duplicate": END,
            "manual_review": END,
            "failed": END,
        },
    )

    # Storage -> Indexing or END
    graph.add_conditional_edges(
        "storage",
        route_after_storage,
        {
            "indexing": "indexing",
            "failed": END,
        },
    )

    # Indexing -> END
    graph.add_conditional_edges(
        "indexing",
        route_after_indexing,
        {
            "success": END,
            "failed": END,
        },
    )

    return graph.compile()


# --------------------------------------------------
# Compiled workflow instance
# --------------------------------------------------

invoice_workflow = build_workflow()
