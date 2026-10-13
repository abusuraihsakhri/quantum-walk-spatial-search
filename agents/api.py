"""
FastAPI REST API Server for Quantum Walk Spatial Search.
"""
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .base import AuditLogger, PHIGuard
from quantum_walk.search import simulate_complete_graph
from .models import SystemTaskPayload, ConsensusDossier
from .supervisor import SystemSupervisor

supervisor = SystemSupervisor(model_provider="mock")

app = FastAPI(
    title="Quantum Walk Spatial Search API",
    description="Enterprise Distributed Component Platform (Post-Quantum Cryptography & Hardware Security)",
    version="3.0.0-ENTERPRISE",
)


class ChatRequest(BaseModel):
    query: str


@app.get("/health")
def health():
    return {"status": "HEALTHY", "service": "quantum-walk-spatial-search", "domain": "Post-Quantum Cryptography & Hardware Security", "standard": "NIST FIPS 203/204/205 / ISO/IEC 17825 Standards", "version": "3.0.0-ENTERPRISE"}


@app.get("/metrics")
def metrics():
    return {
        "dossiers_processed_total": len(supervisor.dossier_registry),
        "audit_blocks_total": len(AuditLogger.get_trail()),
        "system_status": "NOMINAL_OPTIMAL"
    }


@app.post("/api/audit")
def api_audit(payload: SystemTaskPayload):
    dossier = supervisor.process_task(payload)
    return dossier.to_dict()


class SearchRequest(BaseModel):
    node_count: int = Field(default=16, ge=2, le=100000)
    marked_vertex: int = Field(default=0, ge=0)
    gamma: Optional[float] = None
    max_time: Optional[float] = None
    samples: int = Field(default=201, ge=2, le=2001)


@app.post("/api/quantum/search")
def quantum_search(req: SearchRequest):
    """Run exact ideal continuous-time search on the complete graph."""
    try:
        return simulate_complete_graph(req.node_count, req.marked_vertex, req.gamma, req.max_time, req.samples)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/chat")
def api_chat(req: ChatRequest):
    try:
        ans = supervisor.query_supervisory_chat(req.query)
        return {"response": ans}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/audit/logs")
def api_audit_logs():
    return {"audit_trail": AuditLogger.get_trail(), "verified": AuditLogger.verify_integrity()}
