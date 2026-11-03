from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from src.db_setup import execute_sql_query
from src.rag_engine import query_policies

@tool
def search_store_database(sql_query: str) -> str:
    """
    Executes a SQL query against the store's database containing products, orders, customers, and promotions.
    Use this tool to check prices, stock, product details, order statuses, or customer order histories.
    Available tables: produtos, pedidos, clientes, promocoes.
    """
    return execute_sql_query(sql_query)

@tool
def search_store_policies(query: str) -> str:
    """
    Searches the official store policy document.
    Use this tool to answer questions about return policies, working hours, payment methods, shipping, or warranties.
    """
    return query_policies(query)

SYSTEM_PROMPT = """
You are 'Tom', the friendly, professional, and helpful virtual customer service assistant for 'Empório da Música', a musical instrument store located in Campo Grande/MS.

Your goals:
1. Assist customers with product availability, prices, order statuses, store policies, and working hours.
2. Maintain a warm, music-enthusiastic, and helpful tone.
3. Use the `search_store_database` tool whenever you need structured data (products, prices, orders, stock).
4. Use the `search_store_policies` tool whenever you need policy or procedural information (returns, opening hours, payment methods).
5. Politely decline to answer questions that are outside the scope of Empório da Música (e.g., general world trivia, political opinions, coding help).

Important Rules:
- Never fabricate store data, order details, or prices. Always verify via the provided tools.
- Respond in the language used by the customer (default to Portuguese if requested, but maintain documentation in English).
"""

def create_emporio_agent():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    tools = [search_store_database, search_store_policies]
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=True)