"""
Kevin AI - Backend Integration Connector
Connects Streamlit UI to AI agents (kevin_agents.py)

Version: 4.0
Date: January 7, 2026
"""

import sys
import os
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from kevin_agents import (
        AgentState,
        SOPAnalysisAgent,
        ProcessMappingAgent,
        AutomationOpportunityAgent,
        FutureStateDesignAgent,
        TestCaseGeneratorAgent,
        CodeGeneratorAgent,
        KPICalculatorAgent,
        SOPOrchestrator
    )
    BACKEND_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import kevin_agents: {e}")
    BACKEND_AVAILABLE = False

def process_sop(sop_file, config):
    """
    Process SOP document through AI agents
    
    Args:
        sop_file: Uploaded file object
        config: Dict with industry, process_type, erp_system, risk_profile
    
    Returns:
        Dict with all analysis results
    """
    if not BACKEND_AVAILABLE:
        return get_mock_results()
    
    try:
        # Save uploaded file temporarily
        temp_path = f"/tmp/{sop_file.name}"
        with open(temp_path, "wb") as f:
            f.write(sop_file.getvalue())
        
        # Initialize orchestrator
        orchestrator = SOPOrchestrator()
        
        # Create initial state
        initial_state = {
            "sop_document_path": temp_path,
            "process_diagram_path": None,
            "domain": config.get("industry", "logistics"),
            "sop_text": "",
            "sop_structure": {},
            "diagram_content": None,
            "current_state_map": "",
            "current_state_steps": [],
            "gap_analysis": None,
            "automation_opportunities": [],
            "future_state_map": "",
            "future_state_architecture": {},
            "requirements": {},
            "test_cases": [],
            "generated_code": {},
            "kpi_analysis": {},
            "session_id": "demo_session",
            "timestamp": "",
            "agent_logs": [],
            "errors": []
        }
        
        # Run orchestration
        result = orchestrator.process(initial_state)
        
        # Clean up temp file
        os.remove(temp_path)
        
        return {
            "current_state_map": result.get("current_state_map", ""),
            "current_state_steps": result.get("current_state_steps", []),
            "automation_opportunities": result.get("automation_opportunities", []),
            "future_state_map": result.get("future_state_map", ""),
            "test_cases": result.get("test_cases", []),
            "generated_code": result.get("generated_code", {}),
            "kpi_analysis": result.get("kpi_analysis", {}),
            "errors": result.get("errors", [])
        }
        
    except Exception as e:
        print(f"Error processing SOP: {e}")
        return get_mock_results()

def get_mock_results():
    """
    Return mock results for demo when backend unavailable
    """
    return {
        "current_state_map": """
flowchart TD
    Start([Order]) --> A[Review Order]
    A --> B[Check Inventory]
    B --> C{Stock?}
    C -->|Yes| D[Fulfill]
    C -->|No| E[Exception]
    D --> End([Complete])
    E --> End
""",
        "current_state_steps": [
            {
                "step_id": "STEP-001",
                "description": "Review order details",
                "actor": "Customer Service",
                "duration": "5 minutes",
                "automation_candidate": True
            }
        ],
        "automation_opportunities": [
            {
                "opportunity_id": "AUTO-001",
                "title": "Automate Inventory Check",
                "type": "API Integration",
                "savings": 47112,
                "payback_months": 6.4,
                "priority": "P0"
            }
        ],
        "future_state_map": """
flowchart TD
    Start([Order]) --> A[AI Route]
    A --> B[Auto Process]
    B --> End([Complete])
""",
        "test_cases": [
            {
                "test_id": "TC-001",
                "name": "Validate Inventory API",
                "type": "Functional",
                "priority": "Critical"
            }
        ],
        "generated_code": {
            "language": "python",
            "code": "# FastAPI code here"
        },
        "kpi_analysis": {
            "annual_savings": 524000,
            "payback_months": 8.7,
            "roi_3year": 313
        },
        "errors": []
    }

# Test function
if __name__ == "__main__":
    print(f"Backend available: {BACKEND_AVAILABLE}")
    if BACKEND_AVAILABLE:
        print("✅ Successfully connected to kevin_agents.py")
    else:
        print("⚠️ Using mock data - kevin_agents.py not available")
