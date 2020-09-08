cmake_minimum_required(VERSION 3.1)
project(test_package)


include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

# Find the QtCore library
find_package(Qt5Core CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
message(INFO ${CONAN_LIBS})
target_link_libraries(${PROJECT_NAME} ${CONAN_LIBS} Qt5::Core)
