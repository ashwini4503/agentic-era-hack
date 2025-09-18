# Standard definition for itinerary_agent
def itinerary_agent(user_id, preferences, session_state, artifact_service=None):
    """
    Generate an itinerary for the user based on preferences and session state.
    Args:
        user_id (str): The user's ID.
        preferences (dict): User travel preferences.
        session_state (dict): Session state for workflow.
        artifact_service: Optional artifact service for storing artifacts.
    Returns:
        dict: Generated itinerary.
    """
    itinerary = {"id": "itinerary123", "summary": "Sample trip for user."}
    session_state["itinerary"] = itinerary
    if artifact_service:
        artifact_service.save_artifact(user_id, "itinerary", itinerary)
    return itinerary
# --- MCPToolset Integration Example ---
from google.adk.tools import google_search, built_in_code_execution, retrieval
try:
    from google.adk.vertex import VertexAiSearchTool
except ImportError:
    VertexAiSearchTool = None

try:
    from langchain.tools import DuckDuckGoSearchRun
    langchain_search_tool = DuckDuckGoSearchRun()
except ImportError:
    langchain_search_tool = None

try:
    from crewai_tools import CrewaiTool
    crewai_search_tool = CrewaiTool(tool_name="search")
except ImportError:
    crewai_search_tool = None

