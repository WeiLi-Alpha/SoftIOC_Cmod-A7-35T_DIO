--  Copyright (c) 2016 Eclektek LLC. All rights reserved.
--
--
--  Developed by: William Carter
--
--  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and  
--  associated documentation files (the "Software"), to deal with the Software without restriction,  
--  including without limitation the rights to use, copy, modify, merge, publish, sublicense and/or    
--  distribute copies of the Software, and to permit persons to whom the Software is furnished to do so,  
--  subject to the following conditions:
--
--      Redistributions of source code must retain the above copyright notice, this list of conditions 
--      and the following disclaimers.
--      Redistributions in binary form must reproduce the above copyright notice, this list of conditions 
--      and the following disclaimers in the documentation and/or other materials provided with the distribution.
--      Neither the names of William Carter, Eclektek LLC, nor the names of its 
--      contributors may be used to endorse or promote products derived from this Software without 
--      specific prior written permission from Eclektek LLC.
--      This Software is provided free of charge and Eclektek LLC reserves the right to sell copies of the 
--      Software in it original form. Anyone sub-licensing this Software will provide it free of charge.
--
--  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
--  LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
--  IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
--  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
--  SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.
-------------------------------------------------------------------------------
--  History :                                                                       
--                                                                                                                  
--  Date      By    Comments                                         
--  --------  ----  ------------------------------------------------------------
--  09/29/16  W.C.  Created                                     
--	11/16/22  W.L. 	Enable turnning on both A, B and P groups simultaneously.
-------------------------------------------------------------------------------
--  Project       : Cmod A7-35T Demo                                                          
--  PCB           : Cmod A7-35T
--  Entity Name   : CmodA735T_Demo
--  File Name     : CmodA735T_Demo.vhd
--  Design Parent : none                                                          
--                                                                             
-------------------------------------------------------------------------------
--  Dependencies:
--
--  CmodA735T_Demo.vhd is uses the following components:
--    CmodA735T_test    CmodA735T_test.dcp
--
--  NexysVideo_SDR_Test.vhd is uses the following packages:
--    Package        none
--
-------------------------------------------------------------------------------
--
--  Description:
--
--    A simple project to try out the new 48-pin module
--    Easy terminal read/write of internal registers and SRAM. See note below.
--    Capture timestamp by reading register at address A 
--    Read captured timestamp/256 at address B
--    Write sram address register at address C
--    Write sram at address D
--    Read sram at address E
--    write RGB LED on-time (%60) to address A
--      RegA(5:0)  is red on time (max 60)
--      RegA(13:7) is blue on time (max 60)
--      RegA(12:8) is green on time (max 60)
--    write pwm 28-bit divider to address 9 (0 = 50MHz, 0x0FFFFFFF = 2 sec)
--    write PIO1:PIO8 outputs at address 7
--    read  PIO48:PIO41 inputs at address 8
--      note: the outputs are inputs are on opposing pins and PIO48:PIO41 are in reverse order 
--
--  Deficiencies:
--
--  ToDo:
--
--  NOTES:
--
--    - UART comes up as COM34 921600 baud. Have Putty set up to enhance terminal presentation,
--    - Must have CAPS on to use A..F as numeric input to terminal (numbers must be in hex format)
--    - for simplicity sram read/writes are 8-bit ( low 8-bits of sram write register )
--  
-------------------------------------------------------------------------------



Library ieee;
  use ieee.std_logic_1164.all;
  use ieee.std_logic_arith.all;
  use ieee.std_logic_unsigned.all;

library UNISIM;
  use UNISIM.vcomponents.all;
  
