
"use strict";

let MotorReadings = require('./MotorReadings.js');
let SetGrapplerAxis = require('./SetGrapplerAxis.js');
let EncoderReadings = require('./EncoderReadings.js');
let NorthStarReadings = require('./NorthStarReadings.js');
let SetGrapplerAxes = require('./SetGrapplerAxes.js');
let GrapplerReadings = require('./GrapplerReadings.js');
let GripperState = require('./GripperState.js');
let PowerReadings = require('./PowerReadings.js');
let DigitalReadings = require('./DigitalReadings.js');
let SetBHAPressures = require('./SetBHAPressures.js');
let BHAReadings = require('./BHAReadings.js');
let AnalogReadings = require('./AnalogReadings.js');

module.exports = {
  MotorReadings: MotorReadings,
  SetGrapplerAxis: SetGrapplerAxis,
  EncoderReadings: EncoderReadings,
  NorthStarReadings: NorthStarReadings,
  SetGrapplerAxes: SetGrapplerAxes,
  GrapplerReadings: GrapplerReadings,
  GripperState: GripperState,
  PowerReadings: PowerReadings,
  DigitalReadings: DigitalReadings,
  SetBHAPressures: SetBHAPressures,
  BHAReadings: BHAReadings,
  AnalogReadings: AnalogReadings,
};
