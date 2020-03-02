cmake_minimum_required(VERSION 2.8.12)
project(test_package)

set(CMAKE_VERBOSE_MAKEFILE TRUE)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Find the QtCore library
find_package(Qt5Core CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
message(INFO ${CONAN_LIBS})
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} Qt5::Core)
