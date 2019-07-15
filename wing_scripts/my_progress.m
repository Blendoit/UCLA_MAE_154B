%wing shear flow
clear all;
close all;

Vx = 1; Vz = 1; My = 1;  %test loads will be applied individually


%Ixz = -Ixz;

%define webs

%% web cell 1

%upper webs
numStringers = numTopStringers;
stringerGap = upperStringerGap;
webThickness = t_upper;
tempStringers = topStringers;

for i=1:(numStringers+1)
    web(i).xStart = sparCaps(1).posX + stringerGap*(i-1);
    web(i).xEnd = sparCaps(1).posX + stringerGap*(i);
    web(i).thickness = webThickness;
    web(i).zStart = get_z(web(i).xStart/chord,1)*chord;
    web(i).zEnd = get_z(web(i).xEnd/chord,1)*chord;
    if i==1
        web(i).dp_area = sparCaps(1).area;
        web(i).dP_X = 0;
        web(i).dP_Z = 0;
        web(i).qPrime_X = 0;
        web(i).qPrime_Z = 0;
    else
        web(i).dp_area = tempStringers(i-1).area;
        dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;
        web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);  %just Vx
        web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);  %just Vz
        web(i).qPrime_X = web(i-1).qPrime_X - web(i).dP_X;
        web(i).qPrime_Z = web(i-1).qPrime_Z - web(i).dP_Z;
    end
    tempInt = get_int(web(i).xStart/chord,web(i).xEnd/chord,1)*chord^2;  %integral of airfoil function
    triangle1 = abs( (web(i).xStart - sparCaps(1).posX)*web(i).zStart/2);
    triangle2 = abs((web(i).xEnd - sparCaps(1).posX)*web(i).zEnd/2);
    web(i).Area = tempInt + triangle1 - triangle2;
    web(i).ds = get_ds(web(i).xStart/chord,web(i).xEnd/chord,1)*chord;
    web(i).dS_over_t = web(i).ds / web(i).thickness;

    web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
    web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
    web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
    web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
    web(i).qp_dx_X = web(i).qPrime_X *(web(i).xEnd-web(i).xStart);
    web(i).qp_dx_Z = web(i).qPrime_Z *(web(i).xEnd-web(i).xStart);
    web(i).qp_dz_X = web(i).qPrime_X *(web(i).zEnd-web(i).zStart);
    web(i).qp_dz_Z = web(i).qPrime_Z *(web(i).zEnd-web(i).zStart);
end
webTop = web;
web = [];

%rear spar
i=1;
web(i).xStart = sparCaps(3).posX;
web(i).xEnd = sparCaps(4).posX;
web(i).thickness = t_rearSpar;
web(i).zStart = sparCaps(3).posZ;
web(i).zEnd = sparCaps(4).posZ;
web(i).dp_area = sparCaps(3).area;
dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;
web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);
web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);
web(i).qPrime_X = webTop(numTopStringers+1).qPrime_X - web(i).dP_X;
web(i).qPrime_Z = webTop(numTopStringers+1).qPrime_Z - web(i).dP_Z;

web(i).Area = (sparCaps(3).posX-sparCaps(1).posX)*sparCaps(3).posZ/2 + ...
    abs((sparCaps(3).posX-sparCaps(1).posX)*sparCaps(4).posZ/2);
web(i).ds = abs(sparCaps(3).posZ - sparCaps(4).posZ);
web(i).dS_over_t = web(i).ds / web(i).thickness;

web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
web(i).qp_dx_X = web(i).qPrime_X *(web(i).xEnd-web(i).xStart);
web(i).qp_dx_Z = web(i).qPrime_Z *(web(i).xEnd-web(i).xStart);
web(i).qp_dz_X = web(i).qPrime_X *(web(i).zEnd-web(i).zStart);
web(i).qp_dz_Z = web(i).qPrime_Z *(web(i).zEnd-web(i).zStart);

webRearSpar = web;
web = [];


