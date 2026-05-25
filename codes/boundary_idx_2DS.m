function Boundary = boundary_idx_2DS(gamma1_2,gamma1_L,gamma1_R,gamma1_zheng,gamma1_fu, ...
    nodeCoordinates,numberNodes,GDofu,ME)
%% 左右边界去掉底边界
gammal_2L =intersect(gamma1_2,gamma1_L);
gammal_2R =intersect(gamma1_2,gamma1_R);

gamma1_L = setdiff(gamma1_L, gammal_2L);
gamma1_R = setdiff(gamma1_R, gammal_2R);
%% 周期边界的序号对称排列
[gamma1_L,gamma1_R] = SortLR_2d(gamma1_L,gamma1_R,nodeCoordinates);
%% 边界条件
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 固体力学
if ME == 0
    Boundary.machine.period_L = ...
        [gamma1_L;       gamma1_L+numberNodes];

    Boundary.machine.period_R = ...
        [gamma1_R;       gamma1_R+numberNodes];

    Boundary.machine.fix = [gamma1_2; gamma1_2+numberNodes;];

    % 静电
    Boundary.electric.period_L = [gamma1_L+GDofu;   gammal_2L+GDofu];
    Boundary.electric.period_R = [gamma1_R+GDofu;   gammal_2R+GDofu];

    Boundary.electric.zheng = gamma1_zheng+GDofu;
    Boundary.electric.fu = gamma1_fu+GDofu;
else
end
end