def external_search(query: str) -> dict:
    try:
        if langchain_search_tool:
            result = langchain_search_tool.run(query)
            return {"status": "success", "source": "LangChain", "result": result}
        elif crewai_search_tool:
            result = crewai_search_tool.run(query)
            return {"status": "success", "source": "CrewAI", "result": result}
        else:
            return {"status": "pending", "message": "No search tool available"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def search_app(query: str, data_store: dict) -> dict:
    try:
        results = [v for k, v in data_store.items() if query.lower() in str(v).lower()]
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def weather_tool(location: str) -> str:
    return f"Weather in {location}: Sunny, 25°C"

def recommend_restaurant(city: str, cuisine: str) -> str:
    return f"Best {cuisine} restaurant in {city}: Foodie's Paradise"

prebuilt_tools = [google_search, weather_tool, built_in_code_execution, retrieval]
if VertexAiSearchTool:
    prebuilt_tools.append(VertexAiSearchTool)
if langchain_search_tool:
    prebuilt_tools.append(external_search)
if crewai_search_tool:
    prebuilt_tools.append(external_search)
prebuilt_tools.append(search_app)
custom_tools = [recommend_restaurant]

from google.adk.mcp import MCPToolset, SseServerParams

# Connect to a remote MCP server using SSE
mcp_server_params = SseServerParams(url="https://your-mcp-server.com")
mcp_toolset = MCPToolset(server_params=mcp_server_params)

# Optionally, filter tools by name
# mcp_toolset = MCPToolset(server_params=mcp_server_params, tool_filter=["search", "weather"])

# Add MCPToolset to your agent's tools
all_tools = prebuilt_tools + custom_tools + [mcp_toolset]

example_agent = Agent(
    name="example_agent",
    model="gemini-2.5-flash",
    instruction="You are a travel assistant. Use tools to answer user queries.",
    tools=all_tools,
)
# Helper to call itinerary_agent with default artifact_service for workflow lambdas
def itinerary_agent_workflow(user_id, preferences, session_state):
    return itinerary_agent(user_id, preferences, session_state, artifact_service=artifact_service)
# --- Clean Agent Setup Example ---
from google.adk.agents import Agent

# Example: Define your prebuilt and custom tools
from google.adk.tools import google_search

def weather_tool(location: str) -> str:
    """Get the current weather for a location."""
    return f"Weather in {location}: Sunny, 25°C"

def recommend_restaurant(city: str, cuisine: str) -> str:
    """Recommend a restaurant in a city for a given cuisine."""
    return f"Best {cuisine} restaurant in {city}: Foodie's Paradise"

prebuilt_tools = [google_search, weather_tool]
custom_tools = [recommend_restaurant]

# --- MCP Integration Examples ---
# Pattern 1: Using Existing MCP Servers within ADK (ADK as MCP Client)
try:
    from model_context_protocol.client import MCPClient
    mcp_client = MCPClient(server_url="https://your-mcp-server.com")
    external_mcp_tools = mcp_client.get_tools()  # Fetch tools exposed by the MCP server
    prebuilt_tools += external_mcp_tools
except ImportError:
    pass

# Pattern 2: Exposing ADK Tools via an MCP Server (ADK as MCP Server)
try:
    from model_context_protocol.server import MCPServer
    mcp_server = MCPServer(
        tools=prebuilt_tools + custom_tools,
        host="0.0.0.0",
        port=8080
    )
    # To run the MCP server, uncomment below:
    # if __name__ == "__main__":
    #     mcp_server.run()
except ImportError:
    pass
# --- AgentTool Wrapper for Search Agent (single correct block at end) ---
from google.adk.agents import AgentTool

search_only_agent = Agent(
    name="search_only_agent",
    model="gemini-2.5-flash",
    instruction="You are a search specialist. Use search tools to answer queries.",
    tools=[]
)

# Wrap the search agent as a tool
search_agent_tool = AgentTool(agent=search_only_agent, name="search_agent_tool")

# Now you can use search_agent_tool alongside other tools in your main agent
main_agent_tools = prebuilt_tools + custom_tools + [search_agent_tool]

# Example main agent using both search_agent_tool and other tools
hybrid_agent = Agent(
    name="hybrid_agent",
    model="gemini-2.5-flash",
    instruction="You are a travel assistant. Use all available tools, including search_agent_tool, to answer user queries.",
    tools=main_agent_tools,
)
# --- AgentTool Wrapper for Search Agent (single correct block at end) ---
from google.adk.agents import AgentTool

search_only_agent = Agent(
    name="search_only_agent",
    model="gemini-2.5-flash",
    instruction="You are a search specialist. Use search tools to answer queries.",
    tools=[]
)

# Wrap the search agent as a tool
search_agent_tool = AgentTool(agent=search_only_agent, name="search_agent_tool")

# Now you can use search_agent_tool alongside other tools in your main agent
main_agent_tools = prebuilt_tools + custom_tools + [search_agent_tool]

# Example main agent using both search_agent_tool and other tools
hybrid_agent = Agent(
    name="hybrid_agent",
    model="gemini-2.5-flash",
    instruction="You are a travel assistant. Use all available tools, including search_agent_tool, to answer user queries.",
    tools=main_agent_tools,
)
# --- AgentTool Wrapper for Search Agent (single correct block at end) ---
from google.adk.agents import AgentTool



# Example main agent using both search_agent_tool and other tools
hybrid_agent = Agent(
    name="hybrid_agent",
    model="gemini-2.5-flash",
    instruction="You are a travel assistant. Use all available tools, including search_agent_tool, to answer user queries.",
    tools=main_agent_tools,
)

# --- AgentTool Wrapper for Search Agent (single correct block at end) ---
from google.adk.agents import AgentTool

# Define a dedicated search agent using only search tools
search_only_agent = Agent(
    name="search_only_agent",
    model="gemini-2.5-flash",
    instruction="You are a search specialist. Use search tools to answer queries.",
)



# --- Agent Workflow Implementation ---

import os
import google.auth
from google.adk.agents import Agent, SequentialAgent, ParallelAgent, LoopAgent
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from google.adk.artifacts import GcsArtifactService
from google.adk.runners import Runner
from google.adk.events import Event


# Import service classes
from src.services.itinerary_generator import ItineraryGenerator
from src.services.cost_sharing import CostSharingService

from src.services.multilingual_support import MultilingualSupportService
from src.interfaces.multilingual_support import MultilingualSupportInterface
from src.services.testing_feedback import TestingFeedbackService
from src.services.booking_payment import BookingPaymentService
from src.services.realtime_adjustments import *  # If you have a class, import it specifically

from src.services.user_profile import UserProfileService
from src.interfaces.user_interaction import UserInteractionInterface


# Setup environment
_, project_id = google.auth.default()
os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project_id)
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")

