from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

from reportlab.lib.units import inch


def create_pdf(title, content):
    path = "research_report.pdf"
    doc = SimpleDocTemplate(path)

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(title, styles["Title"])
    )

    story.append(Spacer(1,0.3 * inch))

    for line in content.split("\n"):

        story.append(Paragraph(line, styles["BodyText"])
        )

    doc.build(story)

    return path


# Script to test the create_pdf function independently
if __name__ == "__main__":
    test_title = "The Future of Renewable Energy"
    test_content = """Renewable energy is expected to grow significantly in the coming decades. 
    Key drivers include technological advancements, policy support, and increasing environmental concerns."""
    
    pdf_path = create_pdf(test_title, test_content)
    print(f"PDF generated at: {pdf_path}")