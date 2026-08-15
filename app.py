import streamlit as st

from agents.planner import plan
from agents.researcher import research
from agents.writer import write_report

from services.search import (
    gather_sources
)

from services.citations import (
    format_sources
)

from services.pdf_export import (
    create_pdf
)

# 1. Page Configuration
st.set_page_config(
    page_title="Autonomous Research Assistant Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 Autonomous Research Assistant Agent")

# 2. Initialize Session State Variables
if "research_plan" not in st.session_state:
    st.session_state.research_plan = None
if "sources" not in st.session_state:
    st.session_state.sources = None
if "report" not in st.session_state:
    st.session_state.report = None
if "pdf_path" not in st.session_state:
    st.session_state.pdf_path = None
if "current_topic" not in st.session_state:
    st.session_state.current_topic = ""

# 3. User Input
topic = st.text_input(
    "Research Topic", 
    value=st.session_state.current_topic
)

# 4. Trigger Execution Pipeline
if st.button("Start Research"):
    if not topic.strip():
        st.warning("Please enter a valid research topic.")
    else:
        # Clear previous session state for a fresh run
        st.session_state.research_plan = None
        st.session_state.sources = None
        st.session_state.report = None
        st.session_state.pdf_path = None
        st.session_state.current_topic = topic

        try:
            # Phase 1: Planning
            with st.spinner("Planning..."):
                st.session_state.research_plan = plan(topic)

            # Phase 2: Gathering Sources
            with st.spinner("Searching..."):
                st.session_state.sources = gather_sources(topic)

            if not st.session_state.sources:
                raise ValueError("No credible sources could be gathered for this topic.")

            # Phase 3: Research & Extraction
            with st.spinner("Researching..."):
                citations = format_sources(st.session_state.sources)
                findings = research(topic, st.session_state.sources)

            # Phase 4: Report Synthesis
            with st.spinner("Writing report..."):
                st.session_state.report = write_report(
                    topic, 
                    findings, 
                    citations
                )

            # Phase 5: PDF Compilation
            with st.spinner("Generating PDF export..."):
                st.session_state.pdf_path = create_pdf(
                    topic, 
                    st.session_state.report
                )
                
            st.success("Research pipeline completed successfully!")

        except Exception as e:
            st.error(f"An error occurred during the research process: {str(e)}")
            # Reset state variables on failure to avoid rendering broken data
            st.session_state.research_plan = None
            st.session_state.sources = None
            st.session_state.report = None
            st.session_state.pdf_path = None

# 5. Persistent UI Rendering (Preserves UI layout after clicks/downloads)
if st.session_state.research_plan:
    st.subheader("Research Plan")
    st.write(st.session_state.research_plan)

if st.session_state.sources:
    st.subheader("Sources")
    for s in st.session_state.sources:
        title = s.get("title", "Untitled Source")
        url = s.get("url", "#")
        st.markdown(f"### {title}\n\n{url}")

if st.session_state.report:
    st.subheader("Final Report")
    st.markdown(st.session_state.report)

if st.session_state.pdf_path:
    try:
        with open(st.session_state.pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download PDF",
                data=f,
                file_name="Research_Report.pdf",
                mime="application/pdf"
            )
    except FileNotFoundError:
        st.error("The generated PDF report file could not be found.")
    except Exception as e:
        st.error(f"Failed to load PDF download: {str(e)}")

# 6. Sidebar Credentials

with st.sidebar:
    st.markdown("Developed by Oluwasegun Oluwatosin (tosindataginius)")
    st.link_button("Visit my LinkedIn Profile", "https://www.linkedin.com/in/oluwatosin-oluwasegun-1a9266288/")
    st.link_button("Visit my GitHub Profile", "https://github.com/tosindataginius")