entity CmodA735T_Demo is
  port(
        -- GLOBAL SIGNALS
        sysclk        : in    std_logic;                      -- 12 Mhz clock module input        PACKAGE_PIN L17
        btn           : in    std_logic_vector(1 downto 0);   -- normally low, high when pushed   PACKAGE_PIN B18, A18 
        led           : out   std_logic_vector(1 downto 0);   -- high lights the green led        PACKAGE_PIN C16, A17
        led0_b        : out   std_logic;                      -- low lights the RGB blue LED      PACKAGE_PIN B17
        led0_g        : out   std_logic;                      -- low lights the RGB green LED     PACKAGE_PIN B16
        led0_r        : out   std_logic;                      -- low lights the RGB red LED       PACKAGE_PIN C17
        
        -- SRAM pins
        MemAdr        : out   std_logic_vector(18 downto 0);  -- External SRAM address
        MemDB         : inout std_logic_vector(7 downto 0);   -- External SRAM data
        RamOEn        : out   std_logic;                      -- External SRAM OEn 
        RamWEn        : out   std_logic;                      -- External SRAM WEn 
        RamCEn        : out   std_logic;                      -- External SRAM CEn 
        
        -- GP IO pins
        IOGroupA      : inout std_logic_vector(20 downto 0);  -- module pins 23..17, 14..1
        IOGroupB      : inout std_logic_vector(22 downto 0);  -- module pins 23..17, 14..1
        ja            : inout std_logic_vector(7 downto 0);   -- PMOD pins 10..7, 4..1
        -- xa_n          : inout std_logic_vector(15 downto 0);  -- 
        
        uart_txd_in   : in    std_logic;                      -- FT2232HQ UART TxD --> FPGA RxD   PACKAGE_PIN J17
        uart_rxd_out  : out   std_logic                       -- FT2232HQ UART RxD <-- FPGA TxD   PACKAGE_PIN J18 
  );
end entity;

architecture rtl of CmodA735T_Demo is

-------------------------------------------------------------------------------
--  Component Declarations
-------------------------------------------------------------------------------


  component CmodA735T_test
  port(
        -- GLOBAL SIGNALS
        clk100        : in    std_logic;                      -- 100 MHz PLL or MMCM clock input
        btn           : in    std_logic_vector(1 downto 0);   -- normally low, high when pushed   PACKAGE_PIN B18, A18 
        led           : out   std_logic_vector(1 downto 0);   -- high lights the green led        PACKAGE_PIN C16, A17
        led0_b        : out   std_logic;                      -- low lights the RGB blue LED      PACKAGE_PIN B17
        led0_g        : out   std_logic;                      -- low lights the RGB green LED     PACKAGE_PIN B16
        led0_r        : out   std_logic;                      -- low lights the RGB red LED       PACKAGE_PIN C17
        
        -- SRAM pins
        MemAdr        : out   std_logic_vector(18 downto 0);  -- External SRAM address
        MemDB         : inout std_logic_vector(7 downto 0);   -- External SRAM data
        RamOEn        : out   std_logic;                      -- External SRAM OEn 
        RamWEn        : out   std_logic;                      -- External SRAM WEn 
        RamCEn        : out   std_logic;                      -- External SRAM CEn 
        
        -- GroupA IO
        IOA_out       : out   std_logic_vector(20 downto 0);  -- module pins 23..17, 14..1
        IOA_in        : in    std_logic_vector(20 downto 0);  -- module pins 23..17, 14..1
        IOA_oe        : out   std_logic;                      -- output enable 
        
        -- GroupB IO
        IOB_out       : out   std_logic_vector(22 downto 0);  -- module pins 33, 34, 26..32, 35..48
        IOB_in        : in    std_logic_vector(22 downto 0);  -- module pins 33, 34, 26..32, 35..48
        IOB_oe        : out   std_logic;                      -- output enable
        
        -- PMOD IO    
        pmod_out      : out   std_logic_vector(7 downto 0);   -- JA pins 10..7, 4..1
        pmod_in       : in    std_logic_vector(7 downto 0);   -- JA pins 10..7, 4..1
        pmod_oe       : out   std_logic;                      -- output enable
        
        -- XADC interface
        xadc_di       : out   std_logic_vector(15 downto 0);  -- DRP data in
        xadc_do       : in    std_logic_vector(15 downto 0);  -- DRP data out
        xadc_dwe      : out   std_logic;                      -- DRP write enable
        xadc_drdy     : in    std_logic;                      -- DRP read data ready
        xadc_den      : out   std_logic;                      -- DRP enable
        xadc_addr     : out   std_logic_vector(6 downto 0);   -- DRP address
        xadc_alarm    : in    std_logic_vector(7 downto 0);   -- DRP alarm outputs
        xadc_ot_alm   : in    std_logic;                      -- DRP over-temperature alarm output
        
        uart_txd_in   : in    std_logic;                      -- FT2232HQ UART TxD --> FPGA RxD   PACKAGE_PIN J17
        uart_rxd_out  : out   std_logic                       -- FT2232HQ UART RxD <-- FPGA TxD   PACKAGE_PIN J18 
  );
  end component;



  component clk_wiz_0
  port
   (-- Clock in ports
    clk_in1           : in     std_logic;
    -- Clock out ports
    clk_out1          : out    std_logic;
    -- Status and control signals
    reset             : in     std_logic;
    locked            : out    std_logic
   );
  end component;
  

