
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Resume Builder"

    GridLayout {
        columns: 2
        anchors.fill: parent
        anchors.margins: 10

        Label {
            text: "Full Name:"
        }
        TextField {
            id: nameEdit
        }

        Label {
            text: "Email:"
        }
        TextField {
            id: emailEdit
        }

        Label {
            text: "Phone:"
        }
        TextField {
            id: phoneEdit
        }

        Label {
            text: "Address:"
        }
        TextField {
            id: addressEdit
        }

        Label {
            text: "Summary:"
        }
        TextArea {
            id: summaryEdit
        }

        Label {
            text: "Education:"
        }
        TextArea {
            id: educationEdit
        }

        Label {
            text: "Experience:"
        }
        TextArea {
            id: experienceEdit
        }

        Label {
            text: "Skills:"
        }
        TextArea {
            id: skillsEdit
        }

        Label {
            text: "Certifications:"
        }
        TextArea {
            id: certificationsEdit
        }

        Button {
            text: "Add Image"
            onClicked: {
                addImage()
            }
        }

        Button {
            text: "Generate Resume"
            onClicked: {
                generateResume()
            }
        }

        Button {
            text: "Import Resume"
            onClicked: {
                importResume()
            }
        }
    }

    signal addImage()
    signal generateResume()
    signal importResume()
}
