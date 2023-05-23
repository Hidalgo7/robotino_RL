# Install script for directory: /home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs

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
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_msgs/msg" TYPE FILE FILES
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/AnalogReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/BHAReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/DigitalReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/EncoderReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/GrapplerReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/GripperState.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/MotorReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/NorthStarReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/PowerReadings.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/SetBHAPressures.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/SetGrapplerAxes.msg"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/msg/SetGrapplerAxis.msg"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_msgs/srv" TYPE FILE FILES
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/srv/ResetOdometry.srv"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/srv/SetEncoderPosition.srv"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/srv/SetGripperState.srv"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_msgs/cmake" TYPE FILE FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_msgs/catkin_generated/installspace/robotino_msgs-msg-paths.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/devel/include/robotino_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/devel/share/roseus/ros/robotino_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/devel/share/common-lisp/ros/robotino_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/devel/share/gennodejs/ros/robotino_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/devel/lib/python3/dist-packages/robotino_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/devel/lib/python3/dist-packages/robotino_msgs")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_msgs/catkin_generated/installspace/robotino_msgs.pc")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_msgs/cmake" TYPE FILE FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_msgs/catkin_generated/installspace/robotino_msgs-msg-extras.cmake")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_msgs/cmake" TYPE FILE FILES
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_msgs/catkin_generated/installspace/robotino_msgsConfig.cmake"
    "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/build/robots/robotino/robotino_msgs/catkin_generated/installspace/robotino_msgsConfig-version.cmake"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/robotino_msgs" TYPE FILE FILES "/home/bee/irakaskuntza/tfg/2022-2023/IkerHidalgo/robotino_RL/ros/src/robots/robotino/robotino_msgs/package.xml")
endif()

