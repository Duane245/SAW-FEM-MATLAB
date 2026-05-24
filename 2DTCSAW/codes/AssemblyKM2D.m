% calculation of the system stiffness matrix
[massuu,stiffnessuu,stiffnessfifi,stiffnessufi,stiffnessfiu] = formStiffnessMass2D(GDofu,GDoffi, ...
    elementNodes,numberNodes,nodeCoordinates,material_type);

omega = 2*pi*fre(end);      % !!!!!!!!!!
[mass,stiffness] = formStiffnessMass2DPML(massuu,stiffnessuu,stiffnessfifi,stiffnessufi,stiffnessfiu,...
    elementNodes,numberNodes,nodeCoordinates,pml,omega);

% mass = sparse(GDof,GDof);
% mass(1:GDofu,1:GDofu) = massuu1;