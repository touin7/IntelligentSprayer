function [retValue] = drawGraph(inputMatrix)

figure
subplot(2,1,1)
title("Pillow Edge 4 Data")
hold on
plot(inputMatrix(:,1),inputMatrix(:,3))
plot(inputMatrix(:,1),inputMatrix(:,4))
ylim([20 115])
xlabel("time [s]")
ylabel("positions [cm]")
legend("Ultrasound","ToF")
hold off

subplot(2,1,2)
title("Markers")
hold on
plot(inputMatrix(:,1),inputMatrix(:,7))
plot(inputMatrix(:,1),inputMatrix(:,9))
plot(inputMatrix(:,1),inputMatrix(:,11))
plot(inputMatrix(:,1),inputMatrix(:,13))
plot(inputMatrix(:,1),inputMatrix(:,15))
plot(inputMatrix(:,1),inputMatrix(:,17))
xlabel("time [s]")
ylabel("positions [m]")
legend("ID0","ID1","ID2","ID3","ID4","ID5")
ylim([0.20 0.55])
hold off

retValue = 0;
end