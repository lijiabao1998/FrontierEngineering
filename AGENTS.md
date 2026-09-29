# FrontierEngineering agent 入口

讀 README、STATUS、VALIDATION 與治理 9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f。agent 用 <agent>/ENG-xxx-<topic> 分支。每輪先凍結plant/model、fault set、operating envelope、safety constraints、baseline與acceptance。

simulation-first；不連真實電網、交通、機器人或工控設備。controller/model改動與safety/evaluator改動分PR。故障注入只在sandbox。不得把demo success寫成field safety。