%lower webs
numStringers = numBottomStringers;
stringerGap = lowerStringerGap;
webThickness = t_lower;
tempStringers = bottomStringers;

for i=1:(numStringers+1)
    web(i).xStart = sparCaps(4).posX - stringerGap*(i-1);
    web(i).xEnd = sparCaps(4).posX - stringerGap*(i);
    web(i).thickness = webThickness;
    web(i).zStart = get_z(web(i).xStart/chord,0)*chord;
    web(i).zEnd = get_z(web(i).xEnd/chord,0)*chord;
    dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;
    if i==1
        web(i).dp_area = sparCaps(4).area;
        web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);
        web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);
        web(i).qPrime_X = webRearSpar.qPrime_X - web(i).dP_X;
        web(i).qPrime_Z = webRearSpar.qPrime_Z - web(i).dP_Z;
    else
        web(i).dp_area = tempStringers(i-1).area;
        web(i).dP_X = get_dp(dx,dz, Vx,0,Ix,Iz,Ixz,web(i).dp_area);
        web(i).dP_Z = get_dp(dx,dz, 0,Vz,Ix,Iz,Ixz,web(i).dp_area);
        web(i).qPrime_X = web(i-1).qPrime_X - web(i).dP_X;
        web(i).qPrime_Z = web(i-1).qPrime_Z - web(i).dP_Z;
    end

    tempInt = get_int(web(i).xEnd/chord,web(i).xStart/chord,0)*chord^2;  %integral of airfoil function
    triangle2 = abs((web(i).xStart - sparCaps(1).posX)*web(i).zStart/2);
    triangle1 = abs((web(i).xEnd - sparCaps(1).posX)*web(i).zEnd/2);
    web(i).Area = tempInt + triangle1 - triangle2;
    web(i).ds = get_ds(web(i).xStart/chord,web(i).xEnd/chord,0)*chord;
    web(i).dS_over_t = web(i).ds / web(i).thickness;

    web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
    web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
    web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
    web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
    web(i).qp_dx_X = web(i).qPrime_X*(web(i).xEnd-web(i).xStart);
    web(i).qp_dx_Z = web(i).qPrime_Z*(web(i).xEnd-web(i).xStart);
    web(i).qp_dz_X = web(i).qPrime_X*(web(i).zEnd-web(i).zStart);
    web(i).qp_dz_Z = web(i).qPrime_Z*(web(i).zEnd-web(i).zStart);

    %web(i).radCurv = ...   Example:  get_curve(web(i).xStart,web(i).xEnd,1)
end
webBottom = web;
web = [];

%front Spar
i=1;
web(i).xStart = sparCaps(2).posX;
web(i).xEnd = sparCaps(1).posX;
web(i).thickness = t_frontSpar;
web(i).zStart = sparCaps(2).posZ;
web(i).zEnd = sparCaps(1).posZ;
web(i).dp_area = sparCaps(2).area;
dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;
web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);
web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);
web(i).qPrime_X = webBottom(numBottomStringers+1).qPrime_X - web(i).dP_X;
web(i).qPrime_Z = webBottom(numBottomStringers+1).qPrime_Z - web(i).dP_Z;
web(i).Area = 0;
web(i).ds = abs(sparCaps(2).posZ - sparCaps(1).posZ);
web(i).dS_over_t = web(i).ds / web(i).thickness;

web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
web(i).qp_dx_X = web(i).qPrime_X *(web(i).xEnd-web(i).xStart);
web(i).qp_dx_Z = web(i).qPrime_Z *(web(i).xEnd-web(i).xStart);
web(i).qp_dz_X = web(i).qPrime_X *(web(i).zEnd-web(i).zStart);
web(i).qp_dz_Z = web(i).qPrime_Z *(web(i).zEnd-web(i).zStart);

webFrontSpar = web;
web = [];




%% web cell 2

