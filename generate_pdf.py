import os
import sys

def install_and_import():
    try:
        import reportlab
    except ImportError:
        print("ReportLab not found, installing via pip...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        import reportlab

install_and_import()

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total pages and draw professional 
    headers, footers, and page numbers (e.g. Page X of Y) on all pages except the cover.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_elements(num_pages)
            super().showPage()
        super().save()

    def draw_page_elements(self, page_count):
        if self._pageNumber == 1:
            # Skip headers, footers, and dividers on the cover page
            return

        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#0f172a"))
        
        # Header text
        self.drawString(54, 750, "POWER AI BI ASSISTANT")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawRightString(558, 750, "Technical Report & Architecture")
        
        # Divider Line below Header
        self.setStrokeColor(colors.HexColor("#cbd5e1"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        
        # Divider Line above Footer
        self.line(54, 55, 558, 55)
        
        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        self.drawString(54, 40, "Confidential - Project Submission Report")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 40, page_text)
        self.restoreState()


def create_report(filename="Power_AI_BI_Assistant_Report.pdf"):
    # Target letter size with 0.75-inch (54 points) left/right margins, and 1-inch (72 points) top/bottom margins
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    # Custom color palette matching the web application design guidelines
    c_primary = colors.HexColor('#0ea5e9')   # Neon blue
    c_dark = colors.HexColor('#0f172a')      # Sleek slate
    c_muted = colors.HexColor('#475569')     # Gray text
    c_border = colors.HexColor('#cbd5e1')    # Light gray borders
    c_bg_code = colors.HexColor('#f8fafc')   # Code background
    
    # Custom styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=30,
        leading=36,
        textColor=c_dark,
        alignment=1, # Center
        spaceAfter=15
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=15,
        leading=20,
        textColor=c_primary,
        alignment=1, # Center
        spaceAfter=50
    )
    
    h1_style = ParagraphStyle(
        'H1_Custom',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=c_dark,
        spaceBefore=18,
        spaceAfter=10,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'H2_Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=c_muted,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=10,
        leading=14.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=8
    )
    
    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Code'],
        fontName='Courier',
        fontSize=8.5,
        leading=11.5,
        textColor=c_dark,
        backColor=c_bg_code,
        borderColor=c_border,
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=5,
        spaceAfter=8
    )
    
    story = []
    
    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 120))
    story.append(Paragraph("POWER AI BI ASSISTANT", title_style))
    story.append(Paragraph("A Premium AI-Driven Business Intelligence Platform", subtitle_style))
    story.append(Spacer(1, 80))
    
    # Metadata table block
    metadata_data = [
        [Paragraph("<b>Document Type:</b>", body_style), Paragraph("Technical & System Architecture Report", body_style)],
        [Paragraph("<b>Prepared For:</b>", body_style), Paragraph("Academic & Project Submission", body_style)],
        [Paragraph("<b>Author Account:</b>", body_style), Paragraph("hariraman-24", body_style)],
        [Paragraph("<b>GitHub Project:</b>", body_style), Paragraph("github.com/hariraman-24/ai-bi-bkups", body_style)],
        [Paragraph("<b>Current Status:</b>", body_style), Paragraph("Live & Operational", body_style)],
    ]
    
    metadata_table = Table(metadata_data, colWidths=[120, 250])
    metadata_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
    ]))
    
    # Center-align metadata table
    meta_container = Table([[metadata_table]], colWidths=[370])
    meta_container.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    story.append(meta_container)
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 2: EXECUTIVE SUMMARY
    # ----------------------------------------------------
    story.append(Paragraph("1. Executive Summary & Project Objectives", h1_style))
    story.append(Paragraph(
        "The Power AI BI Assistant is a state-of-the-art Business Intelligence application "
        "designed to make complex relational databases and corporate data files accessible via natural language. "
        "Historically, business leaders have been forced to rely on dedicated data analysts to write SQL or run spreadsheet "
        "macros to produce sales performance metrics. This application changes that paradigm by translating English "
        "questions into executable queries, mathematical models, and graphic charts on the fly.",
        body_style
    ))
    story.append(Paragraph(
        "By utilizing a Model Context Protocol (MCP) server structure and local LLM/OpenAI APIs, the assistant "
        "provides accurate analytical responses, forecasts sales trends, parses document structures (including PDFs, "
        "Excel, and CSVs), and automatically drafts human-readable explanations of SQL execution datasets. "
        "The platform contains dual user interfaces—a visual dashboard in Streamlit and a web client in React "
        "and TypeScript—catering to varied end-user preferences.",
        body_style
    ))
    
    story.append(Paragraph("Core Project Objectives:", h2_style))
    story.append(Paragraph("• <b>Natural Language Access (NLP):</b> Democratize querying by enabling standard users to ask questions like <i>'Who was the top employee in January 2025 by sales?'</i> and get instant answers.", bullet_style))
    story.append(Paragraph("• <b>Dual Frontend Delivery:</b> Offer a dark-mode Streamlit analytical page and a reactive single-page React chat application.", bullet_style))
    story.append(Paragraph("• <b>Intelligent Decision Routing:</b> Classify query intent to ensure queries for datasets, charts, or mathematical forecasting are routed to their designated specialized engine.", bullet_style))
    story.append(Paragraph("• <b>High-Fidelity Visualizations:</b> Instantly build corresponding data visualizations matching a clean corporate aesthetic.", bullet_style))
    story.append(Spacer(1, 10))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 3: TECHNICAL SYSTEM ARCHITECTURE
    # ----------------------------------------------------
    story.append(Paragraph("2. System Architecture & Technical Flow", h1_style))
    story.append(Paragraph(
        "The architecture is structured with modular backend engines exposing endpoints through an "
        "exposition layer, accessed by independent frontend clients. Below is a structural mapping of "
        "a user query's execution path:",
        body_style
    ))
    
    # Text-based flow chart
    flow_data = [
        [Paragraph("<b>Step</b>", body_style), Paragraph("<b>Component</b>", body_style), Paragraph("<b>Function & Output</b>", body_style)],
        [Paragraph("1. Request", body_style), Paragraph("Streamlit Client / React Interface", body_style), Paragraph("User types natural language query or uploads a file.", body_style)],
        [Paragraph("2. Classification", body_style), Paragraph("Intent Engine (Ollama / OpenAI fallback)", body_style), Paragraph("Parses query semantic tokens and determines if it is a general chat, database query, forecasting run, or visual chart.", body_style)],
        [Paragraph("3. Routing", body_style), Paragraph("Decision Engine (backend/decision_engine.py)", body_style), Paragraph("Dispatches execution payload to the database SQL generator, the forecasting engine, or the file server.", body_style)],
        [Paragraph("4. Synthesis", body_style), Paragraph("SQL Generator & Validator", body_style), Paragraph("Generates dialect-safe SQL (Postgres/MySQL) and validates database operations against schema rules before executing.", body_style)],
        [Paragraph("5. Insight Engine", body_style), Paragraph("Narrative Generator (backend/insight_engine.py)", body_style), Paragraph("Transforms raw data columns into natural language insights describing peaks, valleys, and summaries.", body_style)],
        [Paragraph("6. Response", body_style), Paragraph("Visualization & Charting Engine", body_style), Paragraph("Generates a clean visual plot (Matplotlib/Plotly) and displays the analytical report to the user.", body_style)]
    ]
    
    flow_table = Table(flow_data, colWidths=[80, 150, 274])
    flow_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(flow_table)
    story.append(Spacer(1, 15))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 4: BACKEND ENGINE DETAILS
    # ----------------------------------------------------
    story.append(Paragraph("3. Core Backend Engines", h1_style))
    
    story.append(Paragraph("3.1. Intent Engine & Decision Router", h2_style))
    story.append(Paragraph(
        "Implemented in <code>backend/intent_engine.py</code> and <code>backend/decision_engine.py</code>, "
        "this layer serves as the primary dispatcher. It combines lightweight keyword pattern heuristics with LLM "
        "semantic classifiers. If a query matches forecasting criteria (e.g., contains 'forecast', 'predict'), the "
        "request is routed to the forecasting module. If a chart is requested, it ensures parameters are prepared for the "
        "visualization module.",
        body_style
    ))
    
    story.append(Paragraph("3.2. SQL Generator & Query Validator", h2_style))
    story.append(Paragraph(
        "Responsible for generating robust SQL statements. The generator in <code>backend/sql_generator.py</code> "
        "references schema contexts and generates database-specific queries. Before execution, the generated query "
        "is run through <code>backend/query_validator.py</code>. The validator checks for syntax irregularities, "
        "schema matches, and prevents potentially destructive queries (e.g., <code>DROP</code>, <code>DELETE</code>, or <code>UPDATE</code> commands), "
        "acting as a security gatekeeper.",
        body_style
    ))
    
    story.append(Paragraph("3.3. Sales & Predictive Forecasting Engine", h2_style))
    story.append(Paragraph(
        "When forecasting intent is identified, the application calls <code>backend/forecasting/forecast.py</code>. "
        "This module reads historical sales volumes from the database, builds seasonal time-series models "
        "(Holt-Winters or Linear Regressions depending on dataset characteristics), and generates a predicted sequence of sales "
        "for the subsequent period, returning both statistical data points and confidence metrics.",
        body_style
    ))
    
    story.append(Paragraph("3.4. Dynamic Insight Engine", h2_style))
    story.append(Paragraph(
        "Found in <code>backend/insight_engine.py</code>, this component runs after the dataset is fetched from the database. "
        "Rather than forcing the user to interpret a raw table of data, the Insight Engine analyzes trends, detects peak sales months, "
        "highlights employees with the highest values, and summarizes key insights into a readable prose paragraphs.",
        body_style
    ))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 5: DATABASE SCHEMA & FOLDER STRUCTURE
    # ----------------------------------------------------
    story.append(Paragraph("4. Database Schema & Project Structure", h1_style))
    story.append(Paragraph(
        "The relational database schema models a typical company sales tracking environment. "
        "The script <code>database/schema.sql</code> seeds these four main tables:",
        body_style
    ))
    
    schema_data = [
        [Paragraph("<b>Table</b>", body_style), Paragraph("<b>Primary Key</b>", body_style), Paragraph("<b>Key Attributes</b>", body_style), Paragraph("<b>Description</b>", body_style)],
        [Paragraph("<b>products</b>", body_style), Paragraph("product_id", body_style), Paragraph("product_name, category, price", body_style), Paragraph("Catalog of products sold by the company.", body_style)],
        [Paragraph("<b>customers</b>", body_style), Paragraph("customer_id", body_style), Paragraph("customer_name, region", body_style), Paragraph("Demographics and locations of clients.", body_style)],
        [Paragraph("<b>employees</b>", body_style), Paragraph("employee_id", body_style), Paragraph("employee_name, department", body_style), Paragraph("Internal staff listing.", body_style)],
        [Paragraph("<b>sales</b>", body_style), Paragraph("sale_id", body_style), Paragraph("product_id, customer_id, employee_id, sales_amount, sale_date", body_style), Paragraph("Main transactions log linking all tables.", body_style)]
    ]
    
    schema_table = Table(schema_data, colWidths=[70, 80, 160, 194])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('BACKGROUND', (0,1), (-1,-1), colors.HexColor('#f8fafc')),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(schema_table)
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("Codebase Layout:", h2_style))
    
    layout_data = [
        [Paragraph("<code>backend/</code>", body_style), Paragraph("Contains core Python engines (SQL generator, forecasting, intents, database connection handlers).", body_style)],
        [Paragraph("<code>frontend/</code>", body_style), Paragraph("Contains the Streamlit web dashboard app (<code>app.py</code>) and the React/Vite single page source files.", body_style)],
        [Paragraph("<code>database/</code>", body_style), Paragraph("Contains the relational schema DDL files.", body_style)],
        [Paragraph("<code>static/</code>", body_style), Paragraph("Stores visualization outputs and mockup image files.", body_style)],
        [Paragraph("<code>visualization/</code>", body_style), Paragraph("Contains graphic plot helpers (<code>charts.py</code>).", body_style)],
    ]
    
    layout_table = Table(layout_data, colWidths=[100, 404])
    layout_table.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#f8fafc')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(layout_table)
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 6: FRONT-ENDS & SCREENSHOT
    # ----------------------------------------------------
    story.append(Paragraph("5. Client Interfaces & UI Design", h1_style))
    story.append(Paragraph(
        "The Power AI BI platform delivers dual user experiences, catering to both structured analytics "
        "and fluid conversation patterns.",
        body_style
    ))
    
    story.append(Paragraph("5.1. Streamlit Executive Dashboard", h2_style))
    story.append(Paragraph(
        "Implemented in <code>frontend/app.py</code>, the Streamlit app delivers an executive-level summary page. "
        "It features styled dark-slate gradients, interactive database connector modals, quick-click metric KPI cards "
        "that translate sales queries into visual KPIs, and full file-upload integrations. The interface is optimized "
        "to automatically adjust layouts depending on screens.",
        body_style
    ))
    
    # Embed the mockup image
    mockup_path = "static/dashboard_mockup.png"
    if os.path.exists(mockup_path):
        story.append(Spacer(1, 5))
        try:
            # We scale the image to fit beautifully on the page: width = 432 pt (6 inches), height = 259.2 pt (3.6 inches)
            img = Image(mockup_path, width=432, height=259.2)
            img.hAlign = 'CENTER'
            story.append(img)
            story.append(Paragraph("<font color='#64748b'><i>Figure 1: Generated mockup representing the dark-mode BI system dashboard interface.</i></font>", ParagraphStyle('Caption', parent=body_style, alignment=1, fontSize=8, textColor=c_muted)))
        except Exception as e:
            story.append(Paragraph(f"<i>[Image failed to render: {str(e)}]</i>", body_style))
        story.append(Spacer(1, 10))
    else:
        story.append(Paragraph("<i>[Dashboard UI Mockup not found at static/dashboard_mockup.png]</i>", body_style))
        
    story.append(Paragraph("5.2. React + TypeScript Web App", h2_style))
    story.append(Paragraph(
        "For a responsive, standalone chat client, the codebase holds a full Single Page Application in "
        "<code>frontend/src/</code>. It connects to the backend endpoints, offering a modern, clean sidebar workspace, "
        "chat timelines, and custom message components that display formatted charts and tables.",
        body_style
    ))
    story.append(PageBreak())
    
    # ----------------------------------------------------
    # PAGE 7: DEPLOYMENT AND VERIFICATION
    # ----------------------------------------------------
    story.append(Paragraph("6. Setup, Run & Verification Guide", h1_style))
    story.append(Paragraph(
        "Follow these steps to run the application components locally in your development workspace.",
        body_style
    ))
    
    story.append(Paragraph("Step 1: Relational Database Initialization", h2_style))
    story.append(Paragraph(
        "Import the schema DDL inside your local database client. For example, in MySQL:",
        body_style
    ))
    story.append(Paragraph(
        "mysql -u root -p < database/schema.sql",
        code_style
    ))
    
    story.append(Paragraph("Step 2: Initialize the Backend & Streamlit App", h2_style))
    story.append(Paragraph(
        "Create a virtual environment and run the dashboard directly:",
        body_style
    ))
    story.append(Paragraph(
        "# Create venv\n"
        "python -m venv venv\n\n"
        "# Activate venv (Windows)\n"
        "venv\\Scripts\\activate\n\n"
        "# Install dependencies\n"
        "pip install -r backend/requirements.txt\n\n"
        "# Start Streamlit app\n"
        "streamlit run frontend/app.py",
        code_style
    ))
    
    story.append(Paragraph("Step 3: Run the React Web App Client", h2_style))
    story.append(Paragraph(
        "Start the frontend development server using Node.js npm utilities:",
        body_style
    ))
    story.append(Paragraph(
        "cd frontend\n"
        "npm install\n"
        "npm run dev",
        code_style
    ))
    
    story.append(Spacer(1, 10))
    story.append(Paragraph("Conclusion", h2_style))
    story.append(Paragraph(
        "The Power AI BI Assistant succeeds in wrapping advanced analytical processes in an intuitive interface. "
        "Users can execute secure queries, observe trends, generate automated summaries, and download reports "
        "interactively. All code has been pushed and verified on the GitHub master repository at "
        "<code>github.com/hariraman-24/ai-bi-bkups</code>.",
        body_style
    ))
    
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully saved as {filename}")

if __name__ == "__main__":
    create_report()
