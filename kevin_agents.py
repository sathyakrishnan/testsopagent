"""
Kevin AI - SOP to Agentic Automation Platform
Main Agentic System with 9 Specialized Agents

Version: 2.0
Date: January 6, 2026
Client: Cars Commerce
"""

import os
import json
from typing import Dict, List, Optional, TypedDict, Annotated
from datetime import datetime
import operator

# LangChain and LangGraph imports
from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor, ToolInvocation
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings

# Document processing
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from docx import Document as DocxDocument

# ============================================================================
# CONFIGURATION
# ============================================================================

class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    # LLM Configuration
    LLM_PROVIDER: str = "azure"  # azure, openai, anthropic
    
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4o"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_EMBEDDING_DEPLOYMENT: str = "text-embedding-3-large"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o"
    
    # Anthropic
    ANTHROPIC_API_KEY: str = ""
    ANTHROPIC_MODEL: str = "claude-sonnet-4-5-20250929"
    
    # Application
    TEMPERATURE: float = 0.1
    MAX_TOKENS: int = 4000
    VECTOR_DB_PATH: str = "./vectordb"
    OUTPUT_DIR: str = "./output"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()

# ============================================================================
# STATE DEFINITION
# ============================================================================

class AgentState(TypedDict):
    """Shared state across all agents"""
    # Input
    sop_document_path: str
    process_diagram_path: Optional[str]
    domain: str  # insurance, logistics, finance, healthcare
    
    # Extracted Content
    sop_text: str
    sop_structure: Dict
    diagram_content: Optional[Dict]
    
    # Analysis Results
    current_state_map: str  # Mermaid diagram
    current_state_steps: List[Dict]
    gap_analysis: Optional[Dict]
    
    # Automation Analysis
    automation_opportunities: List[Dict]
    future_state_map: str
    future_state_architecture: Dict
    
    # Outputs
    requirements: Dict
    test_cases: List[Dict]
    generated_code: Dict
    kpi_analysis: Dict
    
    # Metadata
    session_id: str
    timestamp: str
    agent_logs: Annotated[List[str], operator.add]
    errors: Annotated[List[str], operator.add]

# ============================================================================
# LLM FACTORY
# ============================================================================

