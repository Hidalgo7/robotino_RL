# Install script for directory: /home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_teleop_joy

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_teleop_joy/catkin_generated/installspace/robotino_teleop_joy.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_teleop_joy/cmake" TYPE FILE FILES
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_teleop_joy/catkin_generated/installspace/robotino_teleop_joyConfig.cmake"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_teleop_joy/catkin_generated/installspace/robotino_teleop_joyConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_teleop_joy" TYPE FILE FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_teleop_joy/package.xml")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_teleop_joy" TYPE DIRECTORY FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_teleop_joy/launch")
endif()