# --- Advanced ADK Usage ---
# Use GCS artifact service for production
artifact_service = GcsArtifactService(bucket_name=f"gs://{project_id}-travel-recommendation-artifacts")
# Use Vertex AI session service for production, fallback to in-memory for dev
session_service = VertexAiSessionService(project_id=project_id) if os.environ.get("USE_VERTEXAI_SESSION") else InMemorySessionService()


# Dummy clients for illustration (replace with actual clients)
class DummyAIClient:
    def translate(self, text, target_language):
        return f"[Translated to {target_language}]: {text}"

class DummyFirebaseClient:
    def get_cost_breakdown(self, itinerary_id):
        return {"total": 1000, "details": {}}
    def generate_shareable_link(self, itinerary_id):
        return f"https://share/{itinerary_id}"
    def save_feedback(self, user_id, feedback):
        pass
    def save_booking_confirmation(self, itinerary_id, booking_confirmation):
        pass
    def save_user_profile(self, user_id, user_data):
        pass

class DummyBigQueryClient:
    def query(self, query):
        return []

class DummyEMTClient:
    def book(self, itinerary_id, payment_info):
        return {"confirmation": "CONF123"}

class DummyPaymentClient:
    def process(self, payment_info):
        return {"status": "paid"}

ai_client = DummyAIClient()
firebase_client = DummyFirebaseClient()
bigquery_client = DummyBigQueryClient()
emt_client = DummyEMTClient()
payment_client = DummyPaymentClient()
maps_api_key = "dummy-key"


# Instantiate services
itinerary_service = ItineraryGenerator(ai_client, maps_api_key, bigquery_client, firebase_client)
cost_service = CostSharingService(firebase_client)
translation_service: MultilingualSupportInterface = MultilingualSupportService(ai_client)
feedback_service = TestingFeedbackService(firebase_client, bigquery_client)
booking_service = BookingPaymentService(emt_client, firebase_client, payment_client)
user_profile_service: UserInteractionInterface = UserProfileService(firebase_client)
# If you have a real-time adjustment class, instantiate it here





# --- Prebuilt Tool Example (Google, LangChain, CrewAI) ---
# Tool imports
from google.adk.tools import google_search, built_in_code_execution, retrieval
# If using Vertex AI Search, import the tool
try:
    from google.adk.vertex import VertexAiSearchTool
except ImportError:
    VertexAiSearchTool = None

# LangChain and CrewAI tool integration
try:
    from langchain.tools import DuckDuckGoSearchRun
    langchain_search_tool = DuckDuckGoSearchRun()
except ImportError:
    langchain_search_tool = None

try:
    from crewai_tools import CrewaiTool
    crewai_search_tool = CrewaiTool(tool_name="search")
except ImportError:
    crewai_search_tool = None

def external_search(query: str) -> dict:
    """
    Search using LangChain or CrewAI tool, fallback to DuckDuckGo.
    """
    try:
        if langchain_search_tool:
            result = langchain_search_tool.run(query)
            return {"status": "success", "source": "LangChain", "result": result}
        elif crewai_search_tool:
            result = crewai_search_tool.run(query)
            return {"status": "success", "source": "CrewAI", "result": result}
        else:
            return {"status": "pending", "message": "No search tool available"}
    except Exception as e:
        return {"status": "error", "error": str(e)}

def search_app(query: str, data_store: dict) -> dict:
    """
    Search your own data store to ground responses.
    """
    try:
        results = [v for k, v in data_store.items() if query.lower() in str(v).lower()]
        return {"status": "success", "results": results}
    except Exception as e:
        return {"status": "error", "error": str(e)}

