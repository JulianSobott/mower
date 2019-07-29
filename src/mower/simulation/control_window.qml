import QtQuick 2.5
import QtQuick.Layouts 1.4
import QtQuick.Controls 1.4

ApplicationWindow {
    width: 300
    height: 200
    title: "Simple"
    visible: true

    GridLayout {
        columns: 3

        Text { text: "Three"; font.bold: true; }
        Text { text: "words"; color: "red" }
        Text { text: "in"; font.underline: true }
        Text { text: "a"; font.pixelSize: 20 }
        Text { text: "row"; font.strikeout: true }
    }

}