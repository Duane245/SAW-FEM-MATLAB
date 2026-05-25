function Boundary = boundary_idx_2DF(gamma1_XFL,gamma1_XFR,gamma1_2,gamma1_zheng,gamma1_fu,...
    numberNodes,GDofu,ME)

%% 边界条件
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% 固体力学
if ME == 0
    Boundary.machine.fix = [gamma1_2; gamma1_2+numberNodes;];

    % 静电
    Boundary.electric.zheng = gamma1_zheng+GDofu;
    Boundary.electric.fu = gamma1_fu+GDofu;

    Boundary.electric.XFL = gamma1_XFL+GDofu;
    Boundary.electric.XFR = gamma1_XFR+GDofu;
else
end


end

