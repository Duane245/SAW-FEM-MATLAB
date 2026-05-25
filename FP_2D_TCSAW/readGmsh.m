%% 网格预处理
nodeCoordinates = msh.POS(:,1:2) * 1e-6;

elementNodes = msh.QUADS9(:,1:9);
elementNodes1 = [elementNodes(:,1) elementNodes(:,5) elementNodes(:,2) elementNodes(:,6)...
    elementNodes(:,3) elementNodes(:,7) elementNodes(:,4) elementNodes(:,8)];

numberNodes = msh.nbNod;
numberElements = size(elementNodes,1);

material_type(1).indx = find(msh.QUADS9(:,10) == 2)';
material_type(2).indx = find(msh.QUADS9(:,10) == 1)';
material_type(3).indx = find(msh.QUADS9(:,10) == 13)';
material_type(4).indx = find(msh.QUADS9(:,10) == 14)';

[gamma1_2,gamma1_zheng,gamma1_fu,gamma1_XFL,gamma1_XFR] = findSAWBoundary2DF(msh);
