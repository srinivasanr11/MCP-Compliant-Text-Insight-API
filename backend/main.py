from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import MCPInput, MCPOuput, OutputSummary, MCPResponse
from logic_handler import summarize, classify

# Initialize FastAPI application
app = FastAPI()

# Enable CORS to allow requests from the frontend (e.g., React app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],  # Allow all origins (in production, restrict to specific domains)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Simple health check endpoint
@app.get("/health")
def health():
    return {"status": "OK"}  # Used to verify if the API is running


# Main processing endpoint for MCP-compliant summarization and classification
@app.post("/mcp/process", response_model=MCPOuput)
def process_mcp(input_data: MCPInput):
    """
    Process the input text based on the specified task and intent.

    Supported intents:
    - summarization
    - classification
    - summarization + classification

    Returns:
        JSON containing the output summary/classification and metadata response.
    """
    # Extract intent, task, and text from the request payload
    intent = input_data.model_context.intent
    task = input_data.model_context.task
    text = input_data.input.text

    # Initialize output structures
    output = OutputSummary()
    mcp_response = MCPResponse(
        task=task,
        intent=intent,
        output_type="structured",
        generated_by="rule-engine-v1",  # Indicates this is rule-based logic
    )

    # Handle summarization-only intent
    if intent == "summarization":
        output.summary, _ = summarize(text)  # We discard the category here

    # Handle classification-only intent
    elif intent == "classification":
        output.category, output.confidence = classify(text)

    # Handle both summarization and classification
    elif intent == "summarization + classification":
        output.summary, output.category = summarize(text)
        _, output.confidence = classify(
            text
        )  # Discarding category from classify since it's already set

    # Handle unsupported intents
    else:
        output.message = f"Intent '{intent}' is not supported in this version."
        mcp_response.output_type = "error"

    # Return combined result as per MCP output schema
    return {"output": output, "mcp_response": mcp_response}
