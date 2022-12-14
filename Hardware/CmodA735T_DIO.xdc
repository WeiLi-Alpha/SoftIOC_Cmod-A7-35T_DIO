## This file is a general .xdc for the CmodA7 rev. B
## To use it in a project:
## - uncomment the lines corresponding to used pins
## - rename the used ports (in each line, after get_ports) according to the top level signal names in the project

## Clock signal 12 MHz
set_property -dict {PACKAGE_PIN L17 IOSTANDARD LVCMOS33} [get_ports sysclk]
create_clock -period 83.330 -name sys_clk_pin -waveform {0.000 41.660} -add [get_ports sysclk]


## LEDs
set_property -dict {PACKAGE_PIN A17 IOSTANDARD LVCMOS33} [get_ports {led[0]}]
set_property -dict {PACKAGE_PIN C16 IOSTANDARD LVCMOS33} [get_ports {led[1]}]

set_property -dict {PACKAGE_PIN B17 IOSTANDARD LVCMOS33} [get_ports led0_b]
set_property -dict {PACKAGE_PIN B16 IOSTANDARD LVCMOS33} [get_ports led0_g]
set_property -dict {PACKAGE_PIN C17 IOSTANDARD LVCMOS33} [get_ports led0_r]


## Buttons
set_property -dict {PACKAGE_PIN A18 IOSTANDARD LVCMOS33} [get_ports {btn[0]}]
set_property -dict {PACKAGE_PIN B18 IOSTANDARD LVCMOS33} [get_ports {btn[1]}]


## Pmod Header JA
set_property -dict {PACKAGE_PIN G17 IOSTANDARD LVCMOS33} [get_ports {ja[0]}]
set_property -dict {PACKAGE_PIN G19 IOSTANDARD LVCMOS33} [get_ports {ja[1]}]
set_property -dict {PACKAGE_PIN N18 IOSTANDARD LVCMOS33} [get_ports {ja[2]}]
set_property -dict {PACKAGE_PIN L18 IOSTANDARD LVCMOS33} [get_ports {ja[3]}]
set_property -dict {PACKAGE_PIN H17 IOSTANDARD LVCMOS33} [get_ports {ja[4]}]
set_property -dict {PACKAGE_PIN H19 IOSTANDARD LVCMOS33} [get_ports {ja[5]}]
set_property -dict {PACKAGE_PIN J19 IOSTANDARD LVCMOS33} [get_ports {ja[6]}]
set_property -dict {PACKAGE_PIN K18 IOSTANDARD LVCMOS33} [get_ports {ja[7]}]


## Analog XADC Pins
## Only declare these if you want to use pins 15 and 16 as single ended analog inputs. pin 15 -> vaux4, pin16 -> vaux12
# set_property -dict { PACKAGE_PIN G2    IOSTANDARD LVCMOS33 } [get_ports { xa_n[0] }]; #IO_L1N_T0_AD4N_35 Sch=ain_n[15]
# set_property -dict { PACKAGE_PIN G3    IOSTANDARD LVCMOS33 } [get_ports { xa_p[0] }]; #IO_L1P_T0_AD4P_35 Sch=ain_p[15]
# set_property -dict { PACKAGE_PIN J2    IOSTANDARD LVCMOS33 } [get_ports { xa_n[1] }]; #IO_L2N_T0_AD12N_35 Sch=ain_n[16]
# set_property -dict { PACKAGE_PIN H2    IOSTANDARD LVCMOS33 } [get_ports { xa_p[1] }]; #IO_L2P_T0_AD12P_35 Sch=ain_p[16]


