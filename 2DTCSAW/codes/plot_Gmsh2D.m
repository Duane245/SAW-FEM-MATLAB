function plot_Gmsh2D(msh,nodeCoordinates)
%PLOT_GMSH 此处显示有关此函数的摘要
%   此处显示详细说明
figure;
patch('Faces',msh.QUADS9(:,1:4),'Vertices',nodeCoordinates*1e6,'facecolor','c','Linewidth',1)
axis equal


box on;
set(gca,'linewidth',2,'fontsize',18)

xlim([min(nodeCoordinates(:,1)*1e6),max(nodeCoordinates(:,1)*1e6)])
ylim([min(nodeCoordinates(:,2)*1e6),max(nodeCoordinates(:,2)*1e6)])

title('Meshing')
xlabel('\itx/\mu\itm')
ylabel('\ity/\mu\itm')
end

