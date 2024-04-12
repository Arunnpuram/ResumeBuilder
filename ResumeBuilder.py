import sys
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
        self.setGeometry(100, 100, 400, 500)

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
        self.skills_edit = QLineEdit()

        self.submit_button = QPushButton('Generate Resume')
        self.submit_button.clicked.connect(self.generate_resume)

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

        self.setLayout(layout)

    def generate_resume(self):
        name = self.name_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        address = self.address_edit.text()
        education = self.edu_edit.toPlainText()
        experience = self.exp_edit.toPlainText()
        skills = self.skills_edit.text()

        # Get the file save location from the user
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Resume", f"{name}_resume.pdf", "PDF Files (*.pdf)", options=options)

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

            doc.build(elements)

            print(f"Resume saved as '{file_path}'")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResumeBuilder()
    window.show()
    sys.exit(app.exec_())