-------------------------------------------------------------------------------
--  Type Declarations
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------
--  Constant Declarations
-------------------------------------------------------------------------------
                                                                                      
-------------------------------------------------------------------------------
--  Signal Declarations
-------------------------------------------------------------------------------

signal clk100                     : std_logic;
signal locked                     : std_logic;
signal xadc_di                    : std_logic_vector(15 downto 0);
signal xadc_do                    : std_logic_vector(15 downto 0);
signal xadc_dwe                   : std_logic;
signal xadc_drdy                  : std_logic;
signal xadc_den                   : std_logic;
signal xadc_addr                  : std_logic_vector(6 downto 0);
signal xadc_alarm                 : std_logic_vector(7 downto 0);
signal xadc_overtemp_alarm        : std_logic;
signal io_a_dout                  : std_logic_vector(20 downto 0);
signal io_b_dout                  : std_logic_vector(22 downto 0);
signal pmod_dout                  : std_logic_vector(7 downto 0);
signal io_a_din                   : std_logic_vector(20 downto 0);
signal io_b_din                   : std_logic_vector(22 downto 0);
signal pmod_din                   : std_logic_vector(7 downto 0);
signal io_a_oe                    : std_logic;
signal io_b_oe                    : std_logic;
signal pmod_oe                    : std_logic;

-------------------------------------------------------------------------------
--  Procedure Declarations
-------------------------------------------------------------------------------
  
  
begin


