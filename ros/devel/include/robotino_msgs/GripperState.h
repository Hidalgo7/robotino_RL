// Generated by gencpp from file robotino_msgs/GripperState.msg
// DO NOT EDIT!


#ifndef ROBOTINO_MSGS_MESSAGE_GRIPPERSTATE_H
#define ROBOTINO_MSGS_MESSAGE_GRIPPERSTATE_H


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
struct GripperState_
{
  typedef GripperState_<ContainerAllocator> Type;

  GripperState_()
    : stamp()
    , state(false)  {
    }
  GripperState_(const ContainerAllocator& _alloc)
    : stamp()
    , state(false)  {
  (void)_alloc;
    }



   typedef ros::Time _stamp_type;
  _stamp_type stamp;

   typedef uint8_t _state_type;
  _state_type state;





  typedef boost::shared_ptr< ::robotino_msgs::GripperState_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::robotino_msgs::GripperState_<ContainerAllocator> const> ConstPtr;

}; // struct GripperState_

typedef ::robotino_msgs::GripperState_<std::allocator<void> > GripperState;

typedef boost::shared_ptr< ::robotino_msgs::GripperState > GripperStatePtr;
typedef boost::shared_ptr< ::robotino_msgs::GripperState const> GripperStateConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::robotino_msgs::GripperState_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::robotino_msgs::GripperState_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::robotino_msgs::GripperState_<ContainerAllocator1> & lhs, const ::robotino_msgs::GripperState_<ContainerAllocator2> & rhs)
{
  return lhs.stamp == rhs.stamp &&
    lhs.state == rhs.state;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::robotino_msgs::GripperState_<ContainerAllocator1> & lhs, const ::robotino_msgs::GripperState_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace robotino_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsMessage< ::robotino_msgs::GripperState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::robotino_msgs::GripperState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::robotino_msgs::GripperState_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::robotino_msgs::GripperState_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::robotino_msgs::GripperState_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::robotino_msgs::GripperState_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::robotino_msgs::GripperState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9aa764d58396f955a97125bca8f1e897";
  }

  static const char* value(const ::robotino_msgs::GripperState_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9aa764d58396f955ULL;
  static const uint64_t static_value2 = 0xa97125bca8f1e897ULL;
};

template<class ContainerAllocator>
struct DataType< ::robotino_msgs::GripperState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "robotino_msgs/GripperState";
  }

  static const char* value(const ::robotino_msgs::GripperState_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::robotino_msgs::GripperState_<ContainerAllocator> >
{
  static const char* value()
  {
    return "time stamp\n"
"bool state	# true if open else false if closed\n"
;
  }

  static const char* value(const ::robotino_msgs::GripperState_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::robotino_msgs::GripperState_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.stamp);
      stream.next(m.state);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct GripperState_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::robotino_msgs::GripperState_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::robotino_msgs::GripperState_<ContainerAllocator>& v)
  {
    s << indent << "stamp: ";
    Printer<ros::Time>::stream(s, indent + "  ", v.stamp);
    s << indent << "state: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.state);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ROBOTINO_MSGS_MESSAGE_GRIPPERSTATE_H
