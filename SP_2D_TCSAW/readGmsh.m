%%
nodeCoordinates = msh.POS(:,1:2) * 1e-6;

elementNodes = msh.QUADS9(:,1:9);

numberNodes = msh.nbNod;
numberElements = size(elementNodes,1);

material_type(1).indx = find(msh.QUADS9(:,10) == 16)';
material_type(2).indx = find(msh.QUADS9(:,10) == 15)';
material_type(3).indx = find(msh.QUADS9(:,10) == 12)';
material_type(4).indx = find(msh.QUADS9(:,10) == 11)';

[gamma1_2,gamma1_L,gamma1_R,gamma1_zheng,gamma1_fu] = findSAWBoundary(msh);