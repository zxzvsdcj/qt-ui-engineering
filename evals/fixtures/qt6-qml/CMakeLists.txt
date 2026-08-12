cmake_minimum_required(VERSION 3.16)
project(QtQuickFixture LANGUAGES CXX)

find_package(Qt6 REQUIRED COMPONENTS Quick QuickControls2)

qt_add_executable(app main.cpp)
qt_add_qml_module(app
    URI Fixture
    QML_FILES Main.qml
)
