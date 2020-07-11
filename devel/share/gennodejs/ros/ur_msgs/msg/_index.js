
"use strict";

let Analog = require('./Analog.js');
let MasterboardDataMsg = require('./MasterboardDataMsg.js');
let IOStates = require('./IOStates.js');
let ToolDataMsg = require('./ToolDataMsg.js');
let Digital = require('./Digital.js');
let RobotStateRTMsg = require('./RobotStateRTMsg.js');
let RobotModeDataMsg = require('./RobotModeDataMsg.js');

module.exports = {
  Analog: Analog,
  MasterboardDataMsg: MasterboardDataMsg,
  IOStates: IOStates,
  ToolDataMsg: ToolDataMsg,
  Digital: Digital,
  RobotStateRTMsg: RobotStateRTMsg,
  RobotModeDataMsg: RobotModeDataMsg,
};
