; Auto-generated. Do not edit!


(cl:in-package blob_segmentation-msg)


;//! \htmlinclude Centroid.msg.html

(cl:defclass <Centroid> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type cl:integer
    :initform 0)
   (y
    :reader y
    :initarg :y
    :type cl:integer
    :initform 0)
   (area
    :reader area
    :initarg :area
    :type cl:integer
    :initform 0))
)

(cl:defclass Centroid (<Centroid>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <Centroid>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'Centroid)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name blob_segmentation-msg:<Centroid> is deprecated: use blob_segmentation-msg:Centroid instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <Centroid>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader blob_segmentation-msg:x-val is deprecated.  Use blob_segmentation-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <Centroid>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader blob_segmentation-msg:y-val is deprecated.  Use blob_segmentation-msg:y instead.")
  (y m))

(cl:ensure-generic-function 'area-val :lambda-list '(m))
(cl:defmethod area-val ((m <Centroid>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader blob_segmentation-msg:area-val is deprecated.  Use blob_segmentation-msg:area instead.")
  (area m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <Centroid>) ostream)
  "Serializes a message object of type '<Centroid>"
  (cl:let* ((signed (cl:slot-value msg 'x)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'y)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'area)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 4294967296) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) unsigned) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <Centroid>) istream)
  "Deserializes a message object of type '<Centroid>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'x) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'y) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) unsigned) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'area) (cl:if (cl:< unsigned 2147483648) unsigned (cl:- unsigned 4294967296))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<Centroid>)))
  "Returns string type for a message object of type '<Centroid>"
  "blob_segmentation/Centroid")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'Centroid)))
  "Returns string type for a message object of type 'Centroid"
  "blob_segmentation/Centroid")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<Centroid>)))
  "Returns md5sum for a message object of type '<Centroid>"
  "b3ff87eeaf6039576da4242a0369417e")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'Centroid)))
  "Returns md5sum for a message object of type 'Centroid"
  "b3ff87eeaf6039576da4242a0369417e")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<Centroid>)))
  "Returns full string definition for message of type '<Centroid>"
  (cl:format cl:nil "int32 x~%int32 y~%int32 area~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'Centroid)))
  "Returns full string definition for message of type 'Centroid"
  (cl:format cl:nil "int32 x~%int32 y~%int32 area~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <Centroid>))
  (cl:+ 0
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <Centroid>))
  "Converts a ROS message object to a list"
  (cl:list 'Centroid
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
    (cl:cons ':area (area msg))
))
