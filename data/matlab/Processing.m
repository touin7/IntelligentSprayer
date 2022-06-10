clear all
clc

load("mat0outputTes.mat");

%%

subplot(3,1,1)
hold on
title("Distance Z-axis")
plot(mat0outputTes(:,1),mat0outputTes(:,3))
plot(mat0outputTes(:,1),mat0outputTes(:,4))
xlabel("Time [s]")
ylabel("Distance [m]")
legend("Marker","Laser")
ylim([0.15 0.45])
hold off

subplot(3,1,2)
hold on
title("Speed X-axis")
plot(mat0outputTes(:,1),mat0outputTes(:,5))
plot(mat0outputTes(:,1),mat0outputTes(:,7))
xlabel("Time [s]")
ylabel("Speed [m/s]")
legend("Marker","Feature")
ylim([-0.09 0.07])
hold off

subplot(3,1,3)
hold on
title("Speed Y-axis")
plot(mat0outputTes(:,1),mat0outputTes(:,6))
plot(mat0outputTes(:,1),mat0outputTes(:,8))
xlabel("Time [s]")
ylabel("Speed [m/s]")
legend("Marker","Feature")
ylim([-0.05 0.1])
hold off

%% SIGNAL PROCESSING

time = (HandSensorAccel(:,1) - HandSensorAccel(1,1))./1000; %time in seconds
signal = HandSensorAccel(:,3);

Fs = 1/90; %111Hz
L = length(signal);

MA_coef_num = 100;
MA = ones(1,MA_coef_num)/MA_coef_num;
FilterAccel = conv(signal,MA,'same');

figure
hold on
title("Moving average filter window length 100")
plot(time,signal)
plot(time,FilterAccel)
xlabel("time [s]")
ylabel("speed [m/s]")
legend('Without filtering', 'With filtering')

%%
figure
hold on
title("Position X-axis")
plot(HandDataPC(:,1),HandDataPC(:,3))
xlabel("Time [s]")
ylabel("Position [m]")
xlim([110 220])
%ylim([-0.1 0.12])
%%
figure
hold on
title("Speed X-axis")
plot(HandDataPC(:,1),HandDataPC(:,6))
xlabel("Time [s]")
ylabel("Speed [m/s]")
xlim([110 220])
%ylim([-0.1 0.12])



%% Show speed data + moving filter

MA_coef_num = 10;
MA = ones(1,MA_coef_num)/MA_coef_num;
FilterSpeed = conv(StageDataPC(:,6),MA,'same');

indexes = 1:length(HandDataPC(:,6));

figure
hold on
title("Speed X-axis")
plot(indexes,HandDataPC(:,6))
%plot(indexes,FilterSpeed)
xlabel("Time [s]")
ylabel("Speed [m/s]")
%legend('Without filtering', 'With filtering - window length: 10')
%xlim([400 1200])
%xlim([120 190])
%ylim([-0.1 0.12])
 
%vypocitat prumery v pohybu porovnat s nastavenymi hodnotami
%do powerpointu pridat fotku setupu

%20 [444 - 653]
%30 [858 -1001]
%40 [1250-1329]
%%
startInd = 444;
endInd = 653;
resMean = mean(HandDataPC(startInd:endInd,6)*1000)
resSd = std(HandDataPC(startInd:endInd,6)*1000)