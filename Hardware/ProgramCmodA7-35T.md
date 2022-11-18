# How to Program the Cmod A7-35T

## Preparations
In this project, the following materials are needed
- Vivado 2018.2
- Cmod A7-35T board
- USB A to micro B cable

## Steps to program the board
### 1. Create Vivado project
- open vivado, `create project` and click `next`
- input project name `CmodA7_35T_DIO`and location, click `next`
- `RTL Project` => `next`
- in `Add Sources`, click `Add files` and select `CmodA735T_DIO.vhd`,
  `CmodA735T_DIO.dcp` and `clk_wiz_0.xci` => `next`
- in `Add Constraints`, select `Add files` and select `CmodA735T_DIO.xdc`, click `Next`
- in `Default Parts`, search and select `xc7a35tcpg236-1` => `Next` => `Finish`.
- In `Source => Design Sources => CmodA735T_DIO`, there is an red lock sign on
 `MCM0:clk)wiz_0(clk_wiz_0.xci)`, select it, in `source file properties => IP`, click 
 `Upgrade Version`, choose `Convert IP to Core Container and Set as Default in Project` 
  and click `OK`. When the red lock sign disappears, it ready to continue.

### 2. Generate Bitstream file
- `Run Synthesis`. When finished, `Run Implementation`.
- After `Run Implementation` is finished, `Open Implemented Design`, click `Settings` in in `Flow Navigator`.
- In `BitStream` => check on the box of `-bin_file`; click `Configure additional bitstream settings` on the top,
  `Enable Bitstream Compression` change to `TURE`, then press `OK` and `OK`.
- Run `Generate Bitstream` in `Flow Navigator`.
- After finished, you can choose `Generate memory configuration file`.

### 3. Generate memory configuration file 
- Or you can go to `Tool` => `Generate memory configuration file`
- Change settings as follows:
  - Format: 'MSC' 
  - Memory part: 'mx25l3233f' 
    - information can be found online for the board;
    - if set wrong, the error message should report the 
      correct part number, then do it again. 
    - The memory part number of my Cmod A7-35T board was 
      found to be [mx25l3233f] in the reference manual. 
- Filename: select directory and write the filename to save, for example: boot.mcs 
- check `Load bitstream file`
- Bitfile: select the `.bit` file exported or the default location is 
  `Project_PATH/Project_NAME.runs/impl_1/CmodA735T_Demo.bit`.
- Check the boxes of `Overwrite`, 

### 4. Program the device.
- In `Flow Navigator => Program and Debug => Open Hardware Manager`, connect the device with cable 
  and `Open target`.
- in `Hardware`, right click `xc7a35t_0` and `Add configuration memory device`, search and select 
  `mx25l3233f`.
- right click the newly addned item names `mx25l3233f-xxxxxx`, and `Program Configuration Memory Device`
  - `Configuration file`, select the `boot.mcs` in the directory exported in the last step.
  - Click `OK`
- click `Program Device`, and program the Cmod A7-35T with the bit generated.

Now, the Cmod A7-35T is ready to be plugged on the IOC server as an digital output device.

## Reference and resources
- [Cmod A7-35T Demo Project](https://forum.digilent.com/topic/2866-cmod-a7-35t-demo-project/)
- [7 Series FPGAs and Zynq-7000 SoC XADC Dual 12-Bit 1 MSPS Analog-to-Digital Converter User Guide](https://docs.xilinx.com/r/en-US/ug480_7Series_XADC/7-Series-FPGAs-and-Zynq-7000-SoC-XADC-Dual-12-Bit-1-MSPS-Analog-to-Digital-Converter-User-Guide-UG480)
- [Cmod A7 Reference Manual](https://digilent.com/reference/_media/cmod_a7/cmod_a7_rm.pdf?_ga=2.9108277.12391635.1668662559-346125063.1666201229)