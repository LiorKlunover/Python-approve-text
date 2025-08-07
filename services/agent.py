from typing import Sequence, TypedDict
from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from services.chains import generation_chain
from dotenv import load_dotenv
load_dotenv()

# Define our state
class AgentState(TypedDict):
    """State for the agent."""
    messages: Sequence[BaseMessage]
    tone: str = "Professional"

# Define the improver tool
@tool
def improver(text: str, tone: str = "Professional") -> str:
    """Improve the given text using the generation prompt with specified tone.
    
    Args:
        text: The text to improve
        tone: The tone to use for improvement (default: "Professional")
        
    Returns:
        Improved version of the text
    """
    # Use the generation_chain from chains.py to improve the text with the specified tone
    response = generation_chain.invoke({
        "messages": [HumanMessage(content=text)],
        "tone_instruction": f"Use a {tone} tone for the improvement."
    })
    return response.content

# Create a tool node for the improver tool
tools = [improver]
tool_node = ToolNode(tools)

# Define the agent function
def agent(state: AgentState) -> AgentState:
    """Process the user input and decide what to do."""
    messages = state["messages"]
    last_message = messages[-1]
    tone = state.get("tone", "Professional")
    
    # If this is a user message, use the improver tool
    if isinstance(last_message, HumanMessage) and last_message.content.strip():
        # Use the tool's invoke method instead of calling it directly
        improved_text = improver.invoke(last_message.content, tone=tone)
        return {"messages": [ToolMessage(content=improved_text, name="improver", tool_call_id="call_improver")]}
    
    return {"messages": []}

# Define the condition to determine the next node
def router(state: AgentState):
    """Route to the next node based on the state."""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If the last message is from the user, go to the tool node
    if isinstance(last_message, HumanMessage):
        return "tool_node"
    
    # Otherwise, we're done
    return END

# Create the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent)
workflow.add_node("tool_node", tool_node)

# Define the edges
workflow.add_conditional_edges(
    "agent",
    router,
    {
        "tool_node": "tool_node",
        END: END
    }
)
workflow.add_edge("tool_node", "agent")
workflow.set_entry_point("agent")

# Compile the graph
graph = workflow.compile()

# Function to run the agent
def run_agent(user_input: str, tone: str = "Professional") -> str:
    """Run the agent with user input and specified tone.
    
    Args:
        user_input: The user's input text
        tone: The desired tone for the improved text (default: "Professional")
        
    Returns:
        The improved text
    """
    # Check for empty input
    if not user_input or not user_input.strip():
        return "Please provide some text to improve."
        
    try:
        # Create the initial state with the user's message and tone
        state = {
            "messages": [HumanMessage(content=user_input)],
            "tone": tone
        }
        
        # Run the graph
        result = graph.invoke(state)
        
        # Return the improved text
        if result and "messages" in result and result["messages"]:
            return result["messages"][-1].content
        else:
            return "I couldn't improve the text. Please try again with different content."
    except Exception as e:
        print(f"Error in run_agent: {e}")
        # Fallback to direct use of generation_chain if graph fails
        from services.chains import generation_chain
        response = generation_chain.invoke({
            "messages": [HumanMessage(content=user_input)],
            "tone_instruction": f"Use a {tone} tone for the improvement."
        })
        return response.content
