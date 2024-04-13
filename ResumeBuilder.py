import sys
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QFileDialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


class ResumeBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('Resume Builder')
        self.setGeometry(100, 100, 400, 500) #Adjust According to your requirements

        self.name_label = QLabel('Full Name:')
        self.name_edit = QLineEdit()
        self.email_label = QLabel('Email:')
        self.email_edit = QLineEdit()
        self.phone_label = QLabel('Phone:')
        self.phone_edit = QLineEdit()
        self.address_label = QLabel('Address:')
        self.address_edit = QLineEdit()

        self.edu_label = QLabel('Education:')
        self.edu_edit = QTextEdit()

        self.exp_label = QLabel('Experience:')
        self.exp_edit = QTextEdit()

        self.skills_label = QLabel('Skills:')
        self.skills_edit = QTextEdit()

        self.skills_label = QLabel('Certifications:')
        self.skills_edit = QTextEdit()

        self.submit_button = QPushButton('Generate Resume')
        self.submit_button.clicked.connect(self.generate_resume)

        self.import_button = QPushButton('Import Resume')
        self.import_button.clicked.connect(self.import_resume)

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_edit)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_edit)
        layout.addWidget(self.edu_label)
        layout.addWidget(self.edu_edit)
        layout.addWidget(self.exp_label)
        layout.addWidget(self.exp_edit)
        layout.addWidget(self.skills_label)
        layout.addWidget(self.skills_edit)
        layout.addWidget(self.submit_button)
        layout.addWidget(self.import_button)

        self.setLayout(layout)
        self.update()


    def import_resume(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Resume", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.extract_resume_data(file_path)

    def extract_information_from_text(self, text):
        # Define patterns to search for relevant information
        patterns = {
            'name': r'Full Name:\s*(.*)',
            'email': r'Email:\s*(.*)',
            'phone': r'Phone:\s*(.*)',
            'address': r'Address:\s*(.*)',
            'education': r'Education:(.*?)Experience:',
            'experience': r'Experience:(.*?)Skills:',
            'skills': r'Skills:(.*)'
        }

        information = {}

        # Extract information using regular expressions
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                information[key] = match.group(1).strip()

        return information

    def extract_resume_data(self, file_path):
        doc = fitz.open(file_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()

        # Extract information from text
        information = self.extract_information_from_text(text)

        # Populate text fields
        self.name_edit.setText(information.get('name', ''))
        self.email_edit.setText(information.get('email', ''))
        self.phone_edit.setText(information.get('phone', ''))
        self.address_edit.setText(information.get('address', ''))
        self.edu_edit.setText(information.get('education', ''))
        self.exp_edit.setText(information.get('experience', ''))
        self.skills_edit.setText(information.get('skills', ''))    

    def generate_resume(self):
        name = self.name_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        address = self.address_edit.text()
        education = self.edu_edit.toPlainText()
        experience = self.exp_edit.toPlainText()
        skills = self.skills_edit.toPlainText()  # Use toPlainText() instead of text

        # Get the file save location from the user
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Resume", f"{name}_resume.pdf", "PDF Files (*.pdf)", options=options) #For docx replace with _resume.docx", "DOCX Files (*.docx)"

        if file_path:
            doc = SimpleDocTemplate(file_path, pagesize=letter)

            styles = getSampleStyleSheet()
            header_style = styles['Heading1']
            header_style.textColor = colors.HexColor('#4a4a4a')
            section_title_style = ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#0066cc'))
            content_style = styles['BodyText']
            
            elements = []

            # Header
            header_text = f"<b>{name}</b><br/>{email}<br/>{phone}<br/>{address}"
            elements.append(Paragraph(header_text, header_style))
            elements.append(Spacer(1, 12))

            # Education
            elements.append(Paragraph('<b>Education</b>', section_title_style))
            elements.append(Paragraph(education.replace('\n', '<br/>'), content_style))
            elements.append(Spacer(1, 12))

            # Experience
            elements.append(Paragraph('<b>Experience</b>', section_title_style))
            elements.append(Paragraph(experience.replace('\n', '<br/>'), content_style))
            elements.append(Spacer(1, 12))

            # Skills
            elements.append(Paragraph('<b>Skills</b>', section_title_style))
            elements.append(Paragraph(skills, content_style))

            # Certifications
            elements.append(Paragraph('<b>Certificationss</b>', section_title_style))
            elements.append(Paragraph(Certifications, content_style))


            # Watermark with hyperlink
            watermark_text = "This resume is created using <a href='https://github.com/afadeofred/ResumeBuilder/tree/main'>ResumeBuilder by Arun </a>"
            watermark_style = ParagraphStyle(name='Watermark', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#999999'))
            watermark = Paragraph(watermark_text, watermark_style)
            elements.append(Spacer(1, 36))  # Add space before the watermark
            elements.append(watermark)

            doc.build(elements)

            print(f"Resume saved as '{file_path}'")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResumeBuilder()
    window.show()
    sys.exit(app.exec_())
