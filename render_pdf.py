from fpdf import FPDF

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Ficha de transparencia del modelo - Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

def create_pdf(data):
    pdf = PDF()
    pdf.add_page()

    pdf.set_font('Arial', size=12)
    for question, answer in data.items():
        pdf.cell(200, 10, txt=question, ln=True)
        pdf.multi_cell(0, 10, txt=str(answer))
        pdf.ln(10)

    pdf_file_path = 'ficha_transparencia.pdf'
    pdf.output(pdf_file_path)
    return pdf_file_path
