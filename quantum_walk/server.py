"""
FastAPI REST API Server for Continuous-Time & Discrete Quantum Walk Graph Search Agent.
"""
from typing import Dict, Any, Optional
from .models import FrontierPayload
from .search import simulate_complete_graph
from .agents import QuantumWalkCoordinator

coordinator = QuantumWalkCoordinator()


def create_app():
    try:
        from fastapi import FastAPI
        from pydantic import BaseModel, Field

        app = FastAPI(
            title="Continuous-Time & Discrete Quantum Walk Graph Search Agent",
            description="Simulates coin and shift operators on graph adjacency spectra, finding target marked vertices with quadratic speedup.",
            version="2.0.0-FRONTIER",
        )

        class TaskRequest(BaseModel):
            task_id: str = "TASK-2026-001"
            target_identifier: str = "TARGET-BIO-KEY"
            primary_metric: float = 28.5
            secondary_metric: float = 14.2
            status_descriptor: str = "DISCORDANT_ANOMALY"
            is_critical_flag: bool = True
            attributes: Dict[str, Any] = {}

        class ChatRequest(BaseModel):
            query: str

        class SearchRequest(BaseModel):
            node_count: int = Field(default=16, ge=2, le=100000)
            marked_vertex: int = Field(default=0, ge=0)
            gamma: Optional[float] = None
            max_time: Optional[float] = None
            samples: int = Field(default=201, ge=2, le=2001)

        @app.post("/api/quantum/search")
        def quantum_search(req: SearchRequest):
            from fastapi import HTTPException
            try:
                return simulate_complete_graph(req.node_count, req.marked_vertex, req.gamma, req.max_time, req.samples)
            except ValueError as exc:
                raise HTTPException(status_code=422, detail=str(exc)) from exc

        @app.get("/health")
        def health():
            return {"status": "HEALTHY", "system": "quantum-walk-spatial-search", "domain": "Quantum Algorithms", "version": "2.0.0-FRONTIER"}

        @app.post("/api/audit")
        def api_audit(req: TaskRequest):
            payload = FrontierPayload(
                task_id=req.task_id,
                target_identifier=req.target_identifier,
                primary_metric=req.primary_metric,
                secondary_metric=req.secondary_metric,
                status_descriptor=req.status_descriptor,
                is_critical_flag=req.is_critical_flag,
                attributes=req.attributes,
            )
            return coordinator.process(payload)

        @app.post("/api/chat")
        def api_chat(req: ChatRequest):
            return {"response": coordinator.query_supervisory_chat(req.query)}

        return app
    except ImportError:
        return None
