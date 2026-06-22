import streamlit as st

# Core agent imports
from agents.planner import plan
from agents.researcher import research
from agents.writer import write_report

# Background utility integrations
from services.search import gather_sources
from services.citations import format_sources
from services.pdf_export import create_pdf

# 1. PAGE SETUP
st.set_page_config(
    page_title="Autonomous Research Assistant Agent",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔬 Autonomous Research Assistant Agent")

# 2. DATA CAPTURE INPUTS
topic = st.text_input("Research Topic")

# 3. INTERACTIVE PROCESS FLOW RUNNER
if st.button("Start Research"):
    if not topic.strip():
        st.warning("Please enter a valid research topic before continuing.")
    else:
        # Flag to cleanly halt execution if any background node fails
        execution_failed = False

        # --- STEP A: INITIAL PLANNING WINDOW ---
        with st.spinner("Planning research objectives..."):
            plan_result = plan(topic)

        # Check if the planner node returned a safe backend error dictionary
        if isinstance(plan_result, dict) and plan_result.get("status") == "error":
            st.error(f"⚠️ Planning Phase Blocked: {plan_result['content']}")
            execution_failed = True
        else:
            st.subheader("Research Plan")
            st.write(plan_result)

        # --- STEP B: WEB SEARCH & DOCUMENT RECOVERY ---
        if not execution_failed:
            with st.spinner("Searching and harvesting online references..."):
                try:
                    sources = gather_sources(topic)
                    citations = format_sources(sources)
                except Exception as search_err:
                    st.error("⚠️ Failed to securely harvest data references from search indexes.")
                    st.exception(search_err)
                    execution_failed = True

        # Render sources markdown container safely
        if not execution_failed and sources:
            st.subheader("Sources")
            for s in sources:
                st.markdown(f"### {s.get('title', 'Untitled Source')}\n\n{s.get('url', '#')}")

        # --- STEP C: INFORMATION RESEARCH EXTREMES ---
        if not execution_failed:
            with st.spinner("Deep processing and extracting source findings..."):
                research_result = research(topic, sources)

            if isinstance(research_result, dict) and research_result.get("status") == "error":
                st.error(f"⚠️ Research Phase Blocked: {research_result['content']}")
                execution_failed = True

        # --- STEP D: STRUCTURING FINAL SYNTHESIZED REPORT ---
        if not execution_failed:
            with st.spinner("Writing finalized document text report..."):
                # Use raw content payload or fallback directly if text wasn't wrapped
                findings_text = research_result["content"] if isinstance(research_result, dict) else research_result
                report_result = write_report(topic, findings_text, citations)

            if isinstance(report_result, dict) and report_result.get("status") == "error":
                st.error(f"⚠️ Writing Phase Blocked: {report_result['content']}")
                execution_failed = True
            else:
                final_report_text = report_result["content"] if isinstance(report_result, dict) else report_result
                
                st.subheader("Final Report")
                st.markdown(final_report_text)

                # --- STEP E: PDF FILE COMPILATION AND EXPORT ---
                try:
                    pdf = create_pdf(topic, final_report_text)
                    with open(pdf, "rb") as f:
                        st.download_button(
                            "📄 Download PDF Report",
                            f,
                            file_name="Research_Report.pdf",
                            mime="application/pdf"
                        )
                except Exception as pdf_err:
                    st.warning("⚠️ Report compiled on screen, but local PDF document creation failed.")
                    print(f"PDF compilation terminal alert: {str(pdf_err)}")

# 4. SIDEBAR LOGS AND CREDENTIAL ATTRIBUTIONS
with st.sidebar:
    st.markdown("Developed by Oluwasegun Oluwatosin (tosindataginius)")
    st.link_button("Visit my LinkedIn Profile", "https://www.linkedin.com/in/oluwatosin-oluwasegun-1a9266288/")
    st.link_button("Visit my GitHub Profile", "https://github.com/tosindataginius")
