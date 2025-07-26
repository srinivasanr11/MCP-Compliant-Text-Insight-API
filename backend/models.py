# --- models.py ---
# Defines Pydantic models for validating and serializing incoming and outgoing data.
# This enforces schema compliance with the MCP (Model Context Protocol) specification.

from pydantic import BaseModel, Field
from typing import Dict, Any


class InputData(BaseModel):
    """
    Represents the structure of the 'input' section in the request.

    Attributes:
        text (str): The user-provided input text for processing.
    """

    text: str = Field(
        ...,  # Required field
        example="The latest update caused several issues.",  # Sample input for API docs
    )


class MCPInput(BaseModel):
    """
    Represents the full MCP-compliant input payload structure.

    Attributes:
        model_context (Dict): Contextual metadata for the model, such as the source app.
        task (str): The type of task to be performed (e.g., "text_analysis").
        intent (str): Specifies the operation(s) requested (e.g., "summarization").
        user_role (str): Role of the user submitting the text (e.g., "customer", "admin").
        language (str): Language of the input text.
        input (InputData): The actual content to be processed.
    """

    model_context: Dict = Field(
        default_factory=dict,  # Optional metadata with default empty dict
        example={"source": "webapp-v2"},  # Sample context for API usage
    )
    task: str = Field(
        ...,  # Required field
        example="text_analysis",  # Helps document the expected task type
    )
    intent: str = Field(
        ..., example="summarization + classification"  # Required field  # Sample intent
    )
    user_role: str = Field(
        ...,  # Required field
        example="customer",  # Describes the role of the feedback author
    )
    language: str = Field(
        ..., example="en"  # Required field  # Language code (ISO format)
    )
    input: InputData  # Nested object containing the actual user input
