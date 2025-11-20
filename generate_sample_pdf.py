#!/usr/bin/env python3
"""Generate a sample contract PDF for testing."""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import os

# Create a sample contract PDF
pdf_path = "sample_contract.pdf"
c = canvas.Canvas(pdf_path, pagesize=letter)
width, height = letter

# Title
c.setFont("Helvetica-Bold", 16)
c.drawString(1 * inch, height - 1 * inch, "SERVICE AGREEMENT CONTRACT")

# Contract details
c.setFont("Helvetica", 11)
y_position = height - 1.5 * inch

contract_text = [
    'This Service Agreement ("Agreement") is entered into as of January 15, 2024,',
    "between Acme Corporation, a Delaware corporation with offices at 123 Main Street,",
    'San Francisco, CA 94102 ("Client"), and Tech Solutions LLC, a California limited',
    'liability company located at 456 Oak Avenue, Palo Alto, CA 94301 ("Service Provider").',
    "",
    "WHEREAS, Client desires to engage Service Provider to provide software development",
    "services, and Service Provider agrees to provide such services on the terms set forth",
    "in this Agreement.",
    "",
    "NOW, THEREFORE, in consideration of the mutual covenants and agreements contained",
    "herein, the parties agree as follows:",
    "",
    "1. SERVICES",
    "Service Provider shall provide software development and consulting services as",
    "described in Exhibit A attached hereto.",
    "",
    "2. COMPENSATION",
    "Client agrees to pay Service Provider a total fee of $150,000.00 (One Hundred Fifty",
    "Thousand Dollars) for the services. Payment shall be made in three installments:",
    "- $50,000.00 upon execution of this Agreement",
    "- $50,000.00 upon completion of Phase 1 (March 30, 2024)",
    "- $50,000.00 upon final delivery (June 15, 2024)",
    "",
    "3. TERM",
    "This Agreement shall commence on February 1, 2024 and continue until June 30, 2024,",
    "unless earlier terminated in accordance with the terms herein.",
    "",
    "4. CONTACT PERSONS",
    "Client Representative: John Smith, Chief Technology Officer",
    "Email: john.smith@acmecorp.com",
    "Phone: (415) 555-1234",
    "",
    "Service Provider Representative: Jane Doe, Project Manager",
    "Email: jane.doe@techsolutions.com",
    "Phone: (650) 555-5678",
    "",
    "5. CONFIDENTIALITY",
    "Both parties agree to maintain confidentiality of all proprietary information",
    "disclosed during the term of this Agreement.",
    "",
    "6. INTELLECTUAL PROPERTY",
    "All work product created by Service Provider under this Agreement shall be",
    "the exclusive property of Microsoft Azure Solutions Division upon payment.",
    "",
    "7. LIABILITY",
    "The total liability of either party shall not exceed $500,000.00 (Five Hundred",
    "Thousand Dollars) for any claims arising under this Agreement.",
    "",
    "8. GOVERNING LAW",
    "This Agreement shall be governed by the laws of the State of California.",
    "",
    "9. NOTICES",
    "All notices shall be sent to the addresses listed above or to:",
    "Legal Department, Acme Corporation, New York, NY 10001",
    "",
    "",
    "IN WITNESS WHEREOF, the parties have executed this Agreement as of the date",
    "first written above.",
    "",
    "ACME CORPORATION                    TECH SOLUTIONS LLC",
    "",
    "By: _____________________           By: _____________________",
    "Name: Robert Johnson                Name: Sarah Williams",
    "Title: CEO                          Title: Managing Director",
    "Date: January 15, 2024             Date: January 15, 2024",
    "",
    "Witness: Emily Chen                 Witness: Michael Brown",
    "Location: Boston, MA                Location: Seattle, WA",
]

line_height = 14
for line in contract_text:
    c.drawString(0.75 * inch, y_position, line)
    y_position -= line_height
    if y_position < 1 * inch:
        c.showPage()
        c.setFont("Helvetica", 11)
        y_position = height - 1 * inch

c.save()
print(f"✓ Sample contract PDF created: {os.path.abspath(pdf_path)}")
print(f"✓ File size: {os.path.getsize(pdf_path):,} bytes")
print(f"\nThe PDF contains entities for testing:")
print(
    "- Organizations: Acme Corporation, Tech Solutions LLC, Microsoft Azure Solutions Division"
)
print(
    "- People: John Smith, Jane Doe, Robert Johnson, Sarah Williams, Emily Chen, Michael Brown"
)
print("- Locations: San Francisco CA, Palo Alto CA, New York NY, Boston MA, Seattle WA")
print(
    "- Dates: January 15 2024, February 1 2024, March 30 2024, June 15 2024, June 30 2024"
)
print("- Money: $150,000.00, $50,000.00, $500,000.00")
