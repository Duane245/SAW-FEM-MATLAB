function [massuu,stiffness] = formStiffnessMass2DPML(massuu,...
    stiffnessuu,stiffnessfifi,stiffnessufi,stiffnessfiu,...
    elementNodes,numberNodes,nodeCoordinates,pml,omega)
%FORMSTIFFNESSMASS2DPML 在 PML 区把复坐标拉伸的贡献叠加到 K/M。
%   分别对 uu、phi-phi、u-phi 三块累加 PML 区贡献，再合并成全耦合矩阵。
[stiffnessuu,massuu] = formStiffnessMass2DPMLuu(stiffnessuu, massuu, ...
    elementNodes,numberNodes,nodeCoordinates,1,'Q9','third',pml,omega);

stiffnessfifi = formStiffnessMass2DPMLfi(stiffnessfifi, ...
    elementNodes,nodeCoordinates,1,'Q9','third',pml,omega);

stiffnessufi = formStiffnessMass2DPMLufi(stiffnessufi,...
    elementNodes,numberNodes,nodeCoordinates,1,'Q9','third',pml,omega);

stiffnessfiu = stiffnessufi';

scale = 6.173191780858575e-11;
stiffnessuu = stiffnessuu * scale;
stiffnessfiu = stiffnessfiu * scale;
massuu = massuu * scale;

stiffness = [stiffnessuu stiffnessufi;stiffnessfiu -stiffnessfifi];

end
