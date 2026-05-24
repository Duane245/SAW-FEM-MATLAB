% ================================================================
% 2D TCSAW Demo — 周期单元 (SP) 频域扫频求解
%   - 物理:温度补偿型声表面波(TC-SAW),LiNbO3 衬底
%          + SiO2 / Si3N4 补偿层 + Al 叉指电极
%   - 单元:9 节点四边形 (Q9),平面分析
%   - 边界:左右 Bloch 周期、底部 PML(复坐标拉伸吸收)
%   - 输出:Y11 导纳曲线 + 位移场 / 电势场
% ================================================================
clear; close all

%% 路径设置(相对当前脚本所在目录)
here = fileparts(mfilename('fullpath'));
addpath(fullfile(here,'codes'), fullfile(here,'mesh'));

%% 频率扫描范围
fre = 16e8 : 0.02e8 : 20e8;

%% 材料参数(密度、刚度、压电、介电)
initial_material_parameters;

%% 网格生成(Gmsh 脚本生成的 MATLAB 网格)
SAW_PeriodBC1_TC;
readGmsh;

%% 自由度排列 [u | phi];平面分析每节点 2 位移 + 1 电势
GDofu  = 2*numberNodes;
GDoffi =   numberNodes;
GDof   = 3*numberNodes;

%% 边界索引(力学固定 / 周期、电学信号 / 接地 / 周期)
Boundary = boundary_idx_2DS(gamma1_2, gamma1_L, gamma1_R, ...
    gamma1_zheng, gamma1_fu, nodeCoordinates, numberNodes, GDofu);

%% PML 初始化(复坐标拉伸吸收边界)
pitch = 1.9936e-6;
pml = initialPML(nodeCoordinates, gamma1_2, pitch, msh, material_type);

%% 网格可视化
plot_Gmsh2D(msh, nodeCoordinates);

%% 全局 K / M 组装(循环外只组装一次)
AssemblyKM2D;

%% 扫频前的约束自由度(固定 + 周期右侧 + 电极信号 / 接地)
prescribedDof = [Boundary.machine.fix;
                 Boundary.machine.period_R;
                 Boundary.electric.period_R;
                 Boundary.electric.zheng;
                 Boundary.electric.fu];

%% 频域扫频
V    = 0.1;
nf   = numel(fre);
Q    = zeros(1, nf);
Y    = zeros(1, nf);
fprintf('频点数:%d,扫频区间:%.2f – %.2f GHz\n', nf, fre(1)*1e-9, fre(end)*1e-9);
tic
for k = 1:nf
    f     = fre(k);
    omega = 2*pi*f;

    % 时谐动态矩阵
    A = -omega^2*mass + stiffness;
    A = boundaryPeriodic2D(A, GDof, Boundary);

    % 外力(由信号电极电压激励)
    force = forces(GDof, A, Boundary, V);

    % 求解
    displacements = solution(GDof, prescribedDof, A, force);

    % 周期 / 电极自由度回填
    displacements(Boundary.machine.period_R)  = displacements(Boundary.machine.period_L);
    displacements(Boundary.electric.period_R) = displacements(Boundary.electric.period_L);
    displacements(Boundary.electric.zheng)    = V;
    displacements(Boundary.electric.fu)       = 0;

    % 由信号电极感应电荷计算 Y11
    Q(k) = sum(stiffness(Boundary.electric.zheng, :)*displacements);
    Y(k) = abs(1i*omega*Q(k)/V);
end
fprintf('扫频耗时:%.2f s\n', toc);

%% 取最后一次频点的解作为可视化样本
plot_displacements_field2D(displacements, nodeCoordinates, numberNodes, msh);
plot_phi_field2D       (displacements, nodeCoordinates, numberNodes, msh);

%% 导纳曲线
plotY11(fre, Y);

%% 结果保存
save('Y11.mat', 'Q', 'Y', 'fre');
fprintf('已保存 Y11.mat\n');
