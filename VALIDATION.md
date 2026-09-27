# 工程驗證契約

每題先凍結plant/geometry、sensor model、disturbance/fault set、operating envelope、hard safety constraints、baseline、hardware class與simulation fidelity。
- nominal performance、fault recovery、stability、constraint violation與resource cost分開。
- OOD測試不能從training fault generator原樣抽樣。
- digital twin與physical system的model-form error要單獨估。
- closed-loop claim至少要有stability/safety monitor或故障停止機制；sandbox外需另行合資格審查。
- critical infrastructure研究只做防禦性、模擬與公開資料驗證，不輸出破壞操作。
