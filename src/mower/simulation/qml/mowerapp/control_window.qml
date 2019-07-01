import QtQuick 2.0
import QtQuick.Controls 2.4

Item {
    width: 640
    height: 480
    property alias tfFpsLoggerText: tfFpsLogger.text

    Column {
        id: column
        x: 0
        y: 0
        width: 640
        height: 480

        Row {
            id: row
            width: 200
            height: 400

            Text {
                id: text1
                text: qsTr("FPS: ")
                font.pixelSize: 18
            }

            Text {
                id: tfFpsLogger
                objectName: "tfFpsLogger"
                text: qsTr("None")
                font.pixelSize: 18
            }
        }
    }

}
