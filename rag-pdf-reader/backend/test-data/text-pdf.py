from fpdf import FPDF

# Read the text file
with open("animals_database.txt", "r", encoding="utf-8") as f:
    content = f.readlines()

# Create PDF
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

for line in content:
    # Strip newline characters
    line = line.strip()
    if line:
        pdf.multi_cell(0, 10, line)

# Save PDF
pdf.output("animals_database.pdf")
print("✅ animals_database.pdf created successfully!")