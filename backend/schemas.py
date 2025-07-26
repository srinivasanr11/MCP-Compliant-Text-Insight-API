from pydantic import BaseModel
from typing import Optional, Literal

# ------------------------
# Model Definitions for MCP API
# ------------------------


class ModelContext(BaseModel):
    """
    Contains metadata about the model task and user intent.

    Attributes:
        task (str): The type of task being requested (e.g., "text_analysis").
        intent (str): The specific goal such as "summarization" or "classification".
        user_role (str): Role of the end-user submitting the request (e.g., "customer").
        language (str): Language of the input text (e.g., "en").
    """

    task: str
    intent: str
    user_role: str
    language: str


class InputText(BaseModel):
    """
    Wraps the actual input data for the model.

    Attributes:
        text (str): The user-provided text that needs to be analyzed.
    """

    text: str


class MCPInput(BaseModel):
    """
    The complete input schema as per the MCP specification.

    Attributes:
        model_context (ModelContext): Metadata including task and intent.
        input (InputText): The actual user input text for processing.
    """

    model_context: ModelContext
    input: InputText


class OutputSummary(BaseModel):
    """
    Represents the model's structured output.

    Attributes:
        summary (Optional[str]): Text summarization result (if applicable).
        category (Optional[str]): Classification label/category (if applicable).
        confidence (Optional[float]): Confidence score for the classification.
        message (Optional[str]): Optional message for error or status info.
    """

    summary: Optional[str] = None
    category: Optional[str] = None
    confidence: Optional[float] = None
    message: Optional[str] = None


class MCPResponse(BaseModel):
    """
    Metadata about the model's response and its origin.

    Attributes:
        task (str): The task that was executed.
        intent (str): The intent that guided the execution.
        output_type (Literal): Indicates whether the output was structured or an error.
        generated_by (str): Identifier for the version or engine that produced the output.
    """

    task: str
    intent: str
    output_type: Literal["structured", "error"]
    generated_by: str


class MCPOuput(BaseModel):
    """
    The full response object combining output data and response metadata.

    Attributes:
        output (OutputSummary): The core analysis results.
        mcp_response (MCPResponse): Metadata describing how and what was generated.
    """

    output: OutputSummary
    mcp_response: MCPResponse
