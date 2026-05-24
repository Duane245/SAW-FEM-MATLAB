function force = forces(GDof,A,Boundary,V)
%UNTITLED 此处显示有关此函数的摘要
%   此处显示详细说明

active = setdiff((1:GDof)', [Boundary.electric.zheng;Boundary.electric.fu]);
j = ones(size(active));
v = - A(active,Boundary.electric.zheng)*(V*ones(size(Boundary.electric.zheng)));

force = sparse(active',j',v',GDof,1);
% force(active) = force(active) - A(active,gamma1_zheng+GDofu)*(V*ones(size(gamma1_zheng)));
end