%lower nose webs
numStringers = numNoseBottomStringers;
stringerGap = lowerNoseStringerGap;
webThickness = t_lower_front;
tempStringers = noseBottomStringers;

for i=1:(numStringers+1)
    web(i).xStart = sparCaps(2).posX - stringerGap*(i-1);
    web(i).xEnd = sparCaps(2).posX - stringerGap*(i);
    web(i).thickness = webThickness;
    web(i).zStart = get_z(web(i).xStart/chord,0)*chord;
    web(i).zEnd = get_z(web(i).xEnd/chord,0)*chord;
    dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;

    if i==1
        web(i).dp_area = sparCaps(2).area;
        web(i).dP_X = 0;
        web(i).dP_Z = 0;
        web(i).qPrime_X = 0;
        web(i).qPrime_Z = 0;
    else
        web(i).dp_area = tempStringers(i-1).area;
        web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);
        web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);
        web(i).qPrime_X = web(i-1).qPrime_X - web(i).dP_X;
        web(i).qPrime_Z = web(i-1).qPrime_Z - web(i).dP_Z;
    end
    tempInt = get_int(web(i).xEnd/chord,web(i).xStart/chord,0)*chord^2;  %integral of airfoil function
    triangle1 = abs((web(i).xStart - sparCaps(2).posX)*web(i).zStart/2);
    triangle2 = abs((web(i).xEnd - sparCaps(2).posX)*web(i).zEnd/2);
    web(i).Area = tempInt + triangle1 - triangle2;
    web(i).ds = get_ds(web(i).xStart/chord,web(i).xEnd/chord,0)*chord;
    web(i).dS_over_t = web(i).ds / web(i).thickness;

    web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
    web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
    web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
    web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
    web(i).qp_dx_X = web(i).qPrime_X *(web(i).xEnd-web(i).xStart);
    web(i).qp_dx_Z = web(i).qPrime_Z *(web(i).xEnd-web(i).xStart);
    web(i).qp_dz_X = web(i).qPrime_X *(web(i).zEnd-web(i).zStart);
    web(i).qp_dz_Z = web(i).qPrime_Z *(web(i).zEnd-web(i).zStart);

    %web(i).radCurv = ...   Example:  get_curve(web(i).xStart,web(i).xEnd,1)
end
webLowerNose = web;
web = [];

%upper nose webs
numStringers = numNoseTopStringers;
stringerGap = upperNoseStringerGap;
webThickness = t_upper_front;
tempStringers = noseTopStringers;

for i=1:(numStringers+1)
    web(i).xStart = stringerGap*(i-1);
    web(i).xEnd = stringerGap*(i);
    web(i).thickness = webThickness;
    web(i).zStart = get_z(web(i).xStart/chord,1)*chord;
    web(i).zEnd = get_z(web(i).xEnd/chord,1)*chord;
    dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;
    if i==1
        web(i).dp_area = 0;
        web(i).dP_X = 0;
        web(i).dP_Z = 0;
        web(i).qPrime_X = webLowerNose(numNoseBottomStringers+1).qPrime_X - web(i).dP_X;
        web(i).qPrime_Z = webLowerNose(numNoseBottomStringers+1).qPrime_Z - web(i).dP_Z;
    else
        web(i).dp_area = tempStringers(i-1).area;
        web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);
        web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);
        web(i).qPrime_X = web(i-1).qPrime_X - web(i).dP_X;
        web(i).qPrime_Z = web(i-1).qPrime_Z - web(i).dP_Z;
    end
    tempInt = get_int(web(i).xStart/chord,web(i).xEnd/chord,1)*chord^2;  %integral of airfoil function
    triangle2 = abs((web(i).xStart - sparCaps(2).posX)*web(i).zStart/2);
    triangle1 = abs((web(i).xEnd - sparCaps(2).posX)*web(i).zEnd/2);
    web(i).Area = tempInt + triangle1 - triangle2;
    web(i).ds = get_ds(web(i).xStart/chord,web(i).xEnd/chord,1)*chord;
    web(i).dS_over_t = web(i).ds / web(i).thickness;

    web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
    web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
    web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
    web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
    web(i).qp_dx_X = web(i).qPrime_X *(web(i).xEnd-web(i).xStart);
    web(i).qp_dx_Z = web(i).qPrime_Z *(web(i).xEnd-web(i).xStart);
    web(i).qp_dz_X = web(i).qPrime_X *(web(i).zEnd-web(i).zStart);
    web(i).qp_dz_Z = web(i).qPrime_Z *(web(i).zEnd-web(i).zStart);