## GPIO Pins
## Pins 15 and 16 should remain commented if using them as analog inputs
set_property -dict {PACKAGE_PIN M3 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[0]}]
set_property -dict {PACKAGE_PIN L3 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[1]}]
set_property -dict {PACKAGE_PIN A16 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[2]}]
set_property -dict {PACKAGE_PIN K3 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[3]}]
set_property -dict {PACKAGE_PIN C15 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[4]}]
set_property -dict {PACKAGE_PIN H1 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[5]}]
set_property -dict {PACKAGE_PIN A15 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[6]}]
set_property -dict {PACKAGE_PIN B15 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[7]}]
set_property -dict {PACKAGE_PIN A14 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[8]}]
set_property -dict {PACKAGE_PIN J3 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[9]}]
set_property -dict {PACKAGE_PIN J1 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[10]}]
set_property -dict {PACKAGE_PIN K2 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[11]}]
set_property -dict {PACKAGE_PIN L1 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[12]}]
set_property -dict {PACKAGE_PIN L2 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[13]}]
set_property -dict {PACKAGE_PIN M1 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[14]}]
set_property -dict {PACKAGE_PIN N3 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[15]}]
set_property -dict {PACKAGE_PIN P3 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[16]}]
set_property -dict {PACKAGE_PIN M2 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[17]}]
set_property -dict {PACKAGE_PIN N1 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[18]}]
set_property -dict {PACKAGE_PIN N2 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[19]}]
set_property -dict {PACKAGE_PIN P1 IOSTANDARD LVCMOS33} [get_ports {IOGroupA[20]}]
set_property -dict {PACKAGE_PIN R3 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[20]}]
set_property -dict {PACKAGE_PIN T3 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[19]}]
set_property -dict {PACKAGE_PIN R2 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[18]}]
set_property -dict {PACKAGE_PIN T1 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[17]}]
set_property -dict {PACKAGE_PIN T2 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[16]}]
set_property -dict {PACKAGE_PIN U1 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[15]}]
set_property -dict {PACKAGE_PIN W2 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[14]}]
set_property -dict {PACKAGE_PIN V2 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[21]}]
set_property -dict {PACKAGE_PIN W3 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[22]}]
set_property -dict {PACKAGE_PIN V3 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[13]}]
set_property -dict {PACKAGE_PIN W5 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[12]}]
set_property -dict {PACKAGE_PIN V4 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[11]}]
set_property -dict {PACKAGE_PIN U4 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[10]}]
set_property -dict {PACKAGE_PIN V5 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[9]}]
set_property -dict {PACKAGE_PIN W4 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[8]}]
set_property -dict {PACKAGE_PIN U5 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[7]}]
set_property -dict {PACKAGE_PIN U2 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[6]}]
set_property -dict {PACKAGE_PIN W6 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[5]}]
set_property -dict {PACKAGE_PIN U3 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[4]}]
set_property -dict {PACKAGE_PIN U7 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[3]}]
set_property -dict {PACKAGE_PIN W7 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[2]}]
set_property -dict {PACKAGE_PIN U8 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[1]}]
set_property -dict {PACKAGE_PIN V8 IOSTANDARD LVCMOS33} [get_ports {IOGroupB[0]}]


## UART
set_property -dict {PACKAGE_PIN J18 IOSTANDARD LVCMOS33} [get_ports uart_rxd_out]
set_property -dict {PACKAGE_PIN J17 IOSTANDARD LVCMOS33} [get_ports uart_txd_in]


## Crypto 1 Wire Interface
#set_property -dict { PACKAGE_PIN D17   IOSTANDARD LVCMOS33 } [get_ports { crypto_sda }]; #IO_0_14 Sch=crypto_sda


## QSPI
#set_property -dict { PACKAGE_PIN K19   IOSTANDARD LVCMOS33 } [get_ports { qspi_cs    }]; #IO_L6P_T0_FCS_B_14 Sch=qspi_cs
#set_property -dict { PACKAGE_PIN D18   IOSTANDARD LVCMOS33 } [get_ports { qspi_dq[0] }]; #IO_L1P_T0_D00_MOSI_14 Sch=qspi_dq[0]
#set_property -dict { PACKAGE_PIN D19   IOSTANDARD LVCMOS33 } [get_ports { qspi_dq[1] }]; #IO_L1N_T0_D01_DIN_14 Sch=qspi_dq[1]
#set_property -dict { PACKAGE_PIN G18   IOSTANDARD LVCMOS33 } [get_ports { qspi_dq[2] }]; #IO_L2P_T0_D02_14 Sch=qspi_dq[2]
#set_property -dict { PACKAGE_PIN F18   IOSTANDARD LVCMOS33 } [get_ports { qspi_dq[3] }]; #IO_L2N_T0_D03_14 Sch=qspi_dq[3]


