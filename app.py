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

st.title(
    "🔬 Autonomous Research Assistant Agent"
)

topic = st.text_input(
    "Research Topic"
)

if st.button(
    "Start Research"
):

    with st.spinner(
        "Planning..."
    ):

        research_plan = plan(
            topic
        )

    st.subheader(
        "Research Plan"
    )

    st.write(
        research_plan
    )

    with st.spinner(
        "Searching..."
    ):

        sources = gather_sources(
            topic
        )

    citations = format_sources(
        sources
    )

    st.subheader(
        "Sources"
    )

    for s in sources:

        st.markdown(
            f"""
### {s["title"]}

{s["url"]}
"""
        )

    with st.spinner(
        "Researching..."
    ):

        findings = research(
            topic,
            sources
        )

    with st.spinner(
        "Writing report..."
    ):

        report = write_report(
            topic,
            findings,
            citations
        )

    st.subheader(
        "Final Report"
    )

    st.markdown(
        report
    )

    pdf = create_pdf(
        topic,
        report
    )

    with open(
        pdf,
        "rb"
    ) as f:

        st.download_button(
            "📄 Download PDF",
            f,
            file_name="Research_Report.pdf",
            mime="application/pdf"
        )

with st.sidebar:
    st.markdown("Developed by Oluwasegun Oluwatosin (tosindataginius)")
    st.link_button("Visit my LinkedIn Profile", "https://www.linkedin.com/in/oluwatosin-oluwasegun-1a9266288/")
    st.link_button("Visit my GitHub Profile", "https://github.com/tosindataginius")