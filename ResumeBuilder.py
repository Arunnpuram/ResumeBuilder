# Copyright (C) 2024 Arun Puram
# Licensed under the GPL-3.0 License.
# Created for Utils: https://github.com/afadeofred/ResumeBuilder

# "Resume Builder Launcher" 

# A simple yet modern-like GUI application to build Resumes.

import sys
import os
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QFileDialog
from PySide6.QtQuickWidgets import QQuickWidget
from PySide6.QtCore import QUrl, QObject


class ResumeBuilder(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image_count = 0

    def initUI(self):
        self.setWindowTitle('Resume Builder')
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout(self)
        self.qml_widget = QQuickWidget(self)
        qml_path = os.path.join(os.path.dirname(__file__), 'Resumebuilder.qml')
        print("QML PATH:", qml_path)

        if not os.path.exists(qml_path):
            print("Error: QML file does not exist")
            return

        self.qml_widget.setSource(QUrl.fromLocalFile(qml_path))
        self.qml_widget.setResizeMode(QQuickWidget.SizeRootObjectToView)
        layout.addWidget(self.qml_widget)

        # Connect QML signals to Python slots
        self.qml_widget.statusChanged.connect(self.on_status_changed)

    def on_status_changed(self, status):
        if status == QQuickWidget.Error:
            for error in self.qml_widget.errors():
                print(error.toString())
            return

        root_object = self.qml_widget.rootObject()
        print("Root Object:", root_object)  # Debug print
        if root_object is None:
            print("Error: Root object is None")
            return

        root_object.addImage.connect(self.add_image)
        root_object.generateResume.connect(self.generate_resume)
        root_object.importResume.connect(self.import_resume)

    def import_resume(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Resume", "", "PDF Files (*.pdf)")
        if file_path:
            self.extract_resume_data(file_path)

    def generate_resume(self):
        # Extract data from QML fields and generate resume
        root_object = self.qml_widget.rootObject()
        name = root_object.findChild(QObject, 'nameEdit').property('text')
        email = root_object.findChild(QObject, 'emailEdit').property('text')
        phone = root_object.findChild(QObject, 'phoneEdit').property('text')
        address = root_object.findChild(QObject, 'addressEdit').property('text')
        summary = root_object.findChild(QObject, 'summaryEdit').property('text')
        education = root_object.findChild(QObject, 'educationEdit').property('text')
        experience = root_object.findChild(QObject, 'experienceEdit').property('text')
        skills = root_object.findChild(QObject, 'skillsEdit').property('text')
        certifications = root_object.findChild(QObject, 'certificationsEdit').property('text')

        # Further implementation for generating the resume...

    def add_image(self):
        if self.image_count >= 2:
            print("You can't add more than 2 images.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Add Image", "", "Image Files (*.png *.jpg *.jpeg)")
        if file_path:
            if self.check_image_size(file_path):
                image_path = f"image_{self.image_count}.png"
                self.image_count += 1
                with open(file_path, "rb") as f:
                    with open(image_path, "wb") as out:
                        out.write(f.read())

    def check_image_size(self, file_path):
        # Dummy check function
        return True

    def extract_resume_data(self, file_path):
        # Placeholder for the actual text extraction logic
        text = "sample text from pdf"
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
                if key == 'skills':
                    # Extract skills as a list of tuples
                    skills_list = []
                    skills_text = match.group(1).strip().split('\n')
                    for skill in skills_text:
                        parts = skill.split(':')
                        if len(parts) == 2:
                            skills_list.append((parts[0].strip(), parts[1].strip()))
                    information[key] = skills_list
                else:
                    information[key] = match.group(1).strip()

        return information

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ResumeBuilder()
    window.show()
    sys.exit(app.exec())
