function [massuu,stiffness] = formStiffnessMass2DPML(massuu,...
    stiffnessuu,stiffnessfifi,stiffnessufi,stiffnessfiu,...
    elementNodes,numberNodes,nodeCoordinates,pml,omega,ME)
[stiffnessuu,massuu] = formStiffnessMass2DPMLuu(stiffnessuu, massuu, ...
    elementNodes,numberNodes,nodeCoordinates,1,'Q9','third',pml,omega,ME);

stiffnessfifi = formStiffnessMass2DPMLfi(stiffnessfifi, ...
    elementNodes,nodeCoordinates,1,'Q9','third',pml,omega,ME);

stiffnessufi = formStiffnessMass2DPMLufi(stiffnessufi,...
    elementNodes,numberNodes,nodeCoordinates,1,'Q9','third',pml,omega,ME);

stiffnessfiu = stiffnessufi';


scale = 6.173191780858575e-11;
stiffnessuu = stiffnessuu * scale;
stiffnessfiu = stiffnessfiu * scale;
massuu = massuu * scale;

stiffness = [stiffnessuu stiffnessufi;stiffnessfiu -stiffnessfifi];

end