## Cellular RAM
set_property -dict {PACKAGE_PIN M18 IOSTANDARD LVCMOS33} [get_ports {MemAdr[0]}]
set_property -dict {PACKAGE_PIN M19 IOSTANDARD LVCMOS33} [get_ports {MemAdr[1]}]
set_property -dict {PACKAGE_PIN K17 IOSTANDARD LVCMOS33} [get_ports {MemAdr[2]}]
set_property -dict {PACKAGE_PIN N17 IOSTANDARD LVCMOS33} [get_ports {MemAdr[3]}]
set_property -dict {PACKAGE_PIN P17 IOSTANDARD LVCMOS33} [get_ports {MemAdr[4]}]
set_property -dict {PACKAGE_PIN P18 IOSTANDARD LVCMOS33} [get_ports {MemAdr[5]}]
set_property -dict {PACKAGE_PIN R18 IOSTANDARD LVCMOS33} [get_ports {MemAdr[6]}]
set_property -dict {PACKAGE_PIN W19 IOSTANDARD LVCMOS33} [get_ports {MemAdr[7]}]
set_property -dict {PACKAGE_PIN U19 IOSTANDARD LVCMOS33} [get_ports {MemAdr[8]}]
set_property -dict {PACKAGE_PIN V19 IOSTANDARD LVCMOS33} [get_ports {MemAdr[9]}]
set_property -dict {PACKAGE_PIN W18 IOSTANDARD LVCMOS33} [get_ports {MemAdr[10]}]
set_property -dict {PACKAGE_PIN T17 IOSTANDARD LVCMOS33} [get_ports {MemAdr[11]}]
set_property -dict {PACKAGE_PIN T18 IOSTANDARD LVCMOS33} [get_ports {MemAdr[12]}]
set_property -dict {PACKAGE_PIN U17 IOSTANDARD LVCMOS33} [get_ports {MemAdr[13]}]
set_property -dict {PACKAGE_PIN U18 IOSTANDARD LVCMOS33} [get_ports {MemAdr[14]}]
set_property -dict {PACKAGE_PIN V16 IOSTANDARD LVCMOS33} [get_ports {MemAdr[15]}]
set_property -dict {PACKAGE_PIN W16 IOSTANDARD LVCMOS33} [get_ports {MemAdr[16]}]
set_property -dict {PACKAGE_PIN W17 IOSTANDARD LVCMOS33} [get_ports {MemAdr[17]}]
set_property -dict {PACKAGE_PIN V15 IOSTANDARD LVCMOS33} [get_ports {MemAdr[18]}]
set_property -dict {PACKAGE_PIN W15 IOSTANDARD LVCMOS33} [get_ports {MemDB[0]}]
set_property -dict {PACKAGE_PIN W13 IOSTANDARD LVCMOS33} [get_ports {MemDB[1]}]
set_property -dict {PACKAGE_PIN W14 IOSTANDARD LVCMOS33} [get_ports {MemDB[2]}]
set_property -dict {PACKAGE_PIN U15 IOSTANDARD LVCMOS33} [get_ports {MemDB[3]}]
set_property -dict {PACKAGE_PIN U16 IOSTANDARD LVCMOS33} [get_ports {MemDB[4]}]
set_property -dict {PACKAGE_PIN V13 IOSTANDARD LVCMOS33} [get_ports {MemDB[5]}]
set_property -dict {PACKAGE_PIN V14 IOSTANDARD LVCMOS33} [get_ports {MemDB[6]}]
set_property -dict {PACKAGE_PIN U14 IOSTANDARD LVCMOS33} [get_ports {MemDB[7]}]
set_property -dict {PACKAGE_PIN P19 IOSTANDARD LVCMOS33} [get_ports RamOEn]
set_property -dict {PACKAGE_PIN R19 IOSTANDARD LVCMOS33} [get_ports RamWEn]
set_property -dict {PACKAGE_PIN N19 IOSTANDARD LVCMOS33} [get_ports RamCEn]


set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
