# monitoring

This contains the monitoring GUI apps for the SHMS Calorimeter and Preshower. These can be run by:
```
./run_shms_cal_gui.csh
```
or 
```
./run_shms_pcal_gui.csh
```
to get the calorimeter or pre-shower calorimeter GUIs, respectively. The codes themselves parse the output of the call:
```
getscalers hcvme04
```
and map the channels to the GUI. The code requires a working version of python with ROOT, but the csh files set up the appropriate environment on the machiens in the counting house. The GUI updates every second with new scaler information. 