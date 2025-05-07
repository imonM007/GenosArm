clc
clear all
close all

%length of the arm parts in milimeter
L1 = 1000;
L2 = 2500;
L3 = 2500;
L4 = 1000;
L5 = L2 + L3;

%co-ordinates of the targeted object in milimeter
X= 49;
Y= 340;
Z= 398;

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
if (D3 > L2+L3) || (L2 > D3+L3) || (L3 > D3+L2)
    disp('Object is out of range.')
else
    phi5 = acosd((D2^2 + D3^2 - L4^2)/(2*D2*D3));
    phi6 = acosd((D3^2 + L2^2 - L3^2)/(2*L2*D3));
    phi7 = acosd((L2^2 + L3^2 - D3^2)/(2*L2*L3));
    phi8 = 180 - phi6 - phi7;
    J2_theta = 180 - phi3 - phi5 - phi6 
    %revolution of joint 2 from z-axis on XZ plane
    
    J3_theta = phi7 
    %revolution of joint 3 from z-axis on XZ plane

    J4_theta = phi8 + 180 - phi3 - phi5
    %revolution of joint 4 from z-axis is always 180 degree
end