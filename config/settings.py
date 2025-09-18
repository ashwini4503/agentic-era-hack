
# --- AI Trip Planner Configuration ---

# Google Cloud Project Settings
GOOGLE_CLOUD_PROJECT = "your-gcp-project-id"
GOOGLE_CLOUD_LOCATION = "global"
GOOGLE_GENAI_USE_VERTEXAI = True

# ADK Session and Artifact Services
USE_VERTEXAI_SESSION = False  # Set True for production
GCS_ARTIFACT_BUCKET = f"gs://{GOOGLE_CLOUD_PROJECT}-travel-recommendation-artifacts"

# MCP Server Settings
MCP_SERVER_HOST = "0.0.0.0"
MCP_SERVER_PORT = 8081
MCP_SERVER_TOOLS = ["load_web_page_tool"]

# Agent Names
ROOT_AGENT_NAME = "RootAgent"
SUB_AGENT_NAMES = ["ItinerarySubAgent", "PeerAgent1", "PeerAgent2"]

# External API Keys (replace with secure secrets management in production)
GOOGLE_MAPS_API_KEY = "your-maps-api-key"
EMT_API_KEY = "your-emt-api-key"
PAYMENT_GATEWAY_KEY = "your-payment-gateway-key"

# Multilingual Support
SUPPORTED_LANGUAGES = ["en", "hi", "ta", "bn", "mr"]
DEFAULT_LANGUAGE = "en"

# Feature Flags
ENABLE_COST_SHARING = True
ENABLE_ITINERARY_SHARING = True
ENABLE_REALTIME_ADJUSTMENTS = True

# Logging and Observability
LOG_LEVEL = "INFO"
ENABLE_EVENT_LOGGING = True

# Testing and Feedback
ENABLE_USER_FEEDBACK = True
ENABLE_USER_TESTING = False

# Other Custom Settings
MAX_ITINERARY_LENGTH = 10
MAX_FEEDBACK_LENGTH = 500