end
webUpperNose = web;
web = [];


%front Spar
i=1;
web(i).xStart = sparCaps(1).posX;
web(i).xEnd = sparCaps(2).posX;
web(i).thickness = t_frontSpar;
web(i).zStart = sparCaps(1).posZ;
web(i).zEnd = sparCaps(2).posZ;
web(i).dp_area = sparCaps(1).area;
dx = web(i).xStart-centroid.posX; dz = web(i).zStart-centroid.posZ;

web(i).dP_X = get_dp(dx,dz,Vx,0,Ix,Iz,Ixz,web(i).dp_area);
web(i).dP_Z = get_dp(dx,dz,0,Vz,Ix,Iz,Ixz,web(i).dp_area);
web(i).qPrime_X = webUpperNose(numNoseTopStringers+1).qPrime_X - web(i).dP_X;
web(i).qPrime_Z = webUpperNose(numNoseTopStringers+1).qPrime_Z - web(i).dP_Z;
web(i).Area = 0;
web(i).ds = abs(sparCaps(1).posZ - sparCaps(2).posZ);
web(i).dS_over_t = web(i).ds / web(i).thickness;
web(i).q_dS_over_t_X = web(i).qPrime_X * web(i).dS_over_t;
web(i).q_dS_over_t_Z = web(i).qPrime_Z * web(i).dS_over_t;
web(i).two_A_qprime_X = 2*web(i).Area*web(i).qPrime_X;
web(i).two_A_qprime_Z = 2*web(i).Area*web(i).qPrime_Z;
web(i).qp_dx_X = web(i).qPrime_X *(web(i).xEnd-web(i).xStart);
web(i).qp_dx_Z = web(i).qPrime_Z *(web(i).xEnd-web(i).xStart);
web(i).qp_dz_X = web(i).qPrime_X *(web(i).zEnd-web(i).zStart);
web(i).qp_dz_Z = web(i).qPrime_Z *(web(i).zEnd-web(i).zStart);

webFrontSparCell2 = web;
web = [];


%check that q'*dx sums up to Vx

Fx = sum([webTop.qp_dx_X])+webRearSpar.qp_dx_X+ sum([webBottom.qp_dx_X])+webFrontSpar.qp_dx_X;  %cell 1
Fx = Fx + sum([webLowerNose.qp_dx_X])+ sum([webUpperNose.qp_dx_X]);  %cell 2
Fx
Fz = sum([webTop.qp_dz_X])+webRearSpar.qp_dz_X+ sum([webBottom.qp_dz_X])+webFrontSpar.qp_dz_X;  %cell 1
Fz = Fz + sum([webLowerNose.qp_dz_X])+ sum([webUpperNose.qp_dz_X]);  %cell 2
Fz

%check that q'*dz sums up to Vz


Fx = sum([webTop.qp_dx_Z])+webRearSpar.qp_dx_Z+ sum([webBottom.qp_dx_Z])+webFrontSpar.qp_dx_Z;  %cell 1
Fx = Fx + sum([webLowerNose.qp_dx_Z])+ sum([webUpperNose.qp_dx_Z]);  %cell 2
Fx
Fz = sum([webTop.qp_dz_Z])+webRearSpar.qp_dz_Z+ sum([webBottom.qp_dz_Z])+webFrontSpar.qp_dz_Z;  %cell 1
Fz = Fz + sum([webLowerNose.qp_dz_Z])+ sum([webUpperNose.qp_dz_Z]);  %cell 2
Fz

