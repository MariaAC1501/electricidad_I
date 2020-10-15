clear all
close all
M=importdata('OCV(z).csv');
SOC=(M.data(:,1));
OCV=(M.data(:,2));

SOC_test = linspace(0.2,1,30); %genera 1000 puntos de SOC

for i = 1:30
    res(i)=calculos(SOC_test(i),SOC,OCV);
end

figure
hold on
plot(SOC_test,res,'+')
plot(SOC,OCV) % lo moví 
hold off



function OCV0 = calculos(z,SOC,OCV)
    tam=size(SOC);
    for i = 1:tam(1)-1
       if z>=SOC(i,1)
           OCV0=OCV(i,1)+((OCV(i+1,1)-OCV(i,1))*(z-SOC(i,1))/(SOC(i+1,1)-SOC(i,1)));               
       end
    end
end
