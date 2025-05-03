clc
clear all
close all

%length of the arm parts in milimeter
L1 = 150;
L2 = 250;
L3 = 250;
L4 = 100;
L5 = L2 + L3;

%co-ordinates of the targeted object in milimeter
X= 130;
Y= 220;
Z= 50;

%calculating revolution of the Base from X-axis
J1_theta = atand(Y/X)

%calculating distance in XY plane
D0 = sqrt(X^2 + Y^2);

%consider D0 as X in XZ plane
D1 = sqrt(D0^2 + Z^2);
phi1 = atand(Z/D0);
phi2 = 90 - phi1;
D2 = sqrt(L1^2 + D1^2 - 2*L1*D1*cosd(phi2));
phi3 = acosd((L1^2 +D2^2 - D1^2)/(2*L1*D2));
phi4 = 180 - phi2 - phi3;
D3 = sqrt(D2^2 + L4^2 - 2*L4*D2*cosd(phi3));
if (D3 > L5)
    disp('Object is out of range.')
else
    phi5 = acosd((D2^2 + D3^2 - L4^2)/(2*D2*D3));
    phi6 = acosd((D3^2)/(2*L2*D3));
    phi7 = (180 - (2*phi6));
    J2_theta = 180 - phi3 - phi5 - phi6 
    %revolution of joint 2 from z-axis on XZ plane
    
    phi8 = phi7 - J2_theta;
    J3_theta = 180 - phi8 
    %revolution of joint 3 from z-axis on XZ plane

    J4_theta = 180
    %revolution of joint 4 from z-axis is always 180 degree
end