%% 128°YX-LiNbO3 piezoelectric tensors
material_type(1).rho = 4628;

C_LN = [198390000000.000	66065049726.9665	53784950273.0335	7175389491.19690	0	0;
66065049726.9665	186148671479.564	80484557171.3618	5542848560.60817	0	0;
53784950273.0335	80484557171.3618	209432214177.712	6468545399.12378	0	0;
7175389491.19690	5542848560.60817	6468545399.12378	75004557171.3618	0	0;
0	0	0	0	56488437245.6910	-3684464518.66625;
0	0	0	0	-3684464518.66625	74996562754.3090];

e_LN = [0	0	0	0	4.40335738810247	0.287999501116610;
-1.75215342736883	4.56647020909682	-1.38801517685763	0.308578173488658	0	0;
1.69598300904214	-2.39879620557167	2.59557935534160	0.652137751627810	0	0];

eps0 = 8.854e-12;
eps_LN = [45.6000000000000	0	0;
0	38.6099004836340	-9.27617536580478;
0	-9.27617536580478	33.2900995163660]*eps0;
% oula Transfer  
oula = [0;0;0];
[C,e,eps] = oulaTransfer(oula,C_LN,e_LN,eps_LN);


material_type(1).C = [C(1,1) C(1,3) C(1,5);
    C(3,1) C(3,3) C(3,5); 
    C(5,1) C(5,3) C(5,5)];

material_type(1).e = [e(1,1) e(1,3) e(1,5);
    e(3,1) e(3,3) e(3,5)];

material_type(1).eps = [eps(1,1) eps(1,3);
    eps(3,1)  eps(3,3)];

%% Al
material_type(2).rho = 8960;

E_Al = 120e9;
nu_Al = 0.34;
material_type(2).C = ComputingC2D(nu_Al,E_Al);

material_type(2).e = zeros(2,3);

material_type(2).eps = [1 0;
    0 1]*eps0;
%% SiO2
material_type(3).rho = 2200;

E_Al = 70e9;
nu_Al = 0.17;
material_type(3).C = ComputingC2D(nu_Al,E_Al);

material_type(3).e = zeros(2,3);

material_type(3).eps = [4.2 0;
    0 4.2]*eps0;
%% SIN
material_type(4).rho = 3100;

E_Al = 160e9;
nu_Al = 0.23;
material_type(4).C = ComputingC2D(nu_Al,E_Al);

material_type(4).e = zeros(2,3);

material_type(4).eps = [9.7 0;
    0 9.7]*eps0;