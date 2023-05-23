;; Auto-generated. Do not edit!


(when (boundp 'blob_segmentation::Centroid)
  (if (not (find-package "BLOB_SEGMENTATION"))
    (make-package "BLOB_SEGMENTATION"))
  (shadow 'Centroid (find-package "BLOB_SEGMENTATION")))
(unless (find-package "BLOB_SEGMENTATION::CENTROID")
  (make-package "BLOB_SEGMENTATION::CENTROID"))

(in-package "ROS")
;;//! \htmlinclude Centroid.msg.html


(defclass blob_segmentation::Centroid
  :super ros::object
  :slots (_x _y _area ))

(defmethod blob_segmentation::Centroid
  (:init
   (&key
    ((:x __x) 0)
    ((:y __y) 0)
    ((:area __area) 0)
    )
   (send-super :init)
   (setq _x (round __x))
   (setq _y (round __y))
   (setq _area (round __area))
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:area
   (&optional __area)
   (if __area (setq _area __area)) _area)
  (:serialization-length
   ()
   (+
    ;; int32 _x
    4
    ;; int32 _y
    4
    ;; int32 _area
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; int32 _x
       (write-long _x s)
     ;; int32 _y
       (write-long _y s)
     ;; int32 _area
       (write-long _area s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; int32 _x
     (setq _x (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _y
     (setq _y (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;; int32 _area
     (setq _area (sys::peek buf ptr- :integer)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get blob_segmentation::Centroid :md5sum-) "b3ff87eeaf6039576da4242a0369417e")
(setf (get blob_segmentation::Centroid :datatype-) "blob_segmentation/Centroid")
(setf (get blob_segmentation::Centroid :definition-)
      "int32 x
int32 y
int32 area

")



(provide :blob_segmentation/Centroid "b3ff87eeaf6039576da4242a0369417e")


