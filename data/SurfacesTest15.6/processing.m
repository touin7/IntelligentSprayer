%%
flatSurfaceLine = FlatSurfLine{:,:};
save("FlatSurfaceLineData","flatSurfaceLine")


%%
clear all
clc

load("FlatSurfaceLineData.mat")

%%
figure
subplot(2,1,1)
title("FlatSurfaceData")
hold on
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,3))
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,4))
ylim([25 40])
xlabel("time [s]")
ylabel("positions [cm]")
legend("Ultrasound","ToF")
hold off

subplot(2,1,2)
title("Markers")
hold on
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,7))
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,9))
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,11))
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,13))
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,15))
xlabel("time [s]")
ylabel("positions [m]")
legend("ID0","ID1","ID2","ID3","ID4")
ylim([0.25 0.35])
hold off

%%
ultrasound = flatSurfaceLine(:,3);
laserToF = flatSurfaceLine(:,4);

avrUltrasound = mean(ultrasound);
avrLaserToF = mean(laserToF);

avrMarker = mean(flatSurfaceLine(1:200,11))*100;

correctionCoefUltrasound = avrMarker - avrUltrasound;
correctionCoefLaser = avrMarker - avrLaserToF;

figure
title("FlatSurfaceData with Correction")
hold on
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,3) + correctionCoefUltrasound)
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,4) + correctionCoefLaser)
plot(flatSurfaceLine(:,1),flatSurfaceLine(:,11) * 100)
ylim([25 40])
xlabel("time [s]")
ylabel("positions [cm]")
legend("Ultrasound","ToF","Marker")
hold off

%% Pillow edge 0 deg 1 try
edgePill = pillowEdge{:,:};
save("PillowEdgeData.mat","edgePill")

%%
clear all
clc

load("PillowEdgeData.mat")

%%
drawGraph(edgePill);

%% Pillow edge 0 deg 2 try
edgePill2 = pillowEdge2{:,:};
save("PillowEdge2Data.mat","edgePill2")

%%
clear all
clc

load("PillowEdge2Data.mat")

%%
drawGraph(edgePill2);

%% Pillow edge approx 15 deg 1 try
edgePill3 = pillowEdge3{:,:};
save("PillowEdge3Data.mat","edgePill3")

%%
clear all
clc

load("PillowEdge3Data.mat")

%%
drawGraph(edgePill3);

%% Pillow edge approx 15 deg 2 try
edgePill4 = pillowEdge4{:,:};
save("PillowEdge4Data.mat","edgePill4")

%%
clear all
clc

load("PillowEdge4Data.mat")

%%
drawGraph(edgePill4);

