// Generated by gencpp from file robotino_msgs/SetGripperStateResponse.msg
// DO NOT EDIT!


#ifndef ROBOTINO_MSGS_MESSAGE_SETGRIPPERSTATERESPONSE_H
#define ROBOTINO_MSGS_MESSAGE_SETGRIPPERSTATERESPONSE_H


#include <string>
#include <vector>
#include <memory>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace robotino_msgs
{
template <class ContainerAllocator>
struct SetGripperStateResponse_
{
  typedef SetGripperStateResponse_<ContainerAllocator> Type;

  SetGripperStateResponse_()
    {
    }
  SetGripperStateResponse_(const ContainerAllocator& _alloc)
    {
  (void)_alloc;
    }







  typedef boost::shared_ptr< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> const> ConstPtr;

}; // struct SetGripperStateResponse_

typedef ::robotino_msgs::SetGripperStateResponse_<std::allocator<void> > SetGripperStateResponse;

typedef boost::shared_ptr< ::robotino_msgs::SetGripperStateResponse > SetGripperStateResponsePtr;
typedef boost::shared_ptr< ::robotino_msgs::SetGripperStateResponse const> SetGripperStateResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


} // namespace robotino_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d41d8cd98f00b204e9800998ecf8427e";
  }

  static const char* value(const ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd41d8cd98f00b204ULL;
  static const uint64_t static_value2 = 0xe9800998ecf8427eULL;
};

template<class ContainerAllocator>
struct DataType< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "robotino_msgs/SetGripperStateResponse";
  }

  static const char* value(const ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "\n"
;
  }

  static const char* value(const ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream&, T)
    {}

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SetGripperStateResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream&, const std::string&, const ::robotino_msgs::SetGripperStateResponse_<ContainerAllocator>&)
  {}
};

} // namespace message_operations
} // namespace ros

#endif // ROBOTINO_MSGS_MESSAGE_SETGRIPPERSTATERESPONSE_H
