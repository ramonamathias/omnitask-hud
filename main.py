import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import run_agent_loop

app = FastAPI(title="OmniTask-OS Backend Router")

class CommandRequest(BaseModel):
    objective: str

@app.post("/execute")
async def execute_agent_command(payload: CommandRequest):
    try:
        # ABSOLUTE FINAL LAYER LOCK: Cast it, strip it, ensure it's a raw string
        clean_objective = str(payload.objective).strip()
        print(f"\n⚡ Incoming Server Route Triggered: {clean_objective}", flush=True)
        
        result = run_agent_loop(clean_objective)
        return {"status": "success", "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=False)