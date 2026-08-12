cmake_minimum_required(VERSION 3.16)
project(Qt5WidgetsFixture LANGUAGES CXX)

find_package(Qt5 REQUIRED COMPONENTS Widgets)
add_executable(app main.cpp)
target_link_libraries(app PRIVATE Qt5::Widgets)