def get_llm(model_name: Optional[str] = None, temperature: Optional[float] = None):
    """Factory method to get configured LLM based on provider"""
    
    temp = temperature if temperature is not None else settings.TEMPERATURE
    
    if settings.LLM_PROVIDER == "azure":
        return AzureChatOpenAI(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment_name=model_name or settings.AZURE_OPENAI_DEPLOYMENT_NAME,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            temperature=temp,
            max_tokens=settings.MAX_TOKENS
        )
    elif settings.LLM_PROVIDER == "openai":
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=model_name or settings.OPENAI_MODEL,
            temperature=temp,
            max_tokens=settings.MAX_TOKENS
        )
    elif settings.LLM_PROVIDER == "anthropic":
        return ChatAnthropic(
            api_key=settings.ANTHROPIC_API_KEY,
            model=model_name or settings.ANTHROPIC_MODEL,
            temperature=temp,
            max_tokens=settings.MAX_TOKENS
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

def get_embeddings():
    """Get embeddings model based on provider"""
    if settings.LLM_PROVIDER == "azure":
        return AzureOpenAIEmbeddings(
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
            api_key=settings.AZURE_OPENAI_API_KEY,
            deployment=settings.AZURE_EMBEDDING_DEPLOYMENT,
            api_version=settings.AZURE_OPENAI_API_VERSION
        )
    else:
        return OpenAIEmbeddings(
            api_key=settings.OPENAI_API_KEY
        )

# ============================================================================
# DOCUMENT PROCESSING UTILITIES
# ============================================================================

class DocumentProcessor:
    """Process various document formats"""
    
    @staticmethod
    def extract_pdf(file_path: str) -> tuple[str, bool]:
        """Extract text from PDF, returns (text, is_ocr_needed)"""
        doc = fitz.open(file_path)
        text = ""
        is_ocr = False
        
        for page in doc:
            page_text = page.get_text()
            if len(page_text.strip()) < 50:  # Likely scanned
                is_ocr = True
                # Convert page to image and OCR
                pix = page.get_pixmap()
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                page_text = pytesseract.image_to_string(img)
            text += page_text + "\n"
        
        return text, is_ocr
    
    @staticmethod
    def extract_docx(file_path: str) -> str:
        """Extract text from DOCX"""
        doc = DocxDocument(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    
    @staticmethod
    def extract_image(file_path: str) -> str:
        """Extract text from image using OCR"""
        img = Image.open(file_path)
        text = pytesseract.image_to_string(img)
        return text
    
    @staticmethod
    def parse_structure(text: str) -> Dict:
        """Parse document structure (sections, tables, lists)"""
        # Simple structure parsing - can be enhanced
        lines = text.split('\n')
        structure = {
            "sections": [],
            "current_section": "Introduction",
            "steps": [],
            "decision_points": [],
            "actors": set(),
            "systems": set()
        }
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Detect sections (all caps or numbered)
            if line.isupper() and len(line) > 5:
                structure["sections"].append(line)
                structure["current_section"] = line
            
            # Detect numbered steps
            if line[0].isdigit() and ('.' in line[:4] or ')' in line[:4]):
                structure["steps"].append({
                    "step_number": i + 1,
                    "section": structure["current_section"],
                    "text": line,
                    "type": "manual"  # default
                })
        
        structure["actors"] = list(structure["actors"])
        structure["systems"] = list(structure["systems"])
        return structure

# ============================================================================
# AGENT 1: SOP ANALYSIS AGENT
# ============================================================================

class SOPAnalysisAgent:
    """Deep SOP understanding and structure extraction"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
        self.processor = DocumentProcessor()
    
    def analyze(self, state: AgentState) -> AgentState:
        """Analyze SOP document"""
        print("🔍 SOP Analysis Agent: Analyzing SOP document...")
        
        # Extract text
        file_path = state["sop_document_path"]
        if file_path.endswith('.pdf'):
            text, is_ocr = self.processor.extract_pdf(file_path)
        elif file_path.endswith('.docx'):
            text = self.processor.extract_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        
        state["sop_text"] = text
        state["sop_structure"] = self.processor.parse_structure(text)
        
        # Use LLM to extract detailed process information
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert business process analyst. Analyze the provided SOP document and extract:
1. All process steps in sequential order
2. Decision points and conditions
3. Actors/roles involved
4. Systems/tools mentioned
5. Input/output of each step
6. Manual vs automated steps
7. Exception handling procedures

Format your response as structured JSON."""),
            ("user", "SOP Document:\n\n{sop_text}\n\nProvide comprehensive process analysis.")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"sop_text": text[:10000]})  # Limit context
        
        # Parse LLM response
        try:
            # Extract JSON from response
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0]
            else:
                json_str = content
            
            detailed_analysis = json.loads(json_str)
            state["sop_structure"]["detailed_analysis"] = detailed_analysis
        except:
            state["errors"].append("Failed to parse LLM response for SOP analysis")
        
        state["agent_logs"].append(f"SOP Analysis Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 2: PROCESS MAPPING AGENT
# ============================================================================

class ProcessMappingAgent:
    """Generate visual process representations"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
    
    def map_process(self, state: AgentState) -> AgentState:
        """Generate current state process map"""
        print("📊 Process Mapping Agent: Creating current state process map...")
        
        sop_structure = state["sop_structure"]
        detailed_analysis = sop_structure.get("detailed_analysis", {})
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in process modeling. Create a Mermaid flowchart diagram representing the current state process.

Requirements:
1. Use proper Mermaid syntax (flowchart TD)
2. Include all process steps
3. Show decision points with diamond shapes
4. Indicate manual steps with (Manual) suffix
5. Show parallel processes where applicable
6. Use descriptive node labels
7. Include swim lanes for different actors if applicable

Example format:
```mermaid
flowchart TD
    Start([Process Start]) --> A[Step 1]
    A --> B{Decision?}
    B -->|Yes| C[Step 2]
    B -->|No| D[Step 3]
    C --> End([Process End])
    D --> End
```

Create a comprehensive, accurate process map."""),
            ("user", """SOP Structure: {sop_structure}

Generate the Mermaid flowchart for the current state process.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({"sop_structure": json.dumps(detailed_analysis, indent=2)})
        
        # Extract Mermaid diagram
        content = response.content
        if "```mermaid" in content:
            mermaid = content.split("```mermaid")[1].split("```")[0].strip()
        elif "```" in content:
            mermaid = content.split("```")[1].split("```")[0].strip()
        else:
            mermaid = content.strip()
        
        state["current_state_map"] = mermaid
        state["agent_logs"].append(f"Process Mapping Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 3: GAP IDENTIFICATION AGENT
# ============================================================================

class GapIdentificationAgent:
    """Identify gaps between SOP and diagram"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
    
    def identify_gaps(self, state: AgentState) -> AgentState:
        """Identify gaps if diagram provided"""
        print("🔎 Gap Identification Agent: Analyzing gaps...")
        
        if not state.get("process_diagram_path"):
            state["gap_analysis"] = None
            state["agent_logs"].append("Gap Identification skipped - no diagram provided")
            return state
        
        # Extract diagram content
        diagram_path = state["process_diagram_path"]
        if diagram_path.endswith(('.png', '.jpg', '.jpeg')):
            # Use vision model to understand diagram
            # For MVP, skip actual vision processing
            state["diagram_content"] = {"type": "image", "analysis": "Not implemented in MVP"}
        
        # Compare SOP and diagram
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in process analysis. Compare the SOP document with the provided process diagram and identify:
1. Missing steps in the diagram
2. Steps in diagram not mentioned in SOP
3. Discrepancies in sequence
4. Ambiguous descriptions
5. Inconsistent terminology

Provide specific, actionable recommendations."""),
            ("user", """SOP Text: {sop_text}

Current State Map: {current_state_map}

Identify all gaps and provide recommendations.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "sop_text": state["sop_text"][:5000],
            "current_state_map": state["current_state_map"]
        })
        
        state["gap_analysis"] = {
            "analysis": response.content,
            "timestamp": datetime.now().isoformat()
        }
        state["agent_logs"].append(f"Gap Identification Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 4: AUTOMATION OPPORTUNITY AGENT
# ============================================================================

class AutomationOpportunityAgent:
    """Identify automation opportunities"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.2)
    
    def identify_opportunities(self, state: AgentState) -> AgentState:
        """Identify and prioritize automation opportunities"""
        print("🤖 Automation Opportunity Agent: Identifying automation potential...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an automation expert. Analyze each process step and classify it into:

1. **RPA Candidate** - Repetitive, rule-based, high-volume tasks
2. **API Integration** - System-to-system data exchange
3. **Agentic AI** - Decision-making, natural language processing, complex reasoning
4. **Human-in-the-Loop** - Requires human judgment but can be AI-assisted

For each opportunity, provide:
- Step ID and description
- Automation type
- Complexity (Low/Medium/High)
- Estimated ROI score (1-10)
- Recommended tools/technologies
- Implementation priority (P0/P1/P2/P3)
- Estimated time savings (hours/week)
- Cost savings ($/year)

Format as JSON array."""),
            ("user", """Process Steps: {process_steps}

Domain: {domain}

Identify all automation opportunities.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "process_steps": json.dumps(state["sop_structure"].get("steps", []), indent=2),
            "domain": state["domain"]
        })
        
        # Parse response
        try:
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0]
            else:
                json_str = content
            
            opportunities = json.loads(json_str)
            state["automation_opportunities"] = opportunities
        except:
            state["errors"].append("Failed to parse automation opportunities")
            state["automation_opportunities"] = []
        
        state["agent_logs"].append(f"Automation Opportunity Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 5: FUTURE STATE DESIGN AGENT
# ============================================================================

class FutureStateDesignAgent:
    """Design optimized future state process"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.2)
    
    def design_future_state(self, state: AgentState) -> AgentState:
        """Create optimized future state design"""
        print("🚀 Future State Design Agent: Designing optimized process...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a digital transformation expert. Design an optimized future state process that:

1. Eliminates redundant steps
2. Implements parallel processing where possible
3. Integrates automation opportunities
4. Adds exception handling
5. Improves efficiency and reduces cycle time
6. Maintains compliance and quality

Create a Mermaid flowchart showing the optimized process with:
- Automated steps clearly marked
- AI agent integration points
- API calls
- Exception handling flows
- Performance improvements highlighted

Also provide a digital twin architecture showing:
- Services/microservices
- Data flows
- Integration points
- Technology stack"""),
            ("user", """Current State Map: {current_state_map}

Automation Opportunities: {automation_opportunities}

Domain: {domain}

Design the optimized future state.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "current_state_map": state["current_state_map"],
            "automation_opportunities": json.dumps(state["automation_opportunities"], indent=2),
            "domain": state["domain"]
        })
        
        content = response.content
        
        # Extract Mermaid diagram
        if "```mermaid" in content:
            mermaid = content.split("```mermaid")[1].split("```")[0].strip()
        else:
            mermaid = state["current_state_map"]  # Fallback
        
        state["future_state_map"] = mermaid
        
        # Extract architecture description
        state["future_state_architecture"] = {
            "description": content,
            "timestamp": datetime.now().isoformat()
        }
        
        state["agent_logs"].append(f"Future State Design Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 6: TEST CASE GENERATOR AGENT
# ============================================================================

class TestCaseGeneratorAgent:
    """Generate comprehensive test scenarios"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
    
    def generate_test_cases(self, state: AgentState) -> AgentState:
        """Generate test cases for all process steps"""
        print("🧪 Test Case Generator Agent: Creating test scenarios...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a QA expert. Generate comprehensive test cases for the future state process:

For each process step, create:
1. **Unit Tests** - Test individual components
2. **Integration Tests** - Test system interactions
3. **End-to-End Tests** - Test complete workflows
4. **Edge Cases** - Test boundary conditions
5. **Error Scenarios** - Test exception handling

Each test case should include:
- Test ID (unique)
- Test Name
- Test Type (Unit/Integration/E2E/Edge/Error)
- Preconditions
- Test Steps (detailed)
- Test Data
- Expected Results
- Priority (P0/P1/P2)
- Coverage Area (which process steps)

Format as JSON array."""),
            ("user", """Future State Map: {future_state_map}

Automation Opportunities: {automation_opportunities}

Generate comprehensive test cases.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "future_state_map": state["future_state_map"],
            "automation_opportunities": json.dumps(state["automation_opportunities"], indent=2)
        })
        
        # Parse response
        try:
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0]
            else:
                json_str = content
            
            test_cases = json.loads(json_str)
            state["test_cases"] = test_cases
        except:
            state["errors"].append("Failed to parse test cases")
            state["test_cases"] = []
        
        state["agent_logs"].append(f"Test Case Generator Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 7: CODE GENERATOR AGENT
# ============================================================================

class CodeGeneratorAgent:
    """Generate production-ready code"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
    
    def generate_code(self, state: AgentState) -> AgentState:
        """Generate FastAPI and agentic workflow code"""
        print("💻 Code Generator Agent: Generating production code...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert software architect. Generate production-ready code for the agentic process automation:

Create:
1. **FastAPI Application** - API endpoints for each process step
2. **Pydantic Models** - Data models for requests/responses
3. **Service Layer** - Business logic implementation
4. **Agent Definitions** - LangGraph agent workflows
5. **Integration Connectors** - External system integrations
6. **Error Handling** - Comprehensive exception handling
7. **Logging** - Structured logging with OpenTelemetry
8. **Configuration** - Environment-based config
9. **Docker Setup** - Containerization
10. **Tests** - Unit and integration tests

Use best practices:
- Type hints
- Async/await where appropriate
- Dependency injection
- Circuit breakers for external calls
- Rate limiting
- Authentication/authorization
- API versioning
- OpenAPI documentation

Organize code in proper structure:
```
/api
  /endpoints
    __init__.py
    process.py
    health.py
/models
  process_models.py
/services
  process_service.py
/agents
  agent_definitions.py
/integrations
  external_systems.py
/utils
  logging.py
  config.py
main.py
```

Generate complete, production-ready code."""),
            ("user", """Future State Architecture: {architecture}

Automation Opportunities: {automation_opportunities}

Domain: {domain}

Generate complete code structure.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "architecture": json.dumps(state["future_state_architecture"], indent=2),
            "automation_opportunities": json.dumps(state["automation_opportunities"], indent=2),
            "domain": state["domain"]
        })
        
        state["generated_code"] = {
            "code": response.content,
            "timestamp": datetime.now().isoformat()
        }
        
        state["agent_logs"].append(f"Code Generator Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 8: KPI/SLA CALCULATOR AGENT
# ============================================================================

class KPISLACalculatorAgent:
    """Calculate performance improvements"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.1)
    
    def calculate_kpis(self, state: AgentState) -> AgentState:
        """Calculate KPI improvements and ROI"""
        print("📈 KPI/SLA Calculator Agent: Analyzing performance improvements...")
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a business analyst expert. Calculate the performance improvements from process optimization:

Analyze:
1. **Cycle Time** - Current vs future state processing time
2. **Cost per Transaction** - Current vs future cost
3. **Error Rate** - Expected reduction in errors
4. **SLA Compliance** - Improvement in meeting SLAs
5. **Resource Utilization** - Efficiency gains
6. **Customer Satisfaction** - Expected CSAT improvement
7. **ROI** - Return on investment calculation

For each metric, provide:
- Current baseline (estimated if not available)
- Future state projection
- Improvement percentage
- Annual savings
- Assumptions

Also calculate:
- Implementation cost estimate
- Payback period
- 3-year NPV
- Risk factors

Format as structured JSON."""),
            ("user", """Process Steps: {process_steps}

Automation Opportunities: {automation_opportunities}

Future State: {future_state}

Calculate comprehensive KPIs and ROI.""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({
            "process_steps": json.dumps(state["sop_structure"].get("steps", []), indent=2),
            "automation_opportunities": json.dumps(state["automation_opportunities"], indent=2),
            "future_state": state["future_state_map"]
        })
        
        # Parse response
        try:
            content = response.content
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0]
            else:
                json_str = content
            
            kpi_analysis = json.loads(json_str)
            state["kpi_analysis"] = kpi_analysis
        except:
            state["errors"].append("Failed to parse KPI analysis")
            state["kpi_analysis"] = {}
        
        state["agent_logs"].append(f"KPI/SLA Calculator Agent completed at {datetime.now()}")
        return state

# ============================================================================
# AGENT 9: MASTER ORCHESTRATOR AGENT
# ============================================================================

class MasterOrchestratorAgent:
    """Orchestrate all agents and maintain state"""
    
    def __init__(self):
        self.llm = get_llm(temperature=0.0)
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build LangGraph workflow"""
        
        # Create agent instances
        sop_agent = SOPAnalysisAgent()
        mapping_agent = ProcessMappingAgent()
        gap_agent = GapIdentificationAgent()
        automation_agent = AutomationOpportunityAgent()
        future_agent = FutureStateDesignAgent()
        test_agent = TestCaseGeneratorAgent()
        code_agent = CodeGeneratorAgent()
        kpi_agent = KPISLACalculatorAgent()
        
        # Build graph
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("sop_analysis", sop_agent.analyze)
        workflow.add_node("process_mapping", mapping_agent.map_process)
        workflow.add_node("gap_identification", gap_agent.identify_gaps)
        workflow.add_node("automation_opportunity", automation_agent.identify_opportunities)
        workflow.add_node("future_state_design", future_agent.design_future_state)
        workflow.add_node("test_case_generation", test_agent.generate_test_cases)
        workflow.add_node("code_generation", code_agent.generate_code)
        workflow.add_node("kpi_calculation", kpi_agent.calculate_kpis)
        
        # Define workflow
        workflow.set_entry_point("sop_analysis")
        workflow.add_edge("sop_analysis", "process_mapping")
        workflow.add_edge("process_mapping", "gap_identification")
        workflow.add_edge("gap_identification", "automation_opportunity")
        workflow.add_edge("automation_opportunity", "future_state_design")
        workflow.add_edge("future_state_design", "test_case_generation")
        workflow.add_edge("test_case_generation", "code_generation")
        workflow.add_edge("code_generation", "kpi_calculation")
        workflow.add_edge("kpi_calculation", END)
        
        return workflow.compile()
    
    def process(self, sop_path: str, diagram_path: Optional[str] = None, domain: str = "logistics") -> AgentState:
        """Process SOP through all agents"""
        
        initial_state: AgentState = {
            "sop_document_path": sop_path,
            "process_diagram_path": diagram_path,
            "domain": domain,
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
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "agent_logs": [],
            "errors": []
        }
        
        # Execute workflow
        final_state = self.graph.invoke(initial_state)
        return final_state

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    print("Kevin AI - SOP to Agentic Automation Platform")
    print("=" * 60)
    
    # Initialize orchestrator
    orchestrator = MasterOrchestratorAgent()
    
    # For demo purposes
    print("\n⚠️  Demo Mode: Please provide actual SOP document path")
    print("Example: python kevin_agents.py /path/to/sop.pdf /path/to/diagram.png logistics")