%%

% sum up the ds/t and  q*ds/t to solve 2 equations, 2 unknowns

% [A]*[q1s q2s] = B

A11 = sum([webTop.dS_over_t])+webRearSpar.dS_over_t+ sum([webBottom.dS_over_t])+webFrontSpar.dS_over_t;
A22 = sum([webLowerNose.dS_over_t])+ sum([webUpperNose.dS_over_t])+webFrontSparCell2.dS_over_t;
A12 = -webFrontSpar.dS_over_t;
A21 = -webFrontSparCell2.dS_over_t;

B1_X = sum([webTop.q_dS_over_t_X])+webRearSpar.q_dS_over_t_X+ sum([webBottom.q_dS_over_t_X])+webFrontSpar.q_dS_over_t_X;
B2_X = sum([webLowerNose.q_dS_over_t_X])+ sum([webUpperNose.q_dS_over_t_X])+webFrontSparCell2.q_dS_over_t_X;
B1_Z = sum([webTop.q_dS_over_t_Z])+webRearSpar.q_dS_over_t_Z+ sum([webBottom.q_dS_over_t_Z])+webFrontSpar.q_dS_over_t_Z;
B2_Z = sum([webLowerNose.q_dS_over_t_Z])+ sum([webUpperNose.q_dS_over_t_Z])+webFrontSparCell2.q_dS_over_t_Z;

Amat = [A11 A12; A21 A22];
Bmat_X = -[B1_X;B2_X];
Bmat_Z = -[B1_Z;B2_Z];

qs_X = inv(Amat)*Bmat_X;
qs_Z = inv(Amat)*Bmat_Z;



sum_2_a_q_X = sum([webTop.two_A_qprime_X])+webRearSpar.two_A_qprime_X+ sum([webBottom.two_A_qprime_X]);  %cell 1 qprimes
sum_2_a_q_X = sum_2_a_q_X + sum([webLowerNose.two_A_qprime_X])+ sum([webUpperNose.two_A_qprime_X]);   %cell 2 qprimes
sum_2_a_q_X = sum_2_a_q_X +  2*qs_X(1)*(sum([webTop.Area])+webRearSpar.Area+ sum([webBottom.Area]));
sum_2_a_q_X = sum_2_a_q_X +  2*qs_X(2)*(sum([webLowerNose.Area])+ sum([webUpperNose.Area]));

sum_2_a_q_Z = sum([webTop.two_A_qprime_Z])+webRearSpar.two_A_qprime_Z+ sum([webBottom.two_A_qprime_Z]);  %cell 1 qprimes
sum_2_a_q_Z = sum_2_a_q_Z + sum([webLowerNose.two_A_qprime_Z])+ sum([webUpperNose.two_A_qprime_Z]);   %cell 2 qprimes
sum_2_a_q_Z = sum_2_a_q_Z +  2*qs_Z(1)*(sum([webTop.Area])+webRearSpar.Area+ sum([webBottom.Area]));
sum_2_a_q_Z = sum_2_a_q_Z +  2*qs_Z(2)*(sum([webLowerNose.Area])+ sum([webUpperNose.Area]));

%shear center
sc.posX =  sum_2_a_q_Z / Vz + frontSpar*chord;
sc.posZ = - sum_2_a_q_X / Vx;


% now consider the torque representing shifting the load from the quarter
% chord to the SC  (need to check signs on these moments)

torque_Z = Vz*(sc.posX - 0.25*chord);
torque_X = -Vx*sc.posZ;


Area1 = sum([webTop.Area]) + webRearSpar.Area + sum([webBottom.Area]);
%check area
Area1_check = get_int(frontSpar,backSpar,1)*chord^2 + get_int(frontSpar,backSpar,0)*chord^2;