-------------------------------------------------------------------------------
--  Component Instantiations
-------------------------------------------------------------------------------

  CmodA735T_inst : CmodA735T_test
  port map(
        clk100        => clk100,
        btn           => btn, 
        led           => led,
        led0_b        => led0_b,
        led0_g        => led0_g,
        led0_r        => led0_r,
        MemAdr        => MemAdr,
        MemDB         => MemDB,
        RamOEn        => RamOEn,
        RamWEn        => RamWEn,
        RamCEn        => RamCEn,
        IOA_out       => io_a_dout,
        IOA_in        => io_a_din,
        IOA_oe        => io_a_oe,
        IOB_out       => io_b_dout,
        IOB_in        => io_b_din,
        IOB_oe        => io_b_oe,
        pmod_out      => pmod_dout,
        pmod_in       => pmod_din,
        pmod_oe       => pmod_oe,
        xadc_di       => xadc_di,
        xadc_do       => xadc_do,
        xadc_dwe      => xadc_dwe,
        xadc_drdy     => xadc_drdy,
        xadc_den      => xadc_den ,
        xadc_addr     => xadc_addr,
        xadc_alarm    => xadc_alarm,
        xadc_ot_alm   => xadc_overtemp_alarm,
        uart_txd_in   => uart_txd_in,
        uart_rxd_out  => uart_rxd_out);
        
        
  MCM0 : clk_wiz_0
     port map ( 
     clk_in1  => sysclk,  -- 12 MHz
     clk_out1 => clk100,  -- 100 MHz
     reset    => '0',
     locked   => locked            
   );

  -- XADC: Dual 12-Bit 1MSPS Analog-to-Digital Converter
  -- 7 Series
  -- Xilinx HDL Libraries Guide, version 13.4
  XADC_inst : XADC
  generic map (
    -- INIT_40 - INIT_42: XADC configuration registers
    INIT_40 => X"A000", -- 64 sample averaging enabled
    INIT_41 => X"2ef0",
    INIT_42 => X"0800", -- ADCCLK = 100/8 = 12.5 Mhz
    -- INIT_48 - INIT_4F: Sequence Registers
    INIT_48 => X"4701", -- CHSEL1 - enable Temp VCCINT, VCCAUX, VCCBRAM, and calibration
    INIT_49 => X"0000", -- CHSEL2 - enable nothing else
    INIT_4A => X"0001", -- SEQAVG1 disabled all channels
    INIT_4B => X"0000", -- SEQAVG2 disabled all channels
    INIT_4C => X"0000", -- SEQINMODE0 - all channels unipolar
    INIT_4D => X"0000", -- SEQINMODE1 - all channels unipolar
    INIT_4E => X"0000", -- SEQACQ0 - No extra settling time all channels
    INIT_4F => X"0000", -- SEQACQ1 - No extra settling time all channels
    -- INIT_50 - INIT_58, INIT5C: Alarm Limit Registers
    INIT_50 => X"b5ed", -- Temp upper alarm trigger 85°C
    INIT_51 => X"5999", -- Vccint upper alarm limit 1.05V
    INIT_52 => X"A147", -- Vccaux upper alarm limit 1.89V
    INIT_53 => X"dddd", -- OT upper alarm limit 125°C - see Thermal Management
    INIT_54 => X"a93a", -- Temp lower alarm reset 60°C
    INIT_55 => X"5111", -- Vccint lower alarm limit 0.95V
    INIT_56 => X"91Eb", -- Vccaux lower alarm limit 1.71V
    INIT_57 => X"ae4e", -- OT lower alarm reset 70°C - see Thermal Management
    INIT_58 => X"5999", -- VCCBRAM upper alarm limit 1.05V
    INIT_5C => X"5111", -- VCCBRAM lower alarm limit 0.95V
    -- Simulation attributes: Set for proepr simulation behavior
    SIM_DEVICE => "7SERIES", -- Select target device (values)
    SIM_MONITOR_FILE => "design.txt" -- Analog simulation data file name
  )
  port map (
    -- ALARMS: 8-bit (each) output: ALM, OT
    ALM             => xadc_alarm,          -- 8-bit output: Output alarm for temp, Vccint, Vccaux and Vccbram
    OT              => xadc_overtemp_alarm, -- 1-bit output: Over-Temperature alarm
    -- Dynamic Reconfiguration Port (DRP): 16-bit (each) output: Dynamic Reconfiguration Ports
    DO              => xadc_do,             -- 16-bit output: DRP output data bus
    DRDY            => xadc_drdy,           -- 1-bit output: DRP data ready
    -- STATUS: 1-bit (each) output: XADC status ports
    BUSY            => open, -- 1-bit output: ADC busy output
    CHANNEL         => open, -- 5-bit output: Channel selection outputs
    EOC             => open, -- 1-bit output: End of Conversion
    EOS             => open, -- 1-bit output: End of Sequence
    JTAGBUSY        => open, -- 1-bit output: JTAG DRP transaction in progress output
    JTAGLOCKED      => open, -- 1-bit output: JTAG requested DRP port lock
    JTAGMODIFIED    => open, -- 1-bit output: JTAG Write to the DRP has occurred
    MUXADDR         => open, -- 5-bit output: External MUX channel decode
    -- Auxiliary Analog-Input Pairs: 16-bit (each) input: VAUXP[15:0], VAUXN[15:0]
    VAUXN           => (others => '0'),     -- 16-bit input: N-side auxiliary analog input
    VAUXP           => (others => '0'),     -- 16-bit input: P-side auxiliary analog input
    -- CONTROL and CLOCK: 1-bit (each) input: Reset, conversion start and clock inputs
    CONVST          => '0',                 -- 1-bit input: Convert start input
    CONVSTCLK       => '0',                 -- 1-bit input: Convert start input
    RESET           => '0',                 -- 1-bit input: Active-high reset
    -- Dedicated Analog Input Pair: 1-bit (each) input: VP/VN
    VN              => '0',                 -- 1-bit input: N-side analog input
    VP              => '0',                 -- 1-bit input: P-side analog input
    -- Dynamic Reconfiguration Port (DRP): 7-bit (each) input: Dynamic Reconfiguration Ports
    DADDR           => xadc_addr,           -- 7-bit input: DRP address bus
    DCLK            => clk100      ,        -- 1-bit input: DRP clock
    DEN             => xadc_den,            -- 1-bit input: DRP enable signal
    DI              => xadc_di,             -- 16-bit input: DRP input data bus
    DWE             => xadc_dwe             -- 1-bit input: DRP write enable
  );
   
   
-------------------------------------------------------------------------------
--  Concurrent Assignments
-------------------------------------------------------------------------------

  io_a_din  <= IOGroupA;
  io_b_din  <= IOGroupB;
  pmod_din  <= ja;
  
-------------------------------------------------------------------------------
--  Process Declarations
-------------------------------------------------------------------------------


-------------------------------------------------------------------------------
--  Other Output Assignments
-------------------------------------------------------------------------------
 
--  IOGroupA  <= io_a_dout when io_a_oe = '1' and io_b_oe = '0' else (others => 'Z');
-- IOGroupB  <= io_b_dout when io_a_oe = '0' and io_b_oe = '1' else (others => 'Z');
  IOGroupA  <= io_a_dout when io_a_oe = '1' else (others => 'Z');
  IOGroupB  <= io_b_dout when io_b_oe = '1' else (others => 'Z');
  ja        <= pmod_dout when pmod_oe = '1' else (others => 'Z');

end rtl;
