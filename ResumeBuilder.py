import re
import sys
import os
import fitz  # PyMuPDF
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout
from PyQt5.QtGui import QIcon
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from PyQt5.QtCore import Qt

class ResumeBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_count = 0
    
    def initUI(self):
        self.setWindowTitle('Resume Builder')
        self.setWindowIcon(QIcon('icon.png'))  # Set your icon file path
        self.setStyleSheet("background-color: #f0f0f0;")

        screen = QApplication.desktop().screenGeometry()
        self.setGeometry(screen)
        
        # Create widgets
        self.name_label = QLabel('Full Name:', self)
        self.name_edit = QLineEdit(self)
        self.email_label = QLabel('Email:', self)
        self.email_edit = QLineEdit(self)
        self.phone_label = QLabel('Phone:', self)
        self.phone_edit = QLineEdit(self)
        self.address_label = QLabel('Address:', self)
        self.address_edit = QLineEdit(self)

        self.sum_label = QLabel('Summary:', self)
        self.sum_edit = QTextEdit(self)

        self.edu_label = QLabel('Education:', self)
        self.edu_edit = QTextEdit(self)

        self.exp_label = QLabel('Experience:', self)
        self.exp_edit = QTextEdit(self)

        self.skills_label = QLabel('Skills:', self)
        self.skills_edit = QTextEdit(self)

        self.certifications_label = QLabel('Certifications:', self)
        self.certifications_edit = QTextEdit(self)

        self.add_image_button = QPushButton('Add Image', self)
        self.add_image_button.clicked.connect(self.add_image)
        self.submit_button = QPushButton('Generate Resume', self)
        self.submit_button.clicked.connect(self.generate_resume)
        self.import_button = QPushButton('Import Resume', self)
        self.import_button.clicked.connect(self.import_resume)

        # Set labels alignment
        self.name_label.setAlignment(Qt.AlignCenter)
        self.email_label.setAlignment(Qt.AlignCenter)
        self.phone_label.setAlignment(Qt.AlignCenter)
        self.address_label.setAlignment(Qt.AlignCenter)

        # Create layout
        layout = QVBoxLayout()

        # Add widgets to layout
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_edit)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_edit)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_edit)
        layout.addWidget(self.address_label)
        layout.addWidget(self.address_edit)
        layout.addWidget(self.sum_label)
        layout.addWidget(self.sum_edit)
        layout.addWidget(self.edu_label)
        layout.addWidget(self.edu_edit)
        layout.addWidget(self.exp_label)
        layout.addWidget(self.exp_edit)
        layout.addWidget(self.skills_label)
        layout.addWidget(self.skills_edit)
        layout.addWidget(self.certifications_label)
        layout.addWidget(self.certifications_edit)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_image_button)
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.import_button)
        layout.addLayout(button_layout)

        # Set layout
        self.setLayout(layout)

    def import_resume(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Resume", "", "PDF Files (*.pdf)", options=options)
        if file_path:
            self.extract_resume_data(file_path)

    def generate_resume(self):
        name = self.name_edit.text()
        email = self.email_edit.text()
        phone = self.phone_edit.text()
        address = self.address_edit.text()
        summary = self.edu_edit.toPlainText()
        education = self.edu_edit.toPlainText()
        experience = self.exp_edit.toPlainText()
        skills = self.skills_edit.toPlainText()
        certifications = self.certifications_edit.toPlainText()

        # Get the file save location from the user
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Resume", f"{name}_resume.pdf", "PDF Files (*.pdf)", options=options)

        if file_path:
            doc = SimpleDocTemplate(file_path, pagesize=letter)

            styles = getSampleStyleSheet()
            header_style = styles['Heading1']
            header_style.textColor = colors.HexColor('#4a4a4a')
            section_title_style = ParagraphStyle(name='SectionTitle', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#0066cc'))
            content_style = styles['BodyText']

            # Customize the bullet style
            bullet_color = colors.HexColor('#333333')  # Dark gray
            bullet_size = 6  # smaller bullet size
            bullet_transparency = 0.5  # make the bullet slightly transparent
            bullet_style = ParagraphStyle(
                name='Bullet',
                parent=styles['ListItem'],
                bulletColor=bullet_color,
                bulletFontName='Helvetica',
                bulletFontSize=bullet_size,
                bulletTransparency=bullet_transparency,
            )

            elements = []

            # Header
            header_text = f"<b>{name}</b><br/>{email}<br/>{phone}<br/>{address}"
            elements.append(Paragraph(header_text, header_style))
            elements.append(Spacer(1, 12))

            # Summary
            elements.append(Paragraph('<b>Summary</b>', section_title_style))
            elements.append(Paragraph(summary.replace('\n', '<br/>'), content_style))
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
            skills_list = skills.split('\n')
            skills_bullet_points = ListFlowable(
                [ListItem(Paragraph(skill, content_style), bulletColor=bullet_color, bulletFontName='Helvetica', bulletFontSize=bullet_size, bulletTransparency=bullet_transparency) for skill in skills_list], # type: ignore
                bulletType='bullet',
                start='circle',
                style=bullet_style,
            )
            elements.append(skills_bullet_points)

            # Certifications
            elements.append(Paragraph('<b>Certifications</b>', section_title_style))
            elements.append(Paragraph(certifications.replace('\n', '<br/>'), content_style))

             # Watermark with hyperlink
            watermark_text = "Created using <a href='https://github.com/afadeofred/ResumeBuilder/tree/main'>ResumeBuilder by Arun </a>"
            watermark_style = ParagraphStyle(name='Watermark', parent=styles['Normal'], fontSize=10, textColor=colors.HexColor('#999999'))
            watermark = Paragraph(watermark_text, watermark_style)
            elements.append(Spacer(1, 36))  # Add space before the watermark
            elements.append(watermark)


            doc.build(elements)

            print(f"Resume saved as '{file_path}'")

    def add_image(self):
        if self.image_count >= 2:
            print("You can't add more than 2 images.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Add Image", "", "Image Files (*.png *.jpg *.jpeg)", options=options)
        if file_path:
            if self.check_image_size(file_path):
                image_path = f"image_{self.image_count}.png"
                self.image_count += 1
                with open(file_path, "rb") as f:
                    with open(image_path, "wb") as out:
                        out.write(f.read())

    def check_image_size(self, file_path):
        max_size = 2 * 1024 * 1024  # 2 MB
        size = os.path.getsize(file_path)
        if size > max_size:
            print("Image size exceeds 2 MB. Please select a smaller image.")
            return False
        return True

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
        self.edu_edit.setText(information.get('summary', ''))
        self.edu_edit.setText(information.get('education', ''))
        self.exp_edit.setText(information.get('experience', ''))
        self.skills_edit.setText(information.get('skills', ''))
        self.certifications_edit.setText(information.get('certifications', ''))     

    def extract_information_from_text(self, text):
        # Define patterns to search for relevant information
        patterns = {
            'name': r'Full Name:\s*(.*)',
            'email': r'Email:\s*(.*)',
            'phone': r'Phone:\s*(.*)',
            'address': r'Address:\s*(.*)',
            'education': r'Education:(.*?)Experience:',
            'experience': r'Experience:(.*?)Skills:',
            'skills': r'Skills:(.*?)Certifications:',
            'certifications': r'Certifications:(.*)'
        }

        information = {}

        # Extract information using regular expressions
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
            if match:
                information[key] = match.group(1).strip()

        return information


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResumeBuilder()
    window.showMaximized()  # Show the window maximized
    sys.exit(app.exec_())

