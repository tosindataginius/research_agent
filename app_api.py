import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Import your existing agent logic
from agents.planner import plan
from services.search import gather_sources
from agents.researcher import research
from agents.writer import write_report
from services.citations import format_sources
from services.pdf_export import create_pdf

app = FastAPI(
    title="Autonomous Research Agent API",
    description="API for multi-agent autonomous research and report generation.",
    version="1.0.0"
)

# Input data validator schema
class ResearchRequest(BaseModel):
    topic: str

# Output data structure schema
class ResearchResponse(BaseModel):
    topic: str
    research_plan: str
    sources: list[dict]
    findings: str
    report: str
    pdf_path: str


@app.post("/api/research", response_model=ResearchResponse)
async def run_research(request: ResearchRequest):
    """
    Executes the full autonomous research pipeline:
    Planning -> Gathering Sources -> Researching -> Report Writing -> PDF Generation
    """
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Research topic cannot be empty.")
    
    try:
        # 1. Planning phase
        research_plan = plan(request.topic)
        
        # 2. Source aggregation phase
        sources = gather_sources(request.topic)
        citations = format_sources(sources)
        
        # 3. Deep research phase
        findings = research(request.topic, sources)
        
        # 4. Content generation phase
        report = write_report(request.topic, findings, citations)
        
        # 5. Asset compilation phase (Generates file on host machine)
        pdf_path = create_pdf(request.topic, report)
        
        # Format clean dictionary structures for the API response
        clean_sources = [
            {"title": s.get("title", "Untitled"), "url": s.get("url", "")} 
            for s in sources
        ]
        
        return ResearchResponse(
            topic=request.topic,
            research_plan=research_plan,
            sources=clean_sources,
            findings=findings,
            report=report,
            pdf_path=pdf_path
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {str(e)}")


@app.get("/api/download-pdf")
async def download_pdf(file_path: str):
    """
    Securely serves the compiled research PDF from the host filesystem
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Requested report PDF file not found.")
        
    return FileResponse(
        path=file_path, 
        media_type="application/pdf", 
        filename="Research_Report.pdf"
    )
