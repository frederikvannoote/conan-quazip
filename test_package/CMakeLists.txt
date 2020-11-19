cmake_minimum_required(VERSION 3.1)
project(test_package)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Find the QtCore library
find_package(Qt5Core CONFIG REQUIRED)
find_package(QuaZip-Qt5 REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)

target_link_libraries(${PROJECT_NAME} QuaZip::QuaZip Qt5::Core)
