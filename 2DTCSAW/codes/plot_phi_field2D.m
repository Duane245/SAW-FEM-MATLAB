function plot_phi_field2D(displacements,nodeCoordinates,numberNodes,msh)
%PLOT_PHI_FIELD 此处显示有关此函数的摘要
%   此处显示详细说明

UX = real(displacements(1:numberNodes));
UY = real(displacements(numberNodes+1:2*numberNodes));

scaleFactor = 1e-8;
figure
patch('Faces',msh.QUADS9(:,1:4),'Vertices',nodeCoordinates+scaleFactor*[UX UY],...
    'FaceVertexCData',real(displacements(2*numberNodes+1:end)),'FaceColor','interp');
axis equal
shading interp
% colorbar
box on;
grid on;
colormap(jet)
end

