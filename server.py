import os
os.environ["CHROMA_TELEMETRY_DISABLED"] = "1"  

os.environ["ANONYMIZED_TELEMETRY"] = "False"

from fastmcp import FastMCP
from typing import List, Dict
from connectors.bbc import fetch_bbc
from store.chroma_store import upsert,latest,semantic_search

mcp=FastMCP(name="news-mcp")

@mcp.tool()
def refresh_bbc():
    print("[server] refresh_bbc called")
    items=fetch_bbc()
    print(f"[server] fetched {len(items)} items")
    count=upsert(items)
    return {"written":count}

@mcp.tool()
def bbc_top(limit:int):
    print(f"[server] bbc_top called limit={limit}")
    items=latest(limit)
    if not items:
        refresh_bbc()
    return latest(limit)

@mcp.tool()
def bbc_search(topic,k:int=5):
    return semantic_search(topic,k)

if __name__=="__main__":
    '''try:
        items = fetch_bbc()         # <-- this SHOULD trigger your prints
        print(f"[server] warm-up fetched {len(items)}")
        if items:
            print("[server] first:", items[0].title, "-", items[0].url)
    except Exception as e:
        print("[server] warm-up error:", e)'''
    mcp.run()


