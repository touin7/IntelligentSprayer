TestChairData = TestChair{:,:};
save('testChairMatlab',"TestChairData")

%%
clear all
clc

load("testChairMatlab.mat");

%%

figure
hold on
title("Distance Z-axis")
plot(TestChairData(:,1),TestChairData(:,3)*100)
plot(TestChairData(:,1),TestChairData(:,5))
plot(TestChairData(:,1),TestChairData(:,6))
xlabel("Time [s]")
ylabel("Distance [cm]")
legend("Marker","Ultrasound","ToF")
%ylim([0.15 0.45])
hold off

%%
TestPillow1Data = TestPillow1{:,:};
save('testPillow1Matlab',"TestPillow1Data")

%%
clear all
clc

load("TestPillow1Matlab.mat");

%%

figure
hold on
title("Distance Z-axis")
plot(TestPillow1Data(:,1),TestPillow1Data(:,3)*100)
plot(TestPillow1Data(:,1),TestPillow1Data(:,5))
plot(TestPillow1Data(:,1),TestPillow1Data(:,6))
xlabel("Time [s]")
ylabel("Distance [cm]")
legend("Marker","Ultrasound","ToF")
%ylim([0.15 0.45])
hold off

%%
TestPillow2Data = TestPillow2{:,:};
save('testPillow2Matlab',"TestPillow2Data")

%%
clear all
clc

load("TestPillow2Matlab.mat");

%%

figure
hold on
title("Distance Z-axis")
plot(TestPillow2Data(:,1),TestPillow2Data(:,3)*100)
plot(TestPillow2Data(:,1),TestPillow2Data(:,5))
plot(TestPillow2Data(:,1),TestPillow2Data(:,6))
xlabel("Time [s]")
ylabel("Distance [cm]")
legend("Marker","Ultrasound","ToF")
%ylim([0.15 0.45])
hold off
