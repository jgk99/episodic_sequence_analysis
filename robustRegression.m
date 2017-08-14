Xss = dlmread('XssForRegression.txt',',');
Yss = dlmread('YssForRegression.txt',',');
runEpochs = dlmread('runEpochs.txt');
speeds = dlmread('speed.txt',',');
length(Xss);
funcs = zeros(length(Xss),2);
for i = 1:length(Xss)
    funcs(i,:) = robustfit(Xss(i,:),Yss(i,:))';
    
    
end

XssForPlotting = reshape(Xss,[length(Xss(1,:))*length(Xss(:,1)),1]);
YssForPlotting = reshape(Yss,[length(Yss(1,:))*length(Yss(:,1)),1]);
scatter(XssForPlotting,YssForPlotting)

hold on
for i = 1:length(runEpochs)
    x = linspace(runEpochs(i,1),runEpochs(i,2));
    y = funcs(i,1) + funcs(i,2) * x;
    plot(x, y)
end
hold off

scXss = funcs(:,2);
scYss = zeros(length(runEpochs),1);

for i = 1:length(runEpochs)
    
   scYss(i) =  median(speeds(int16(runEpochs(i,1))+1:int16(runEpochs(i,2))+1));
    
end

scatter(scXss,scYss)
hold on
tempFunc = robustfit(scXss,scYss);
x = linspace(-.05,.2);
plot(x,tempFunc(1)+tempFunc(2) *x )
corr(scXss,scYss)