# --- Importance of Structured Docstrings and Typing ---
# When writing agent tool functions, always use clear docstrings and type hints for better LLM understanding and reliability.

def weather_tool(location: str) -> str:
    """
    Get the current weather for a location using a prebuilt API.

    Args:
        location (str): The location to get weather for.

    Returns:
        str: Weather description for the location.
    """
    # Example: Use a prebuilt API or mock
    return f"Weather in {location}: Sunny, 25°C"

# --- Custom Tool Function Example ---
def recommend_restaurant(city: str, cuisine: str) -> str:
    """
    Recommend a restaurant in a city for a given cuisine.

    Args:
        city (str): The city to search in.
        cuisine (str): The type of cuisine.

    Returns:
        str: Restaurant recommendation.
    """
    # Example: Replace with actual API call or logic
    return f"Best {cuisine} restaurant in {city}: Foodie's Paradise"

# --- Setup and Requirements ---
# To use these tools, add them to your agent's tool list:
prebuilt_tools = [google_search, weather_tool, built_in_code_execution, retrieval]
if VertexAiSearchTool:
    prebuilt_tools.append(VertexAiSearchTool)
if langchain_search_tool:
    prebuilt_tools.append(external_search)
if crewai_search_tool:
    prebuilt_tools.append(external_search)
prebuilt_tools.append(search_app)
custom_tools = [recommend_restaurant]

# Example agent using these tools
example_agent = Agent(
    name="example_agent",
    model="gemini-2.5-flash",
    instruction="You are a travel assistant. Use tools to answer user queries.",
    tools=prebuilt_tools + custom_tools,
)

def cost_agent(itinerary_id: str, session_state: dict) -> dict:
    cost = cost_service.get_cost_breakdown(itinerary_id)
    session_state["cost"] = cost
    return {"status": "success", "cost": cost}

def translation_agent(text: str, target_language: str, session_state: dict) -> dict:
    translated = translation_service.translate(text, target_language)
    session_state["translated"] = translated
    return {"status": "success", "translated": translated}

def feedback_agent(user_id: str, feedback: str, session_state: dict) -> dict:
    feedback_service.collect_feedback(user_id, feedback)
    session_state.setdefault("feedbacks", []).append(feedback)
    return {"status": "success", "message": "Feedback collected"}

def booking_agent(itinerary_id: str, payment_info: str, session_state: dict) -> dict:
    booking_confirmation, payment_status = booking_service.book(itinerary_id, payment_info)
    session_state["booking_confirmation"] = booking_confirmation
    session_state["payment_status"] = payment_status
    return {
        "status": "success",
        "booking_confirmation": booking_confirmation,
        "payment_status": payment_status
    }

# Break down user_profile_agent into update_name and update_age
def update_name(user_id: str, name: str, session_state: dict) -> dict:
    user_profile_service.update_name(user_id, name)
    session_state.setdefault("user_profile", {})["name"] = name
    return {"status": "success", "name": name}

def update_age(user_id: str, age: int, session_state: dict) -> dict:
    user_profile_service.update_age(user_id, age)
    session_state.setdefault("user_profile", {})["age"] = age
    return {"status": "success", "age": age}

def realtime_adjustment_agent(itinerary_id: str, session_state: dict) -> dict:
    # Placeholder: implement actual adjustment logic
    session_state["adjusted_itinerary"] = {"id": itinerary_id, "adjusted": True}
    return {"status": "success", "adjusted_itinerary": session_state["adjusted_itinerary"]}


# --- Advanced Callback Example ---
def custom_callback(event: Event, state: dict):
    # Example: log, modify state, or trigger external actions
    print(f"Callback: Event {event.id}, Type {event.type}, State keys: {list(state.keys())}")
    if event.type == "tool_call" and "cost" in state:
        # Example: trigger alert if cost exceeds threshold
        if state["cost"].get("total", 0) > 5000:
            print("ALERT: High cost detected!")

