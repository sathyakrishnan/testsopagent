"""
Kevin AI - FastAPI Application
REST API for SOP to Agentic Automation

Version: 2.0
Date: January 6, 2026
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
import uvicorn
import os
import shutil
from datetime import datetime
import json

from kevin_agents import MasterOrchestratorAgent, AgentState

# ============================================================================
# APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Kevin AI - SOP Automation Platform",
    description="Enterprise-grade SOP to Agentic Automation transformation",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure based on environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Storage directories
UPLOAD_DIR = "./uploads"
OUTPUT_DIR = "./outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Global orchestrator instance
orchestrator = None

def get_orchestrator():
    """Dependency to get orchestrator instance"""
    global orchestrator
    if orchestrator is None:
        orchestrator = MasterOrchestratorAgent()
    return orchestrator

# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class ProcessRequest(BaseModel):
    """Request model for SOP processing"""
    domain: str = Field(default="logistics", description="Business domain (logistics, insurance, finance, healthcare)")
    include_gap_analysis: bool = Field(default=False, description="Include gap analysis if diagram provided")
    generate_code: bool = Field(default=True, description="Generate production-ready code")
    calculate_roi: bool = Field(default=True, description="Calculate KPI/SLA improvements")

class ProcessResponse(BaseModel):
    """Response model for SOP processing"""
    session_id: str
    status: str
    timestamp: str
    current_state_map: Optional[str] = None
    future_state_map: Optional[str] = None
    automation_opportunities_count: int = 0
    test_cases_count: int = 0
    estimated_savings_annual: Optional[float] = None
    errors: List[str] = []

class AutomationOpportunity(BaseModel):
    """Model for automation opportunity"""
    step_id: str
    description: str
    automation_type: str
    complexity: str
    roi_score: float
    priority: str
    estimated_savings_annual: float

class TestCase(BaseModel):
    """Model for test case"""
    test_id: str
    test_name: str
    test_type: str
    priority: str
    preconditions: str
    test_steps: List[str]
    expected_results: str

# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Kevin AI",
        "version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/v1/status")
async def get_status():
    """Get API status"""
    return {
        "api_version": "v1",
        "llm_provider": os.getenv("LLM_PROVIDER", "azure"),
        "features": {
            "sop_analysis": True,
            "gap_identification": True,
            "automation_discovery": True,
            "code_generation": True,
            "test_generation": True,
            "roi_calculation": True
        },
        "timestamp": datetime.now().isoformat()
    }

# ============================================================================
# SOP PROCESSING ENDPOINTS
# ============================================================================

@app.post("/api/v1/process/sop", response_model=ProcessResponse)
async def process_sop(
    sop_file: UploadFile = File(...),
    diagram_file: Optional[UploadFile] = File(None),
    domain: str = "logistics",
    orchestrator: MasterOrchestratorAgent = Depends(get_orchestrator)
):
    """
    Process SOP document and generate automation artifacts
    
    Args:
        sop_file: SOP document (PDF, DOCX, or Mermaid)
        diagram_file: Optional process diagram (PNG, JPG)
        domain: Business domain
    
    Returns:
        ProcessResponse with session ID and summary
    """
    
    try:
        # Save uploaded files
        session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = os.path.join(UPLOAD_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        sop_path = os.path.join(session_dir, sop_file.filename)
        with open(sop_path, "wb") as f:
            shutil.copyfileobj(sop_file.file, f)
        
        diagram_path = None
        if diagram_file:
            diagram_path = os.path.join(session_dir, diagram_file.filename)
            with open(diagram_path, "wb") as f:
                shutil.copyfileobj(diagram_file.file, f)
        
        # Process through orchestrator
        print(f"Processing SOP for session: {session_id}")
        result = orchestrator.process(sop_path, diagram_path, domain)
        
        # Save outputs
        output_dir = os.path.join(OUTPUT_DIR, session_id)
        os.makedirs(output_dir, exist_ok=True)
        
        with open(os.path.join(output_dir, "full_result.json"), "w") as f:
            # Convert to serializable format
            serializable_result = {
                k: v for k, v in result.items() 
                if k not in ['agent_logs', 'errors'] or isinstance(v, (str, int, float, list, dict, type(None)))
            }
            json.dump(serializable_result, f, indent=2, default=str)
        
        # Save individual artifacts
        with open(os.path.join(output_dir, "current_state_map.mermaid"), "w") as f:
            f.write(result["current_state_map"])
        
        with open(os.path.join(output_dir, "future_state_map.mermaid"), "w") as f:
            f.write(result["future_state_map"])
        
        with open(os.path.join(output_dir, "automation_opportunities.json"), "w") as f:
            json.dump(result["automation_opportunities"], f, indent=2)
        
        with open(os.path.join(output_dir, "test_cases.json"), "w") as f:
            json.dump(result["test_cases"], f, indent=2)
        
        with open(os.path.join(output_dir, "generated_code.txt"), "w") as f:
            f.write(result["generated_code"].get("code", ""))
        
        with open(os.path.join(output_dir, "kpi_analysis.json"), "w") as f:
            json.dump(result["kpi_analysis"], f, indent=2)
        
        # Calculate total annual savings
        total_savings = sum(
            opp.get("estimated_savings_annual", 0) 
            for opp in result["automation_opportunities"]
        )
        
        return ProcessResponse(
            session_id=session_id,
            status="completed",
            timestamp=result["timestamp"],
            current_state_map=result["current_state_map"],
            future_state_map=result["future_state_map"],
            automation_opportunities_count=len(result["automation_opportunities"]),
            test_cases_count=len(result["test_cases"]),
            estimated_savings_annual=total_savings,
            errors=result.get("errors", [])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/results/{session_id}")
async def get_results(session_id: str):
    """Get full results for a session"""
    
    result_path = os.path.join(OUTPUT_DIR, session_id, "full_result.json")
    if not os.path.exists(result_path):
        raise HTTPException(status_code=404, detail="Session not found")
    
    with open(result_path, "r") as f:
        results = json.load(f)
    
    return results

@app.get("/api/v1/results/{session_id}/current-state-map")
async def get_current_state_map(session_id: str):
    """Get current state process map"""
    
    map_path = os.path.join(OUTPUT_DIR, session_id, "current_state_map.mermaid")
    if not os.path.exists(map_path):
        raise HTTPException(status_code=404, detail="Current state map not found")
    
    return FileResponse(map_path, media_type="text/plain", filename="current_state_map.mermaid")

@app.get("/api/v1/results/{session_id}/future-state-map")
async def get_future_state_map(session_id: str):
    """Get future state process map"""
    
    map_path = os.path.join(OUTPUT_DIR, session_id, "future_state_map.mermaid")
    if not os.path.exists(map_path):
        raise HTTPException(status_code=404, detail="Future state map not found")
    
    return FileResponse(map_path, media_type="text/plain", filename="future_state_map.mermaid")

@app.get("/api/v1/results/{session_id}/automation-opportunities")
async def get_automation_opportunities(session_id: str):
    """Get automation opportunities"""
    
    opp_path = os.path.join(OUTPUT_DIR, session_id, "automation_opportunities.json")
    if not os.path.exists(opp_path):
        raise HTTPException(status_code=404, detail="Automation opportunities not found")
    
    with open(opp_path, "r") as f:
        opportunities = json.load(f)
    
    return opportunities

@app.get("/api/v1/results/{session_id}/test-cases")
async def get_test_cases(session_id: str):
    """Get test cases"""
    
    test_path = os.path.join(OUTPUT_DIR, session_id, "test_cases.json")
    if not os.path.exists(test_path):
        raise HTTPException(status_code=404, detail="Test cases not found")
    
    with open(test_path, "r") as f:
        test_cases = json.load(f)
    
    return test_cases

@app.get("/api/v1/results/{session_id}/generated-code")
async def get_generated_code(session_id: str):
    """Get generated code"""
    
    code_path = os.path.join(OUTPUT_DIR, session_id, "generated_code.txt")
    if not os.path.exists(code_path):
        raise HTTPException(status_code=404, detail="Generated code not found")
    
    return FileResponse(code_path, media_type="text/plain", filename="generated_code.txt")

@app.get("/api/v1/results/{session_id}/kpi-analysis")
async def get_kpi_analysis(session_id: str):
    """Get KPI/SLA analysis"""
    
    kpi_path = os.path.join(OUTPUT_DIR, session_id, "kpi_analysis.json")
    if not os.path.exists(kpi_path):
        raise HTTPException(status_code=404, detail="KPI analysis not found")
    
    with open(kpi_path, "r") as f:
        kpi_analysis = json.load(f)
    
    return kpi_analysis

@app.get("/api/v1/sessions")
async def list_sessions():
    """List all processing sessions"""
    
    if not os.path.exists(OUTPUT_DIR):
        return {"sessions": []}
    
    sessions = []
    for session_id in os.listdir(OUTPUT_DIR):
        session_path = os.path.join(OUTPUT_DIR, session_id)
        if os.path.isdir(session_path):
            result_path = os.path.join(session_path, "full_result.json")
            if os.path.exists(result_path):
                with open(result_path, "r") as f:
                    result = json.load(f)
                    sessions.append({
                        "session_id": session_id,
                        "timestamp": result.get("timestamp"),
                        "domain": result.get("domain"),
                        "automation_opportunities": len(result.get("automation_opportunities", [])),
                        "test_cases": len(result.get("test_cases", []))
                    })
    
    return {"sessions": sorted(sessions, key=lambda x: x["timestamp"], reverse=True)}

# ============================================================================
# EXPORT ENDPOINTS
# ============================================================================

@app.get("/api/v1/export/{session_id}/package")
async def export_package(session_id: str):
    """Export complete package as ZIP"""
    
    import zipfile
    from io import BytesIO
    
    output_dir = os.path.join(OUTPUT_DIR, session_id)
    if not os.path.exists(output_dir):
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Create ZIP in memory
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(output_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, output_dir)
                zip_file.write(file_path, arcname)
    
    zip_buffer.seek(0)
    
    return Response(
        content=zip_buffer.getvalue(),
        media_type="application/zip",
        headers={"Content-Disposition": f"attachment; filename=kevin_ai_{session_id}.zip"}
    )

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    uvicorn.run(
        "kevin_api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
