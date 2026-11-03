import os
from dotenv import load_dotenv
from src.db_setup import init_database
from src.agent import create_emporio_agent
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()

def main():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        raise SystemExit(
            "OPENAI_API_KEY não configurada. Copie .env.example para .env e "
            "defina sua chave da OpenAI."
        )

    print("Initializing Empório da Música Assistant...")
    init_database()
    agent_executor = create_emporio_agent()
    chat_history = []
    
    print("\n--- Agent Ready! Type 'exit' or 'quit' to stop. ---\n")
    while True:
        user_input = input("Customer: ")
        if user_input.lower() in ["exit", "quit"]:
            break
            
        response = agent_executor.invoke({
            "input": user_input,
            "chat_history": chat_history
        })
        
        output = response["output"]
        print(f"\nTom (Agent): {output}\n")
        
        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=output))

if __name__ == "__main__":
    main()