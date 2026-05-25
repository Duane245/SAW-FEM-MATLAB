# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 与
[Semantic Versioning](https://semver.org/lang/zh-CN/) 规范。

## [Unreleased]

## [0.2.0] - 2026-05-25

### Added
- 第二个开源算例 `FP_2D_TCSAW/` —— 温度补偿型 SAW(TC-SAW)二维**有限器件**模型
  - 21 周期多指 IDT,约 48 700 节点
  - LiNbO₃ 衬底 + SiO₂ / Si₃N₄ 温补层 + Al 叉指电极
  - Q9 单元、悬浮电势端部边界、复坐标拉伸 PML
  - 单进程序列扫频,跑通命令 `matlab -batch "SolveSAW"`

## [0.1.0] - 2026-05-24

### Added
- 首个开源算例 `2DTCSAW/` —— 温度补偿型 SAW (TC-SAW) 二维周期单元 demo
  - LiNbO₃ 衬底 + SiO₂ / Si₃N₄ 温补层 + Al 叉指电极
  - Q9 单元、Bloch 周期边界、复坐标拉伸 PML
  - 单进程序列扫频,跑通命令 `matlab -batch "SolveSAW"`
- MIT 许可证(`LICENSE`,© 2026 Shaoqing Duan)
- 项目主 README(英文)+ `README.zh-CN.md`(中文)
- 中英双语 demo README(`2DTCSAW/README.md`)

### Notes
- 仓库性质由"纯展示文档"扩展为"展示 + 可运行代码 demo"

[Unreleased]: https://github.com/Duane245/SAW-FEM-MATLAB/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/Duane245/SAW-FEM-MATLAB/releases/tag/v0.2.0
[0.1.0]: https://github.com/Duane245/SAW-FEM-MATLAB/releases/tag/v0.1.0
