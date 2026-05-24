function plotY11(fre,Y)
%PLOTY11 此处显示有关此函数的摘要
%   此处显示详细说明
figure;
plot(fre*1e-9,log(Y),'LineWidth',2)

box on;
set(gca,'linewidth',2,'fontsize',18)
xlim([fre(1)*1e-9 fre(end)*1e-9])

xlabel('\itf/GHz')
ylabel('Admittance/log|Y|')
end