Area2 = sum([webLowerNose.Area]) + sum([webUpperNose.Area]);
Area2_check = get_int(0,frontSpar,1)*chord^2 + get_int(0,frontSpar,0)*chord^2;


%for twist equation  (see excel spreadsheet example)

q1t_over_q2t = (A22/Area2 + webFrontSpar.dS_over_t/Area1)/(A11/Area1 + webFrontSpar.dS_over_t/Area2);

q2t = torque_X/(2*Area1*q1t_over_q2t + 2*Area2);
q1t = q2t*q1t_over_q2t;
qt_X = [q1t;q2t];

q2t = torque_Z/(2*Area1*q1t_over_q2t + 2*Area2);
q1t = q2t*q1t_over_q2t;
qt_Z = [q1t;q2t];



% --- - add up all shear flows:  qtot = (qPrime + qs) + qt




%--- insert force balance to check total shear flows ---

% --- --


%end

sc


%plotting airfoil cross-section

xChord = 0:.01:1;
xChord = xChord*chord;
upperSurface = zeros(1,length(xChord));
lowerSurface = zeros(1,length(xChord));

for i=1:length(xChord)
    upperSurface(i) = get_z(xChord(i)/chord,1)*chord;
    lowerSurface(i) = get_z(xChord(i)/chord,0)*chord;
end

figure; hold on; axis equal; grid on;
%plot(xChord,z_camber,'-')
plot(xChord,upperSurface,'-k','linewidth',2)
plot(xChord,lowerSurface,'-k','linewidth',2)
plot([0 1],[0 0],'--k','linewidth',1)


for i = 1:length(webTop)
   vecX = [frontSpar*chord webTop(i).xStart webTop(i).xEnd];
   vecZ = [0 webTop(i).zStart webTop(i).zEnd];
   fill(vecX,vecZ,[0.9 0.9 0.9])
end

for i = 1:length(webBottom)
   vecX = [frontSpar*chord webBottom(i).xStart webBottom(i).xEnd];
   vecZ = [0 webBottom(i).zStart webBottom(i).zEnd];
   fill(vecX,vecZ,[0.9 0.9 0.9])
end

for i = 1:length(webUpperNose)
   vecX = [frontSpar*chord webUpperNose(i).xStart webUpperNose(i).xEnd];
   vecZ = [0 webUpperNose(i).zStart webUpperNose(i).zEnd];
   fill(vecX,vecZ,[0.7 0.9 1.0])
end

for i = 1:length(webLowerNose)
   vecX = [frontSpar*chord webLowerNose(i).xStart webLowerNose(i).xEnd];
   vecZ = [0 webLowerNose(i).zStart webLowerNose(i).zEnd];
   fill(vecX,vecZ,[0.7 0.9 1.0])
end

   vecX = [frontSpar*chord sparCaps(3).posX sparCaps(4).posX];
   vecZ = [0 sparCaps(3).posZ sparCaps(4).posZ];
   fill(vecX,vecZ,[0.9 0.9 0.9])


sparCapSize = 18;
stringerSize = 18;
plot([sparCaps(1).posX sparCaps(2).posX],[sparCaps(1).posZ sparCaps(2).posZ],'-k','linewidth',2)
plot([sparCaps(3).posX sparCaps(4).posX],[sparCaps(3).posZ sparCaps(4).posZ],'-k','linewidth',2)
plot([sparCaps.posX],[sparCaps.posZ],'.b','markersize',sparCapSize)
plot([topStringers.posX],[topStringers.posZ],'.r','markersize',stringerSize)
plot([bottomStringers.posX],[bottomStringers.posZ],'.r','markersize',stringerSize)
plot([noseTopStringers.posX],[noseTopStringers.posZ],'.r','markersize',stringerSize)
plot([noseBottomStringers.posX],[noseBottomStringers.posZ],'.r','markersize',stringerSize)
plot(centroid.posX,centroid.posZ,'.k','markerSize',18)
plot(sc.posX,sc.posZ,'.g','markersize',18)
