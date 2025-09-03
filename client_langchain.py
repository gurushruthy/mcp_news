import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

async def main():

    client = MultiServerMCPClient({
    "mcp_news": {
        "command": "python",
        "args": ["/Users/shruthymoorthy/Desktop/mcp_news/server.py"],
        "transport": "stdio",
        "env": {  
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
            "OPENAI_EMBED_MODEL": os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
        }
    }
})
    '''async with client.session("mcp_news") as session:
   
        print(await session.call_tool("refresh_bbc", {}))

  
        res = await session.call_tool("bbc_top", {"limit": 3})
        print("bbc_top ->", res.content)
        return '''
    async with client.session("mcp_news") as session:
        tools = await load_mcp_tools(session) 
        print("Loaded tools:", [t.name for t in tools])

        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

        agent = create_react_agent(model=llm, tools=tools)

       
        result = await agent.ainvoke({
            "messages": [("user", "Give me the top 3 BBC headlines right now, with links.")]
        })

        
        last_msg = result["messages"][-1]
        print(getattr(last_msg, "content", last_msg))

if __name__ == "__main__":
    asyncio.run(main())
