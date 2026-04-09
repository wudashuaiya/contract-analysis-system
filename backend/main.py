from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uuid
import asyncio
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks = {}

@app.post("/api/analysis")
async def create_analysis(contractId: str, file: UploadFile = File(...)):
    task_id = str(uuid.uuid4())
    tasks[task_id] = {
        "taskId": task_id,
        "status": "running",
        "currentStep": "初始化",
        "progress": 0,
        "logs": []
    }
    asyncio.create_task(analyze(task_id))
    return {"taskId": task_id}

async def analyze(task_id):
    for step, progress in [("提取信息", 25), ("分析风险", 50), ("生成报告", 75), ("完成", 100)]:
        await asyncio.sleep(2)
        tasks[task_id].update({
            "currentStep": step,
            "progress": progress,
            "logs": tasks[task_id]["logs"] + [{"step": step, "progress": progress}]
        })
    tasks[task_id].update({
        "status": "completed",
        "result": {
            "metadata": {"title": "测试合同", "parties": [{"name": "甲方", "role": "甲方"}]},
            "risks": [{"category": "付款风险", "level": "high", "description": "预付款过高"}],
            "score": 75
        }
    })

@app.get("/api/analysis/{task_id}")
async def get_status(task_id: str):
    return tasks.get(task_id, {"error": "not found"})

@app.get("/api/contracts/{id}")
async def get_contract(id: str):
    return {"id": id, "title": "示例"}
