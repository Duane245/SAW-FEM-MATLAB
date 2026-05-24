function plot_displacements_field2D(displacements,nodeCoordinates,numberNodes,msh)
%PLOT_DISPLACEMENTS_FIELD 此处显示有关此函数的摘要
%   此处显示详细说明

disptotal = real(sqrt(displacements(1:numberNodes).^2+displacements(numberNodes+1:2*numberNodes).^2));
scaleFactor = 1e-8;
UX = real(displacements(1:numberNodes));
UY = real(displacements(numberNodes+1:2*numberNodes));
figure
patch('Faces',msh.QUADS9(:,1:4),'Vertices',nodeCoordinates+scaleFactor*[UX UY],'FaceVertexCData',disptotal,'FaceColor','interp');
axis equal
shading interp
box on;
% grid on;
% title(['特征频率=' num2str(omega_f(modeNumber)*1e-6) 'MHz'])
xlabel('\itx/\mu\itm')
ylabel('\ity/\mu\itm')
% colorbar
colormap(jet)
% axis off
end

