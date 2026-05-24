<div align="center">

# 2D TCSAW Demo

**温度补偿声表面波(TC-SAW)二维周期单元演示算例**

[English](README.md) · **简体中文**

![MATLAB](https://img.shields.io/badge/MATLAB-R2023a%2B-EE6B27?logo=mathworks&logoColor=white)
![Method](https://img.shields.io/badge/Method-Piezoelectric%20FEM%20%2B%20PML-555555)
![License](https://img.shields.io/badge/License-MIT-blue)

</div>

---

## 简介

本目录是一个**独立、可直接运行**的温度补偿型 SAW(TC-SAW)二维周期单元演示算例。压电衬底:LiNbO₃;补偿层:SiO₂ / Si₃N₄;电极:Al 叉指。采用 9 节点四边形(Q9)单元离散,左右施加 Bloch 周期边界、底部 PML(复坐标拉伸)吸收。频域逐频点扫频得 Y₁₁ 导纳。

---

## 跑通

```bash
cd 2DTCSAW
matlab -batch "SolveSAW"
```

或在交互式 MATLAB 中:

```matlab
cd 2DTCSAW
SolveSAW
```

**预期产出**

| 文件 / 图窗 | 内容 |
|---|---|
| `Y11.mat` | `fre`(201 频点)、`Q`、`Y` |
| Figure 1 | 网格 |
| Figure 2 | 位移场 |
| Figure 3 | 电势场 |
| Figure 4 | Y₁₁ 导纳曲线 |

201 频点扫频耗时 **≈ 4–5 分钟**(单进程,普通工作站,无需 Parallel Computing Toolbox)。

---

## 算例参数

| 项 | 值 |
|---|---|
| 压电衬底 | LiNbO₃ |
| 补偿层 | SiO₂ + Si₃N₄ |
| 电极 | Al(叉指 IDT) |
| 周期 pitch | 1.9936 µm |
| 金属化比 | 0.46 |
| 单元类型 | Q9(9 节点四边形) |
| 边界 | 左右 Bloch 周期 · 底部 PML |
| 扫频区间 | 1.60 – 2.00 GHz |
| 频点数 | 201 |

---

## 目录结构

```
2DTCSAW/
├── SolveSAW.m                          主驱动
├── initial_material_parameters.m       材料参数(LiNbO3 / Al / SiO2 / Si3N4)
├── initialPML.m                        PML 初始化(复坐标拉伸)
├── readGmsh.m                          网格读取
├── findSAWBoundary.m                   边界节点识别
├── codes/                              求解器内核
│   ├── AssemblyKM2D.m                      K/M 组装入口
│   ├── boundary_idx_2DS.m                  SP 边界索引
│   ├── boundaryPeriodic2D.m                Bloch 周期约束
│   ├── forces.m / solution.m               外力 / 线性解
│   ├── formStiffnessMass2D*.m              压电耦合块组装(uu / φφ / uφ)
│   ├── formStiffnessMass2DPML*.m           PML 区组装(复坐标拉伸)
│   ├── gaussQuadrature.m                   高斯积分
│   ├── shapeFunctionsQ2D.m                 Q9 形函数
│   ├── Jacobian.m                          雅可比工具
│   ├── oulaTransfer.m                      欧拉角旋转晶体张量
│   ├── ComputingC2D.m                      刚度张量构造
│   ├── SortLR_2d.m                         左右周期边界节点排序
│   └── plot_*.m  /  plotY11.m              可视化
└── mesh/
    ├── SAW_PeriodBC1_TC.m                  MATLAB 网格(由下方 .py 生成)
    └── SAW-PeriodBC1_TC_1.py               Gmsh 参数化几何脚本
```

---

## 依赖

- MATLAB R2023a 或更新版本
- 无任何附加 Toolbox 要求(单进程序列扫频)
- 网格 `.m` 已随仓附带;若想从 `.py` 重新生成,需 [Gmsh](https://gmsh.info) + Python

---

## 物理与方法

- **未知场** `[u₁, u₂, φ]`(位移 + 电势),压电耦合本构
- **组装** 按 `[u | φ]` 分块的全耦合 `K`、`M`
- **PML** 通过复坐标拉伸 `α = 1 + d/(iω)` 在外行波路径上引入衰减;`d` 为多项式廓线
- **扫频** 每频点求解 `(-ω²M + K) x = f`,经信号电极感应电荷 `Q` 算出 `Y₁₁ = |iωQ/V|`

---

## 引用

若本 demo 对你的工作有帮助,可以引用本仓库:

```bibtex
@software{duan2026_saw,
  author = {Shaoqing Duan},
  title  = {SAW: a piezoelectric FEM solver with TC-SAW 2D demo},
  year   = {2026},
  url    = {https://github.com/Duane245/SAW}
}
```

---

## 许可证

基于 [MIT License](../LICENSE) 发布 · Copyright © 2026 [Shaoqing Duan](https://github.com/Duane245)
