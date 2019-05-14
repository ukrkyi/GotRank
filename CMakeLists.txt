cmake_minimum_required(VERSION 2.8)

project(GotRank)

find_package (Eigen3 3.3 REQUIRED NO_MODULE)

add_executable(${PROJECT_NAME} "main.cpp")
target_link_libraries (${PROJECT_NAME} Eigen3::Eigen)

