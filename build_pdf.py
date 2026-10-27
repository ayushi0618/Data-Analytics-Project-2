"""
Build Olist Project Document PDF (Olist_Ecommerce_Project_Document.pdf)
========================================================================
Author: Ayushi Singh, Data Analyst
Generates a comprehensive, diagram-led executive project document using ReportLab.
Follows all section ordering, KPI totals, and chart embedding rules.
"""

import os
import json
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_DIR = os.path.join(BASE_DIR, "data", "clean")
CHARTS_DIR = os.path.join(BASE_DIR, "charts")
PDF_PATH = os.path.join(BASE_DIR, "Olist_Ecommerce_Project_Document.pdf")

# Palette
NAVY = colors.HexColor("#0F2040")
SLATE = colors.HexColor("#1E40AF")
CHARCOAL = colors.HexColor("#1E293B")
MUTED = colors.HexColor("#64748B")
LIGHT_BG = colors.HexColor("#F8FAFC")
CARD_BG = colors.HexColor("#F1F5F9")
BORDER_COLOR = colors.HexColor("#CBD5E1")
CORAL = colors.HexColor("#E11D48")
GREEN = colors.HexColor("#059669")


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and print total page count and running header/footer."""
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
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(MUTED)

        # Header
        self.drawString(54, letter[1] - 36, "Olist Brazilian E-Commerce Analytics | Executive Project Document")
        self.drawRightString(letter[0] - 54, letter[1] - 36, "Ayushi Singh, Data Analyst")
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer
        self.line(54, 46, letter[0] - 54, 46)
        self.drawString(54, 32, "Source: Kaggle (olistbr/brazilian-ecommerce, CC BY-NC-SA 4.0) — Delivered Orders Scope")
        self.drawRightString(letter[0] - 54, 32, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        PDF_PATH,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        "CoverTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=24,
        leading=28,
        textColor=NAVY,
        alignment=0,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=16,
        textColor=SLATE,
        spaceAfter=18
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=18,
        textColor=NAVY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=15,
        textColor=SLATE,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=13.5,
        textColor=CHARCOAL,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        "Body_Bold",
        parent=body_style,
        fontName="Helvetica-Bold"
    )

    caption_style = ParagraphStyle(
        "Caption_Custom",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=11,
        textColor=MUTED,
        alignment=1,
        spaceBefore=4,
        spaceAfter=8
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8.5,
        leading=10,
        textColor=colors.white,
        alignment=1
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
        textColor=CHARCOAL,
        alignment=0
    )

    table_cell_right = ParagraphStyle(
        "TableCellRight",
        parent=table_cell_style,
        alignment=2
    )

    table_cell_center = ParagraphStyle(
        "TableCellCenter",
        parent=table_cell_style,
        alignment=1
    )

    story = []

    # ----------------------------------------------------
    # COVER PAGE
    # ----------------------------------------------------
    story.append(Spacer(1, 15))
    story.append(Paragraph("OLIST BRAZILIAN E-COMMERCE ANALYTICS", title_style))
    story.append(Paragraph("Comprehensive Operational, Customer Segmentation & Logistics Performance Report", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=NAVY, spaceBefore=0, spaceAfter=15))

    # Metadata Block
    meta_data = [
        [Paragraph("<b>Prepared By:</b>", body_style), Paragraph("Ayushi Singh, Data Analyst", body_style)],
        [Paragraph("<b>Publication Date:</b>", body_style), Paragraph("October 2026", body_style)],
        [Paragraph("<b>Data Source:</b>", body_style), Paragraph("Kaggle: olistbr/brazilian-ecommerce (CC BY-NC-SA 4.0)", body_style)],
        [Paragraph("<b>Public Mirror:</b>", body_style), Paragraph("https://github.com/olist/work-at-olist-data", body_style)],
        [Paragraph("<b>Analytical Tools:</b>", body_style), Paragraph("Python 3.12 (Pandas, NumPy, Matplotlib), OpenPyXL, Streamlit, Power BI Pack, Google Cloud BigQuery", body_style)],
        [Paragraph("<b>Scope Rule:</b>", body_style), Paragraph("<b>Strictly Delivered Orders Only</b> (96,478 orders). Shipped/Cancelled/Unavailable orders excluded from GMV.", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[110, 394])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BG),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 18))

    # KPI Summary Cards (4 Cards)
    story.append(Paragraph("<b>HEADLINE VERIFIED PERFORMANCE INDICATORS</b>", h2_style))
    kpi_cards = [
        [
            Paragraph("<b>DELIVERED GMV</b><br/><font size='14' color='#0F2040'><b>R$ 13,221,498.11</b></font><br/><font size='7.5' color='#64748B'>Delivered Orders Only</font>", table_cell_center),
            Paragraph("<b>DELIVERED ORDERS</b><br/><font size='14' color='#0F2040'><b>96,478</b></font><br/><font size='7.5' color='#64748B'>AOV: R$ 137.04</font>", table_cell_center),
            Paragraph("<b>AVG REVIEW SCORE</b><br/><font size='14' color='#0F2040'><b>4.16 / 5.00</b></font><br/><font size='7.5' color='#64748B'>58.6% 5-Star Reviews</font>", table_cell_center),
            Paragraph("<b>LATE DELIVERY RATE</b><br/><font size='14' color='#E11D48'><b>8.11%</b></font><br/><font size='7.5' color='#64748B'>Avg: 12.56d | Med: 10.22d</font>", table_cell_center)
        ]
    ]
    kpi_table = Table(kpi_cards, colWidths=[126, 126, 126, 126])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CARD_BG),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 1, colors.white),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 15))

    # Executive Abstract on Cover
    exec_text = (
        "<b>Executive Summary:</b> This study presents an exhaustive, end-to-end analytical assessment of the Brazilian "
        "e-commerce marketplace Olist, encompassing 99,441 raw orders recorded between September 2016 and October 2018. "
        "Adhering to strict enterprise revenue recognition principles, revenue analysis is confined solely to successfully "
        "<b>delivered orders</b> (96,478 orders across 93,358 unique customers), generating a cumulative GMV of "
        "<b>R$ 13,221,498.11</b> with an Average Order Value (AOV) of <b>R$ 137.04</b>.<br/><br/>"
        "Two empirical findings dominate the findings: (1) <b>Delivery lateness directly suppresses review satisfaction</b>, "
        "with on-time deliveries averaging 4.30 stars compared to just 2.57 stars for late deliveries, dropping to 2.25 stars for "
        "orders exceeding 30 days; and (2) <b>Customer retention is severely constrained</b>, with only 3.0% of customers placing a "
        "subsequent order, resulting in an empty 'Champions' RFM segment. This document outlines the empirical findings, "
        "data cleaning logs, star schema, cohort behavior, and five actionable commercial recommendations."
    )
    story.append(Paragraph(exec_text, body_style))
    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 1 — BUSINESS QUESTIONS
    # ----------------------------------------------------
    story.append(Paragraph("1. Business Questions", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))
    
    sec1_text = (
        "To provide actionable operational intelligence for marketplace leadership, this analysis addresses six fundamental business questions:<br/>"
        "• <b>Q1 (Revenue Trajectory):</b> What is the historical growth trajectory of delivered GMV and order volume, and what seasonal peaks or operational gaps occurred?<br/>"
        "• <b>Q2 (Category Concentration):</b> Which product categories drive the highest sales volume and gross revenue, and how concentrated is GMV among top performers?<br/>"
        "• <b>Q3 (Geographic Concentration & Inequity):</b> Where are buyers located geographically, and how do delivery fulfillment speed and delivery delay rates differ across Brazilian states?<br/>"
        "• <b>Q4 (Logistics Impact on Customer Satisfaction):</b> Does actual delivery duration correlate with customer review scores, and what is the quantitative satisfaction penalty of late deliveries?<br/>"
        "• <b>Q5 (Customer Loyalty & Repeat Behavior):</b> Do customers return to make repeat purchases on Olist, and what does RFM segmentation reveal about customer lifetime behavior?<br/>"
        "• <b>Q6 (Payment Dynamics & Financing):</b> How do Brazilian consumers finance marketplace transactions across payment methods, and what role do installment plans play?"
    )
    story.append(Paragraph(sec1_text, body_style))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 2 — DATA AND CLEANING
    # ----------------------------------------------------
    story.append(Paragraph("2. Data and Cleaning", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))

    sec2_scope = (
        "<b>2.1 Scope Rules and Financial Reconciliation:</b><br/>"
        "A critical pitfall in e-commerce analytics is aggregating non-delivered statuses into revenue. In this model, "
        "<b>GMV is strictly defined as the sum of item prices for delivered orders</b>. Freight is reported separately as an operational fee "
        "(Delivered Freight = R$ 2,202,965.54) and is never conflated with merchandise GMV. Customer payment receipts total "
        "R$ 15,422,461.77. The exact reconciliation discrepancy across the entire dataset is <b>R$ 2,001.88</b>, arising from voucher "
        "subsidies, minor payment split rounding, and partial payment authorizations."
    )
    story.append(Paragraph(sec2_scope, body_style))
    story.append(Spacer(1, 6))

    # Reconciliation Table
    recon_headers = [Paragraph("<b>Metric</b>", table_header_style), Paragraph("<b>Scope / Formula</b>", table_header_style), Paragraph("<b>Verified Value (R$)</b>", table_header_style)]
    recon_rows = [
        recon_headers,
        [Paragraph("Delivered GMV", table_cell_style), Paragraph("SUM(price) for delivered orders", table_cell_style), Paragraph("R$ 13,221,498.11", table_cell_right)],
        [Paragraph("Delivered Freight", table_cell_style), Paragraph("SUM(freight_value) for delivered orders", table_cell_style), Paragraph("R$ 2,202,965.54", table_cell_right)],
        [Paragraph("Delivered Payments", table_cell_style), Paragraph("SUM(payment_value) for delivered orders", table_cell_style), Paragraph("R$ 15,422,461.77", table_cell_right)],
        [Paragraph("Reconciliation Discrepancy", table_cell_style), Paragraph("GMV + Freight - Payments", table_cell_style), Paragraph("R$ 2,001.88", table_cell_right)],
        [Paragraph("Delivered Orders Count", table_cell_style), Paragraph("COUNT(order_id) WHERE status='delivered'", table_cell_style), Paragraph("96,478", table_cell_right)],
        [Paragraph("Unique Delivered Customers", table_cell_style), Paragraph("COUNT(DISTINCT customer_unique_id)", table_cell_style), Paragraph("93,358", table_cell_right)]
    ]
    t_recon = Table(recon_rows, colWidths=[140, 220, 144])
    t_recon.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_recon)
    story.append(Spacer(1, 10))

    # Cleaning Log Table
    story.append(Paragraph("<b>2.2 Cleaning Decisions and Transformation Log:</b>", h2_style))
    
    clean_log_headers = [
        Paragraph("<b>Transformation Step</b>", table_header_style),
        Paragraph("<b>Rule & Rationale</b>", table_header_style),
        Paragraph("<b>Before</b>", table_header_style),
        Paragraph("<b>After</b>", table_header_style),
        Paragraph("<b>Dropped</b>", table_header_style)
    ]
    clean_log_rows = [
        clean_log_headers,
        [Paragraph("Order Status Filter", table_cell_style), Paragraph("Confine GMV to delivered status only", table_cell_style), Paragraph("99,441", table_cell_center), Paragraph("96,478", table_cell_center), Paragraph("2,963", table_cell_center)],
        [Paragraph("Review Dedup Pt. 1", table_cell_style), Paragraph("Drop duplicate review_id records", table_cell_style), Paragraph("99,224", table_cell_center), Paragraph("98,410", table_cell_center), Paragraph("814", table_cell_center)],
        [Paragraph("Review Dedup Pt. 2", table_cell_style), Paragraph("Keep first review per order for multi-reviews", table_cell_style), Paragraph("98,410", table_cell_center), Paragraph("98,167", table_cell_center), Paragraph("243", table_cell_center)],
        [Paragraph("Category Translation", table_cell_style), Paragraph("Translate PT to EN; unmapped to 'Unknown'", table_cell_style), Paragraph("32,951", table_cell_center), Paragraph("32,951", table_cell_center), Paragraph("623 unk", table_cell_center)],
        [Paragraph("Missing Dates Policy", table_cell_style), Paragraph("Preserve 2,965 delivery & 160 approval dates as null", table_cell_style), Paragraph("99,441", table_cell_center), Paragraph("99,441", table_cell_center), Paragraph("0 (kept)", table_cell_center)],
        [Paragraph("Geolocation Removal", table_cell_style), Paragraph("Exclude 1M rows; state/city already in customer", table_cell_style), Paragraph("1,000,163", table_cell_center), Paragraph("0", table_cell_center), Paragraph("1,000,163", table_cell_center)],
        [Paragraph("Customer Identity", table_cell_style), Paragraph("Use customer_unique_id (never customer_id)", table_cell_style), Paragraph("99,441", table_cell_center), Paragraph("93,358", table_cell_center), Paragraph("N/A", table_cell_center)]
    ]
    t_clean = Table(clean_log_rows, colWidths=[105, 189, 70, 70, 70])
    t_clean.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_clean)
    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 3 — EXECUTIVE OVERVIEW
    # ----------------------------------------------------
    story.append(Paragraph("3. Executive Overview", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))

    sec3_text = (
        "Between September 2016 and August 2018, Olist experienced rapid sales expansion, scaling from 265 delivered orders "
        "in October 2016 to over 6,300 monthly delivered orders by August 2018. Two major anomalies must be noted: (1) November 2016 "
        "had zero orders due to a known raw data capture hiatus; and (2) September–October 2018 shows zero delivered orders because "
        "the Kaggle extract cutoff prevented tracking orders that had not yet reached delivery completion.<br/>"
        "Gross sales reached an all-time peak in <b>November 2017 during Black Friday</b>, achieving <b>R$ 987,765.37 across 7,289 orders</b>."
    )
    story.append(Paragraph(sec3_text, body_style))
    story.append(Spacer(1, 6))

    # Embed Monthly GMV Chart
    monthly_chart_path = os.path.join(CHARTS_DIR, "monthly_gmv.png")
    if os.path.exists(monthly_chart_path):
        story.append(Image(monthly_chart_path, width=6.8*inch, height=3.4*inch))
        story.append(Paragraph("Figure 1: Monthly Delivered GMV (BRL) from Sep 2016 to Aug 2018 with Black Friday peak annotation.", caption_style))

    story.append(Spacer(1, 8))

    # Category and State Breakdown
    story.append(Paragraph("<b>3.1 Product Category & Geographic Drivers:</b>", h2_style))
    cat_text = (
        "Product demand is led by <b>health_beauty</b> with <b>R$ 1,233,132</b> in delivered GMV (8,836 items), followed by "
        "<b>watches_gifts</b> (R$ 1,166,936) and <b>bed_bath_table</b> (R$ 1,029,915). Geographically, the state of <b>São Paulo (SP)</b> "
        "dominates marketplace commerce, generating <b>R$ 5,067,633</b> (38.3% of national GMV) across 40,494 orders. Rio de Janeiro (RJ) "
        "is second at R$ 1,757,984 (13.3%), and Minas Gerais (MG) is third at R$ 1,547,404 (11.7%)."
    )
    story.append(Paragraph(cat_text, body_style))
    story.append(Spacer(1, 6))

    # Embed Top Categories & Top States Charts side-by-side or stacked
    top_cat_path = os.path.join(CHARTS_DIR, "top_categories.png")
    if os.path.exists(top_cat_path):
        story.append(Image(top_cat_path, width=6.8*inch, height=3.3*inch))
        story.append(Paragraph("Figure 2: Top 10 Product Categories by Delivered GMV.", caption_style))

    story.append(PageBreak())

    top_state_path = os.path.join(CHARTS_DIR, "top_states.png")
    if os.path.exists(top_state_path):
        story.append(Image(top_state_path, width=6.8*inch, height=3.3*inch))
        story.append(Paragraph("Figure 3: Top 10 Brazilian States by Customer Delivered GMV with state late rates annotated.", caption_style))

    story.append(Spacer(1, 8))

    # Payment Methods Table
    story.append(Paragraph("<b>3.2 Payment Methods & Financing Behavior:</b>", h2_style))
    pay_text = (
        "Brazilian consumers heavily utilize credit card financing. <b>Credit cards account for R$ 12,101,095 (78.5% of total payments)</b>, "
        "with an average of <b>3.50 installments</b> per transaction. Cash-based bank slips (<b>Boleto Bancário</b>) represent the second-largest "
        "payment mode at <b>R$ 2,769,933 (18.0%)</b>, followed by vouchers (R$ 343,013) and debit cards (R$ 208,421)."
    )
    story.append(Paragraph(pay_text, body_style))
    story.append(Spacer(1, 6))

    pay_headers = [
        Paragraph("<b>Payment Type</b>", table_header_style),
        Paragraph("<b>Total Value (R$)</b>", table_header_style),
        Paragraph("<b>Share of Total (%)</b>", table_header_style),
        Paragraph("<b>Avg Installments</b>", table_header_style),
        Paragraph("<b>Transactions Count</b>", table_header_style)
    ]
    pay_rows = [
        pay_headers,
        [Paragraph("Credit Card", table_cell_style), Paragraph("R$ 12,101,094.88", table_cell_right), Paragraph("78.46%", table_cell_center), Paragraph("3.50", table_cell_center), Paragraph("74,586", table_cell_right)],
        [Paragraph("Boleto (Bank Slip)", table_cell_style), Paragraph("R$ 2,769,932.58", table_cell_right), Paragraph("17.96%", table_cell_center), Paragraph("1.00", table_cell_center), Paragraph("19,191", table_cell_right)],
        [Paragraph("Voucher", table_cell_style), Paragraph("R$ 343,013.19", table_cell_right), Paragraph("2.22%", table_cell_center), Paragraph("1.00", table_cell_center), Paragraph("5,493", table_cell_right)],
        [Paragraph("Debit Card", table_cell_style), Paragraph("R$ 208,421.12", table_cell_right), Paragraph("1.35%", table_cell_center), Paragraph("1.00", table_cell_center), Paragraph("1,486", table_cell_right)],
        [Paragraph("<b>Total Delivered Payments</b>", table_cell_style), Paragraph("<b>R$ 15,422,461.77</b>", table_cell_right), Paragraph("<b>100.00%</b>", table_cell_center), Paragraph("<b>2.85</b>", table_cell_center), Paragraph("<b>100,756</b>", table_cell_right)]
    ]
    t_pay = Table(pay_rows, colWidths=[130, 110, 84, 85, 95])
    t_pay.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, LIGHT_BG]),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_pay)
    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 4 — DELIVERY AND SATISFACTION
    # ----------------------------------------------------
    story.append(Paragraph("4. Delivery Performance and Customer Satisfaction", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))

    sec4_text = (
        "<b>4.1 The Empirical Link Between Transit Time and Review Ratings:</b><br/>"
        "Across 96,478 delivered orders, the national <b>average delivery time is 12.56 days</b> (median: 10.22 days), and the <b>national "
        "late rate is 8.11%</b>. The relationship between delivery speed and customer ratings is statistically striking:<br/>"
        "• Orders delivered within <b>0–5 days</b> average an exceptional <b>4.45 / 5.00 review score</b>, with <b>69.4% receiving 5-star ratings</b>.<br/>"
        "• As transit time extends, satisfaction degrades monotonically: 6–10 days (4.36★), 11–15 days (4.27★), 16–20 days (4.13★), and 21–30 days (3.69★).<br/>"
        "• Orders taking <b>30+ days collapse to an average score of 2.25 / 5.00</b>, with <b>only 15.9% receiving 5 stars</b>.<br/>"
        "Furthermore, comparing overall on-time versus late orders reveals a massive <b>1.73 rating point gap</b>: on-time orders average "
        "<b>4.30 stars</b> while orders arriving past their estimated delivery date average just <b>2.57 stars</b>."
    )
    story.append(Paragraph(sec4_text, body_style))
    story.append(Spacer(1, 6))

    deliv_chart_path = os.path.join(CHARTS_DIR, "delivery_review.png")
    if os.path.exists(deliv_chart_path):
        story.append(Image(deliv_chart_path, width=6.8*inch, height=3.3*inch))
        story.append(Paragraph("Figure 4: Average Review Score and 5-Star Share by Actual Delivery Duration Bucket.", caption_style))

    story.append(Spacer(1, 8))

    # Delivery Buckets Table
    deliv_headers = [
        Paragraph("<b>Delivery Bucket</b>", table_header_style),
        Paragraph("<b>Delivered Orders</b>", table_header_style),
        Paragraph("<b>Share of Orders (%)</b>", table_header_style),
        Paragraph("<b>Avg Review Score</b>", table_header_style),
        Paragraph("<b>5-Star Share (%)</b>", table_header_style)
    ]
    deliv_rows = [
        deliv_headers,
        [Paragraph("0–5 days", table_cell_center), Paragraph("13,430", table_cell_right), Paragraph("13.92%", table_cell_center), Paragraph("4.45", table_cell_center), Paragraph("69.4%", table_cell_center)],
        [Paragraph("6–10 days", table_cell_center), Paragraph("33,050", table_cell_right), Paragraph("34.26%", table_cell_center), Paragraph("4.36", table_cell_center), Paragraph("65.2%", table_cell_center)],
        [Paragraph("11–15 days", table_cell_center), Paragraph("23,613", table_cell_right), Paragraph("24.48%", table_cell_center), Paragraph("4.27", table_cell_center), Paragraph("60.7%", table_cell_center)],
        [Paragraph("16–20 days", table_cell_center), Paragraph("12,154", table_cell_right), Paragraph("12.60%", table_cell_center), Paragraph("4.13", table_cell_center), Paragraph("54.7%", table_cell_center)],
        [Paragraph("21–30 days", table_cell_center), Paragraph("9,673", table_cell_right), Paragraph("10.03%", table_cell_center), Paragraph("3.69", table_cell_center), Paragraph("42.4%", table_cell_center)],
        [Paragraph("30+ days", table_cell_center), Paragraph("4,550", table_cell_right), Paragraph("4.72%", table_cell_center), Paragraph("2.25", table_cell_center), Paragraph("15.9%", table_cell_center)],
    ]
    t_deliv = Table(deliv_rows, colWidths=[90, 104, 100, 105, 105])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_deliv)
    story.append(Spacer(1, 10))

    # Regional Inequity in Delivery
    story.append(Paragraph("<b>4.2 Geographic Disparities in Fulfillment Lateness:</b>", h2_style))
    geo_late_text = (
        "Lateness is highly uneven across Brazilian states due to postal routing infrastructure centered around the Southeast:<br/>"
        "• <b>São Paulo (SP):</b> Boasts the lowest late delivery rate among major states at <b>5.9%</b> (average delivery: 8.7 days).<br/>"
        "• <b>Rio de Janeiro (RJ):</b> Suffers from acute urban logistics bottlenecks, resulting in a <b>13.5% late rate</b> (average: 15.0 days).<br/>"
        "• <b>Bahia (BA):</b> Experiences severe interstate long-haul delays, reaching a <b>14.0% late rate</b> (average: 15.7 days).<br/>"
        "• <b>Ceará (CE):</b> Exhibits the highest delay rate among high-volume destination states at <b>15.3% late</b> (average: 20.8 days).<br/>"
        "This geographic divide explains much of the regional variance in customer review scores."
    )
    story.append(Paragraph(geo_late_text, body_style))
    story.append(PageBreak())

    # Review Distribution Chart
    story.append(Paragraph("<b>4.3 Review Score Distribution:</b>", h2_style))
    rev_chart_path = os.path.join(CHARTS_DIR, "review_dist.png")
    if os.path.exists(rev_chart_path):
        story.append(Image(rev_chart_path, width=6.2*inch, height=3.2*inch))
        story.append(Paragraph("Figure 5: Delivered Orders Review Score Distribution (58.6% of delivered orders rated 5 stars).", caption_style))

    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 5 — CUSTOMERS: RFM AND COHORTS
    # ----------------------------------------------------
    story.append(Paragraph("5. Customers: RFM and Cohorts", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))

    sec5_text = (
        "<b>5.1 The Repeat Purchase Gap and Empty Champions Segment:</b><br/>"
        "Customer analysis is evaluated on <b>customer_unique_id</b> (representing distinct individuals) rather than order-level customer_id. "
        "Across 93,358 unique delivered customers, an overwhelming <b>97.0% (90,557 buyers) purchased exactly once</b>. Only <b>3.0% (2,801 customers) "
        "ever made a repeat purchase</b> on the platform.<br/><br/>"
        "Under standard enterprise RFM scoring (Recency 1–5, Frequency 1–5, Monetary 1–5; Score = R+F+M, range 3–15):<br/>"
        "• <b>Champions (Score >= 13):</b> Exactly <b>0 customers (Empty)</b>. Because 97.0% of buyers purchased once, the frequency quintile collapses to 1, "
        "meaning the absolute maximum attainable score is 5 (R) + 1 (F) + 5 (M) = 11. No customer can reach 13 points without invented data.<br/>"
        "• <b>Loyal Customers (Score >= 11):</b> Comprises <b>3,699 customers</b> who achieved top recency and monetary quintiles, generating "
        "<b>R$ 1,513,441.00</b> with an average spend of <b>R$ 409.15</b>.<br/>"
        "• <b>Recent / Potential (R >= 4):</b> 33,734 customers, R$ 3,896,175.16 GMV (Avg spend: R$ 115.50).<br/>"
        "• <b>Regular (R = 3):</b> 18,709 customers, R$ 2,508,084.26 GMV (Avg spend: R$ 134.06).<br/>"
        "• <b>Lost / Hibernating (R <= 2):</b> 37,216 customers, R$ 5,303,797.69 GMV (Avg spend: R$ 142.51)."
    )
    story.append(Paragraph(sec5_text, body_style))
    story.append(Spacer(1, 6))

    rfm_chart_path = os.path.join(CHARTS_DIR, "rfm_gmv.png")
    if os.path.exists(rfm_chart_path):
        story.append(Image(rfm_chart_path, width=6.5*inch, height=3.1*inch))
        story.append(Paragraph("Figure 6: Delivered GMV by RFM Segment (Champions segment is verified empty).", caption_style))

    story.append(PageBreak())

    # Cohort Retention Matrix
    story.append(Paragraph("<b>5.2 Cohort Retention Matrix Analysis:</b>", h2_style))
    cohort_text = (
        "Tracking monthly buyer cohorts from Month 0 (acquisition) through Month 20 confirms the platform's one-and-done nature. "
        "Subsequent-month retention rates uniformly hover below <b>0.5%</b> across all cohorts.<br/>"
        "<b>Critical Statistical Caveat:</b> September 2016 (n=1 customer) and December 2016 (n=1 customer) are single-customer cohorts "
        "resulting from beta platform testing and must <b>NOT</b> be interpreted as 100% or 0% retention rates. Full commercial cohort "
        "tracking effectively commenced in January 2017."
    )
    story.append(Paragraph(cohort_text, body_style))
    story.append(Spacer(1, 6))

    cohort_chart_path = os.path.join(CHARTS_DIR, "cohort_heatmap.png")
    if os.path.exists(cohort_chart_path):
        story.append(Image(cohort_chart_path, width=6.8*inch, height=4.2*inch))
        story.append(Paragraph("Figure 7: Customer Cohort Retention Rate (%) Across Acquisition Months (Sep 2016 – Aug 2018).", caption_style))

    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # SECTION 6 — INSIGHTS AND RECOMMENDED ACTIONS
    # ----------------------------------------------------
    story.append(Paragraph("6. Insights and Recommended Commercial Actions", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))

    recs = [
        ("Action 1: Target Regional Freight Inequity to Recover 1.73 Rating Points",
         "The data proves that late orders incur a 1.73-star penalty (2.57 vs 4.30). Furthermore, destination states like Rio de Janeiro (13.5% late) and Bahia (14.0% late) suffer double the delay rate of São Paulo (5.9%). Olist should contract localized fulfillment hubs and partner with regional micro-carriers in Rio de Janeiro and Salvador to compress transit times below 10 days, directly protecting merchant ratings."),
        
        ("Action 2: Institute a Post-Purchase Retention Engine to Address the 97% Churn",
         "With only 3.0% of buyers repeating (2,801 customers), customer acquisition is largely wasted on single transactions. Olist must institute automated post-delivery engagement triggered within 14 days of successful delivery (e.g. bounce-back vouchers, category replenishment reminders), targeting the 33,734 'Recent/Potential' customers before they lapse into 'Lost/Hibernating'."),
        
        ("Action 3: Premium Fulfillment SLAs for High-Ticket Categories",
         "Health & Beauty (R$ 1.23M GMV) and Watches & Gifts (R$ 1.17M GMV) represent over 18% of platform GMV with elevated average order values. Implementing certified seller fulfillment and guaranteed 3-day express shipping for these top categories will protect the highest-margin transaction volume from shipping-induced churn."),
        
        ("Action 4: Expand Low-Installment Financing and Streamline Boleto Friction",
         "Credit card transactions generate 78.5% of GMV (R$ 12.10M) with an average of 3.50 installments, indicating that installment flexibility is essential to conversion. Conversely, Boleto bank slips represent 18.0% of revenue (R$ 2.77M) but require 1–3 business days for payment confirmation. Introducing instant Pix payments (which launched post-2018 in Brazil) would eliminate Boleto confirmation delays and reduce order cancellation rates."),
        
        ("Action 5: Proactive Delay Alerting and SLA Buffer Adjustments for Distant Geographies",
         "Deliveries taking 21–30 days average 3.69 stars, dropping to 2.25 stars past 30 days. However, customer dissatisfaction is intensified when orders exceed the estimated delivery date. Olist should recalibrate delivery estimation algorithms for Northern/Northeastern states (e.g. adding 3–5 day realistic buffers for Ceará and Bahia) while dispatching proactive in-transit apology notifications and credit vouchers as soon as a carrier scan is missed.")
    ]

    for title, desc in recs:
        story.append(Paragraph(f"• <b>{title}</b>", body_bold))
        story.append(Paragraph(desc, body_style))
        story.append(Spacer(1, 3))

    story.append(PageBreak())

    # ----------------------------------------------------
    # SECTION 7 — LIMITATIONS
    # ----------------------------------------------------
    story.append(Paragraph("7. Project and Data Limitations", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=8))

    limits_text = (
        "To preserve intellectual and empirical integrity, the following limitations must be formally recognized:<br/>"
        "1. <b>Association is Not Causation:</b> Delivery duration and customer review scores move together strongly (0–5d = 4.45★ vs 30d+ = 2.25★). However, this association does not prove that transit speed alone caused low ratings; product defects, misleading merchant descriptions, or carrier package damage frequently co-occur with shipping delays.<br/>"
        "2. <b>Window-Bounded Repeat Purchase Measurement:</b> The observation that 97.0% of customers purchased only once applies strictly to the 2016–2018 dataset window. Customers who purchased near the August 2018 cutoff had limited opportunity to reorder before data extraction ceased.<br/>"
        "3. <b>Absence of Financial Cost, Marketing Spend, and Profit Data:</b> The dataset contains item gross prices and freight fees, but zero data regarding seller cost of goods sold (COGS), platform commissions, merchant acquisition costs, or customer acquisition costs (CAC). Therefore, <b>CAC, LTV:CAC ratios, operating margins, and net profit are mathematically non-computable</b> from this dataset and have been intentionally excluded.<br/>"
        "4. <b>Unknown Product Categories:</b> Exactly 623 product items (610 lacking Portuguese category metadata and 13 lacking English translations) are categorized as 'Unknown'. They have been retained without synthetic imputation.<br/>"
        "5. <b>Historical Snapshot Status:</b> Delivered order records terminate in August 2018. This is a static historical analysis with interactive parameters, not a live or real-time sales feed.<br/>"
        "6. <b>Power BI Artifact Scope:</b> Power BI Desktop is a Windows GUI application that cannot be programmatically generated as a native .pbix file. All necessary Power Query M scripts, DAX measures, and page-by-page build instructions are provided in the accompanying Power BI pack."
    )
    story.append(Paragraph(limits_text, body_style))
    story.append(Spacer(1, 10))

    # ----------------------------------------------------
    # APPENDIX A & B
    # ----------------------------------------------------
    story.append(Paragraph("Appendix A: Key Performance Indicator (KPI) Dictionary", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=6))

    dict_headers = [Paragraph("<b>KPI Name</b>", table_header_style), Paragraph("<b>Mathematical Definition</b>", table_header_style), Paragraph("<b>Scope / Rules</b>", table_header_style)]
    dict_rows = [
        dict_headers,
        [Paragraph("Delivered GMV", table_cell_style), Paragraph("SUM(price) across all delivered order items", table_cell_style), Paragraph("Delivered orders only (R$ 13,221,498.11)", table_cell_style)],
        [Paragraph("Delivered Freight", table_cell_style), Paragraph("SUM(freight_value) across delivered items", table_cell_style), Paragraph("Reported separately (R$ 2,202,965.54)", table_cell_style)],
        [Paragraph("AOV", table_cell_style), Paragraph("Delivered GMV / Delivered Orders Count", table_cell_style), Paragraph("R$ 137.04 per delivered order", table_cell_style)],
        [Paragraph("Late Rate (%)", table_cell_style), Paragraph("COUNT(is_late=True) / Delivered Orders", table_cell_style), Paragraph("Delivered customer date > estimated date (8.11%)", table_cell_style)],
        [Paragraph("Days to Delivery", table_cell_style), Paragraph("(delivered_customer_date - purchase_timestamp) / 86400", table_cell_style), Paragraph("Mean: 12.56 days | Median: 10.22 days", table_cell_style)],
        [Paragraph("RFM Score", table_cell_style), Paragraph("Recency Quintile + Frequency Quintile + Monetary Quintile", table_cell_style), Paragraph("Range 3 to 15 (Max observed: 11 points)", table_cell_style)]
    ]
    t_dict = Table(dict_rows, colWidths=[120, 220, 164])
    t_dict.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('BOX', (0, 0), (-1, -1), 1, BORDER_COLOR),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDER_COLOR),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(t_dict)
    story.append(Spacer(1, 10))

    story.append(Paragraph("Appendix B: Pipeline Reproducibility Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=SLATE, spaceBefore=0, spaceAfter=6))

    repro_text = (
        "The complete analysis is 100% reproducible through the following terminal workflow:<br/>"
        "1. <b>Download Raw Data:</b> Clone the public mirror or extract Kaggle datasets into <code>data/raw/</code>.<br/>"
        "2. <b>Execute Cleaning Pipeline:</b> Run <code>python build_olist.py</code>. This cleans the data, produces all 14 clean CSVs in <code>data/clean/</code>, and enforces Gate 1 and Gate 2 verification checks.<br/>"
        "3. <b>Generate Figures:</b> Run <code>python generate_charts.py</code> to produce 7 publication charts in <code>charts/</code>.<br/>"
        "4. <b>Build Excel Workbook:</b> Run <code>python build_excel.py</code> to generate <code>Olist_Ecommerce_Workbook.xlsx</code> and verify Gate 3.<br/>"
        "5. <b>Launch Web Dashboard:</b> Run <code>streamlit run streamlit_app/app.py</code> to interact with the multi-page dashboard.<br/>"
        "6. <b>Power BI Build:</b> Follow <code>powerbi/Build_Guide.md</code> using DAX measures and Power Query M code."
    )
    story.append(Paragraph(repro_text, body_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"PDF successfully generated at {PDF_PATH}")


if __name__ == "__main__":
    build_pdf()