# Callback chaining example
def callback_chain(event: Event, state: dict, callbacks):
    for cb in callbacks:
        cb(event, state)


# --- Runner Example ---
def run_agent_workflow(user_id, preferences, user_data, payment_info, target_language="en", feedback=None):
    session_id = f"session_{user_id}"
    # Session persistence: check if session exists, else create
    try:
        session = session_service.get_session(app_name="travel-recommendation", user_id=user_id, session_id=session_id)
    except Exception:
        session_service.create_session(app_name="travel-recommendation", user_id=user_id, session_id=session_id)
    runner = Runner(agent=trip_planner_workflow, app_name="travel-recommendation", session_service=session_service)
    state = {
        "user_id": user_id,
        "preferences": preferences,
        "user_data": user_data,
        "payment_info": payment_info,
        "target_language": target_language,
        "feedback": feedback or {},
    }
    # Callback chaining: run multiple callbacks per event
    callbacks = [custom_callback, lambda e, s: print(f"Extra callback: {e.type}")]
    for event in runner.run(user_id=user_id, session_id=session_id, state=state):
        callback_chain(event, state, callbacks)
        print(f"Event: {event.type}, Content: {getattr(event, 'content', None)}")


# --- Workflow Definitions ---

# SequentialAgent: Trip Planning Workflow (extended)
trip_planner_workflow = SequentialAgent(
    name="TripPlannerWorkflow",
    sub_agents=[
        lambda state: update_name(state["user_id"], state.get("name", ""), state),
        lambda state: update_age(state["user_id"], state.get("age", 0), state),
        lambda state: itinerary_agent_workflow(state["user_id"], state["preferences"], state),
        lambda state: cost_agent(state["itinerary"]["id"], state),
        lambda state: translation_agent(state["itinerary"].get("summary", ""), state.get("target_language", "en"), state),
        lambda state: feedback_agent(state["user_id"], state.get("feedback", ""), state),
        lambda state: booking_agent(state["itinerary"]["id"], state.get("payment_info", ""), state),
        lambda state: realtime_adjustment_agent(state["itinerary"]["id"], state),
    ],
)

# ParallelAgent: Example concurrent tasks (extended)
parallel_workflow = ParallelAgent(
    name="ParallelWorkflow",
    sub_agents=[
        lambda state: itinerary_agent_workflow(state["user_id"], state["preferences"], state),
        lambda state: cost_agent(state.get("itinerary_id", "dummy"), state),
        lambda state: translation_agent(state.get("text", "Hello"), state.get("target_language", "en"), state),
        lambda state: booking_agent(state.get("itinerary_id", "dummy"), state.get("payment_info", {}), state),
        lambda state: realtime_adjustment_agent(state.get("itinerary_id", "dummy"), state),
    ],
)

# LoopAgent: Iterative refinement based on feedback (extended)
def refinement_condition(state):
    # Example: stop if feedback is positive
    return state.get("feedback", {}).get("positive", False)

loop_workflow = LoopAgent(
    name="LoopWorkflow",
    sub_agents=[
        lambda state: itinerary_agent_workflow(state["user_id"], state["preferences"], state),
        lambda state: feedback_agent(state["user_id"], state.get("feedback", {}), state),
        lambda state: realtime_adjustment_agent(state["itinerary"]["id"], state),
    ],
    condition=refinement_condition,
)

# --- Observability: Event Logging Example ---
import logging
logger = logging.getLogger("agent_workflow")

def log_event(event_type, details):
    logger.info(f"Event: {event_type} | Details: {details}")

# Example usage (not executed here):
# session_state = {"user_id": "123", "preferences": {...}, "target_language": "fr", "feedback": {}}
# result = trip_planner_workflow.run(session_state)
# log_event("workflow_completed", result)
