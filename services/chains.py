from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv
load_dotenv()

DEFAULT_MODEL = "gemini-2.5-flash-preview-05-20"

generation_promt = ChatPromptTemplate.from_messages(
    [
     (   "system",
     "You are a writing assistant tasked with improving texts. "
     "Generate the best text possible for the user's request. "
     "Provide a single, complete improved version of the text. "
     "Do not include multiple options or alternatives. "
     "Fix grammar, enhance clarity, and make it an excellent text. "
     "Adapt your improvements to match the specified tone. "
     "Return only the improved text without explanations or comments."),
     ("system", "{tone_instruction}"),
     MessagesPlaceholder(variable_name="messages")
    ]
)


llm = ChatGoogleGenerativeAI(
    model=DEFAULT_MODEL

)

generation_chain = generation_promt | llm