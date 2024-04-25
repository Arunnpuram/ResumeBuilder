# Resume Builder

![alt text](https://github.com/afadeofred/ResumeBuilder/blob/main/logo.png)

A free ResumeBuilder made in Python uses PyQt5 GUI and saves resume in a PDF file upon taking input.

How to Use:-
pip install -r requirements.txt 

<h1> --This installs the required modules to run the script. </h1>

![alt text](https://github.com/afadeofred/ResumeBuilder/blob/main/Screenshot%202024-04-14%20085826.png)

1. run py ResumeBuilder.py to run the GUI
2. Fill in your information
3. Click on Generate Resume
4. Save the file to your specified path as a pdf file.

New Features added:- 
Import Resume.
1. Integrated the extract_information_from_text function into the ResumeBuilder class.
2. The extract_resume_data method now uses PyMuPDF to extract text from the PDF resume file specified by the user.
3. It then calls the extract_information_from_text method to parse the extracted text and populate the text fields with the relevant information.
4. Added Summary text field
5. Added Add Image button to add images to the resume( The max cap is 2 MB)
6. Added Button points layout for skills for better Format. Skills will be listed as bullet points on the output file

 Here's a sample resume output as pdf file:-

 ![alt text](https://github.com/afadeofred/ResumeBuilder/blob/main/Screenshot%202024-04-12%20145205.png)


