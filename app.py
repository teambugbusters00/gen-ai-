"""Prompt library + OpenAI-compatible generation endpoint."""
import os,json
from pathlib import Path
import httpx
from fastapi import FastAPI,HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel,Field
app=FastAPI(title="GenAI Playground");DB=Path("prompts.json")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
def read():return json.loads(DB.read_text()) if DB.exists() else []
class Prompt(BaseModel):name:str=Field(min_length=1);template:str=Field(min_length=1)
class Run(BaseModel):name:str;variables:dict[str,str]={}
@app.get("/prompts")
def prompts():return read()
@app.post("/prompts")
def save(p:Prompt):
 rows=read();rows=[x for x in rows if x["name"]!=p.name];rows.append(p.model_dump());DB.write_text(json.dumps(rows,indent=2));return p
@app.post("/run")
async def run(x:Run):
 p=next((p for p in read() if p["name"]==x.name),None)
 if not p:raise HTTPException(404,"Prompt not found")
 try:prompt=p["template"].format(**x.variables)
 except KeyError as e:raise HTTPException(422,f"Missing variable: {e}")
 key=os.getenv("AI_API_KEY")
 if not key: return {"rendered_prompt":prompt,"mode":"preview","note":"Set AI_API_KEY to call a model."}
 base=os.getenv("AI_BASE_URL","https://api.openai.com/v1");model=os.getenv("AI_MODEL","gpt-4o-mini")
 async with httpx.AsyncClient(timeout=60) as c:r=await c.post(base.rstrip("/")+"/chat/completions",headers={"Authorization":f"Bearer {key}"},json={"model":model,"messages":[{"role":"user","content":prompt}]})
 if r.is_error:raise HTTPException(r.status_code,"Provider request failed")
 return {"output":r.json()["choices"][0]["message"]["content"]}
@app.get("/")
def home():return {"app":"GenAI Playground","endpoints":["GET /prompts","POST /prompts","POST /run"]}