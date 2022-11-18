#-----------------------------------------------------------------------------
#  Copyright (c) 2016 Eclektek LLC. All rights reserved.
#
#
#  Developed by: William Carter
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and  
#  associated documentation files (the "Software"), to deal with the Software without restriction,  
#  including without limitation the rights to use, copy, modify, merge, publish, sublicense and/or    
#  distribute copies of the Software, and to permit persons to whom the Software is furnished to do so,  
#  subject to the following conditions:
#
#      Redistributions of source code must retain the above copyright notice, this list of conditions 
#      and the following disclaimers.
#      Redistributions in binary form must reproduce the above copyright notice, this list of conditions 
#      and the following disclaimers in the documentation and/or other materials provided with the distribution.
#      Neither the names of William Carter, Eclektek LLC, nor the names of its 
#      contributors may be used to endorse or promote products derived from this Software without 
#      specific prior written permission from Eclektek LLC.
#      This Software is provided free of charge and Eclektek LLC reserves the right to sell copies of the 
#      Software in it original form. Anyone sub-licensing this Software will provide it free of charge.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT 
#  LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
#  IN NO EVENT SHALL THE CONTRIBUTORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
#  WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
#  SOFTWARE OR THE USE OR OTHER DEALINGS WITH THE SOFTWARE.
#-----------------------------------------------------------------------------
#  History :                                                                       
#                                                                                                                  
#  Date      By    Version  Comments                                         
#  --------  ----  -------  -----------------------------------------------------
#  10/03/16  W.C.  1.00     Created                                     
#
#-----------------------------------------------------------------------------
# C7Test.py was written using Python 2.7 on Windows 7
# C7Test.py requires the following non-standard Library modules:
#   pyserial-2.6
#   
#-----------------------------------------------------------------------------
# C7Test.py was designed to simplify testing the Cmod A7 board using a USB UART interface. 
# C7Test requires that the Cmod A7 to be configured with CmodA735T_Demo.bit
#
#
# Command line Useage: <Python Path>python C7Test.py [-p port]
#  where <Python Path> is the location of your Python version 2.7 or less installation
#  [port] is the name of the USB UART port connected to your FPGA board UART connector
#  [off] disables data logging ( anything else or absense of the -l options enables data logging
#
#   Windows example:  C:\Python27\python27 C7Test.py -p COM9
#   Linux example:    python C7Test.py -p /dev/ttyUSB1 
#
# C7Test first checks that the specified UART port is available. If not it exits. If the port is
# available a series of tests are run and then the user is presented with a menu displayed in the 
# terminal window or DOS box offering a number of subsequent commands.
#
# If you know what serial port is enumerated you can modify the uart_port variable to 
# avoid using the -p command line option:
#   uart_port = 'COM34'         - Cmod A7-35T UART on Win7
#   uart_port = '/dev/ttyUSB1'  - Cmod A7-35T UART on Centos 6.8
#
# C7Test Commands are:
#   'Q' - Quit C7Test
#   'D' - Display registers R0 though R15
#   'T' - Displays the current FPGA Temperature sensor reading in Celsius degrees
#   'I' - Set output enables for the IO Groups
#   'W' - Set the output value for an IO Group
#   'S' - Write or read an external SRAM memory location
#   'L' - Change the tricolor LED brightness and blink rate
#   'C' - Display the Current Timer Count 
#           The timer is incremented every 2.56 us
#           [timer count]*256/100000000 is the elapsed time from configuratation 
#           or the last reset (btn(0) press) in seconds. Overflows about every 183 minutes.
# 
#-----------------------------------------------------------------------------
# NOTES:
#
#   - in Windows 7 the appropriate UART port can be found using the Windows Device Manager and is typically COMxx. In
#     Linux typing 'dmesg | grep tty' in a terminal will display all of the USB devices that have been enumerated. In either OS
#     comparing what's available when the FPGA UART is not attached to what's available when it is attached helps 
#     identify the correct port in case of confusion.
#
#   - Vivado tries to maintain a JTAG connection to the Cmod7 board. For the Cmod7 designs this causes a problem if 
#     this program and Vivado are running simultaneously. Digilent Adept for Windows utility seems to co-exist with
#     C7Test.py most of the time. Occasionally, the USB UART is disconnected if C7Test is running for a long time. 
#     One solution is to quit C7Test, unplug the USB cable , and reconfigure the Cmod7 board.
# 
#-----------------------------------------------------------------------------
# ToDo:
#
#-----------------------------------------------------------------------------
# KNOWN ISSUES:
#
#-----------------------------------------------------------------------------

# Modules
import serial
import time
import math
import sys

# Some definitions

# FPGA UART_RegAccess Register Assignments
xadc_read_reg             = '0'
xadc_write_reg            = '1'
gpio_control_reg          = '2'
iogroup_a_read_reg        = '3'
iogroup_a_write_reg       = '4'
iogroup_b_read_reg        = '5'
iogroup_b_write_reg       = '6'
iopmod_read_reg           = '7'
iopmod_write_reg          = '8'
pwm_prescaler             = '9'
pwm_control_reg           = 'A'
timer_capture_reg         = 'B'
sram_address_reg          = 'C'
sram_data_write_reg       = 'D'
sram_data_read_reg        = 'E'
sram_control_reg          = 'F'

# Control and Status bit field assignments
## Reg0
xadc_temp_ot_alarm_mask   = 0x80000000
xadc_alarm_mask           = 0x7F000000
xadc_read_data_mask       = 0x0000FFFF
## Reg1
xadc_wr_bit_mask          = 0x80000000
xadc_address_mask         = 0x01FF0000
xadc_write_data           = 0x0000FFFF
## Reg2
io_a_output_enable_mask   = 0x00000001
io_b_output_enable_mask   = 0x00000002
pmod_output_enable_mask   = 0x00000004
enable_mask               = 0x00000007
## Reg3, REG4
io_a_data_mask            = 0x001FFFFF
## Reg5, REG6
io_b_data_mask            = 0x007FFFFF
## Reg7, REG8
pmod_data_mask            = 0x000000FF
## Reg9
pwm_red_on_mask           = 0x0000001F
pwm_blue_on_mask          = 0x00001F00
pwm_green_on_mask         = 0x001F0000
## Reg10
pwm_prescaler_mask        = 0x0FFFFFFF
## Reg11
timer_count_mask          = 0xFFFFFFFF
## Reg12
sram_address_mask         = 0x0003FFFF
## Reg13, Reg14
sram_data_mask            = 0x000000FF
## Reg15

# Global values
bit_31      = 2147483648
bit_24      = 16777216
bit_16      = 65536
bit_8       = 256
bit_2       = 4
bit_1       = 2
bit_0       = 1

regrd_last_data_digit     = 14
regrd_length              = 15


# command line options
uart_port = 'COM34'
#uart_port = '/dev/ttyUSB1'

# get command-line options
def get_options(argv):
  clo= {}
  while argv:
    if argv[0][0] == '-':
      clo[argv[0]] = argv[1]
      argv = argv[2:]
    else:
      argv = argv[1:]
  return clo

# Write XADC  
def write_xadc():
  s = raw_input('Enter Reg11 data => ')
  print(s)
  TestData = 'W ' + xadc_write_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)
 
# Display FPGA core temperature in Celsius degrees
def get_xadc_temp():
  TestData = 'W ' + xadc_write_reg + ' 0' + ' \x0D\x0A'
  ser.write(TestData)
  time.sleep(.2)              # delay 
  TestData = 'R ' + xadc_read_reg + ' \x0D\x0A'
  ser.write(TestData)
  ResponseData = ser.read(regrd_length)
  n = int(ResponseData[4:regrd_last_data_digit], 16)
  t = float(n)*2015.0/(16.0*16384.0) - 273.0
  print('FPGA Core Temperature = ', t)   
    

# function to display the contents of all registers
def reg_dump():
  x = 0
  while x < 16:
    s = str(hex(x))
    TestData = 'R ' + s.upper() + '\x0D\x0A'
    ser.write(TestData)
    ResponseData = ser.read(regrd_length)
    print(ResponseData)
    x = x + 1

# Function to set the pwm on times
# expects values of r,g and b to be in between 0 and 31
def set_pwm_rgb(r, g, b):
  x = r + b*bit_8 + g*bit_16
  s = str(hex(x))
  TestData = 'W ' + pwm_control_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)

# Function to set the pwm prescaler
def set_pwm_interval(n):
  x = n & pwm_prescaler_mask
  s = str(hex(x))
  TestData = 'W ' + pwm_prescaler + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)

# Function to display IO Group Output enables
def show_enables():
  a = 'off'
  b = 'off'
  p = 'off'
  TestData = 'R ' + gpio_control_reg + ' \x0D\x0A'
  ser.write(TestData)
  ResponseData = ser.read(regrd_length)
  x = int(ResponseData[4:regrd_last_data_digit],16)
  if x & io_a_output_enable_mask > 0:
    a = 'On'
  if x & io_b_output_enable_mask > 0:
    b = 'On'
  if x & pmod_output_enable_mask > 0:
    p = 'On'
  print('A GPIO IO; ', a, ' B GPIO IO; ', b, ' PMOD IO; ', p)   
  

# Function to Set GPIO Output Enables
# n is an integer bewteen 0 and 7
def set_output_enables(n):
  x = n & enable_mask
  if x == 1 or x == 2:
    # Disable A and B outputs before enabling either
    TestData = 'W ' + gpio_control_reg + '0 \x0D\x0A'
    ser.write(TestData)
    time.sleep(.1)  
  s = str(hex(x))
  TestData = 'W ' + gpio_control_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)
    
# Function to write Group IO value
# p is an int; IOA = 1, IOB = 2, PMOD = 3
# v is an int
def set_gpio(p, v):
  if p == 1:
    x = v & io_a_data_mask
    s = format(x,'012x')
    TestData = 'W ' + iogroup_a_write_reg + ' ' + s.upper() + ' \x0D\x0A'
    ser.write(TestData)   
  elif p == 2:
    x = v & io_b_data_mask
    s = format(x,'012x')
    TestData = 'W ' + iogroup_b_write_reg + ' ' + s.upper() + ' \x0D\x0A'
    ser.write(TestData)
  elif p == 3:
    x = v & io_b_data_mask
    s = format(x,'012x')
    TestData = 'W ' + iopmod_write_reg + ' ' + s.upper() + ' \x0D\x0A'
    ser.write(TestData)
  
# Function to read Group IO value

# Function to Write SRAM Memory at a specific address
def write_sram(a,d):
  s = format(a,'012x')
  TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)   
  s = format(d,'012x')
  TestData = 'W ' + sram_data_write_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)   

# Function to Read SRAM Memory from a specific address
def read_sram(a):
  s = format(a,'012x')
  TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)   
  TestData = 'R ' + sram_data_read_reg + ' \x0D\x0A'
  ser.write(TestData)   
  ResponseData = ser.read(regrd_length)
  d = int(ResponseData[12:14],16)
  print(hex(a),hex(d))
  
# Function to Write SRAM Memory at current address
# NOTE: reading sram_data_read_reg or writing sram_data_write_reg auto-increments
#       the sram_address_reg 
def write_sram_ca(d):
  s = format(d,'012x')
  TestData = 'W ' + sram_data_write_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)   
  time.sleep(.1)

# Function to Read SRAM Memory from current address
# NOTE: reading sram_data_read_reg or writing sram_data_write_reg auto-increments
#       the sram_address_reg 
def read_sram_ca():
  TestData = 'R ' + sram_data_read_reg + ' \x0D\x0A'
  ser.write(TestData)   
  ResponseData = ser.read(regrd_length)
  d = int(ResponseData[12:14],16)
  return d    
    
# Function to test the SRAM  by writing a block and reading it back
def sram_test():
  e = [0,0,0,0,0,0,0,0]
  # read the timer to get a starting address
  TestData = 'R ' + timer_capture_reg + ' \x0D\x0A'
  ser.write(TestData)   
  ResponseData = ser.read(regrd_length)
  a = int(ResponseData[10:14],16)
  d = int(ResponseData[7:9],16)   
  s = format(a,'012x')
  TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)
  c = 0
  print('Wrote SRAM ', str(hex(a)),'')
  while c < 8:
    e[c] = d
    print(hex(d))
    write_sram_ca(d)
    c = c + 1
    d = d + 1
  print()
  # reset the address counter
  s = format(a,'012x')
  TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
  ser.write(TestData)   
  # read back the SRAM  
  c = 0
  print('Read  SRAM ', str(hex(a)), '')
  while c < 8:
    x = read_sram_ca()
    print(hex(x))
    c = c + 1
  print()
  
# Function to display current timer count
def get_timer():
  TestData = 'R ' + timer_capture_reg + ' \x0D\x0A'
  ser.write(TestData)   
  ResponseData = ser.read(regrd_length)
  x = float(int(ResponseData[4:regrd_last_data_digit],16))*256.0/100000000.0
  print('Timer Count = ',x)
       
  
def print_cmds():
  print('\nCommands: Q D T I W S L C')
  
 
# Begin by checking for command line options
#   -p 'USB PORT NAME'  - USB PORT NAME examples 'COM11' , 'USB1'
cmd_line_options = get_options(sys.argv)
print(cmd_line_options)
str_temp = "-p"
#if cmd_line_options.has_key('-p') == 1:
#if str_temp in cmd_line_options:
if "-p" in cmd_line_options:
  uart_port = cmd_line_options['-p']
  uart_port = uart_port
  print('Using UART PORT: ', uart_port)
      
  

# Start by trying to open the specified UART port
try:
  ser = serial.Serial(port=uart_port)
except:  
  uart_port_is_open = False
  print(uart_port, ' is not available')
else:
  uart_port_is_open = True
  ser.baudrate = 921600 
  # select FIVEBITS, SIXBITS, SEVENBITS or EIGHTBITS of data
  #ser.bytesize = serial.FIVEBITS
  #ser.bytesize = serial.SIXBITS
  #ser.bytesize = serial.SEVENBITS
  ser.bytesize = serial.EIGHTBITS
  
  # select STOPBITS_ONE, STOPBIT_TWO or STOPBITS_ONE_POINT_FIVE
  ser.stopbits = serial.STOPBITS_ONE
  #ser.stopbits = serial.STOPBIT_TWO
  #ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
  
  # select PARITY_NONE, PARITY_EVEN or PARITY_ODD
  ser.parity = serial.PARITY_NONE
  #ser.parity = serial.PARITY_EVEN
  #ser.parity = serial.PARITY_ODD
  
  ser.xonxoff = 0
  ser.rtscts = 0
  # IF you don't set the timeout for reads the code will hang
  ser.timeout = 0.5
  
  #ser.parity = serial.PARITY_EVEN
  
# only continue if the specified UART connection exists  
if uart_port_is_open == True:
    
  # Test R15 to see if we can communicate with the FPGA
  print('Writing R15 with 0x11223344 to test interface')
  TestData = 'W ' + sram_control_reg + ' 11223344\x0D\x0A' # write command followed by CRLF
  ser.write(TestData.encode())
  TestData = 'R ' + sram_control_reg + ' \x0D\x0A'
  ser.write(TestData.encode())
  ResponseData = ser.read(regrd_length).decode()
  #print('Undecoded:',ser.read(regrd_length))
  #print('decoded:',ResponseData)
  #print('Reading R15: ',ResponseData)
  if ResponseData[:regrd_last_data_digit] == '0xF 0x11223344':
    print('Register write/read Test Successful')
    has_connection = True
  else:  
    print('Register write/read Test Failed!')
    has_connection = False
    #has_connection = True
  
  
  # After the initial tests we have the main menu
  # but only if we were able to read back R0 successfully
  if has_connection == True:
    # but first light the tri-color LED
    set_pwm_rgb(8, 8, 8)
    # then runs a simple sram test
    sram_test()
    u = '~'
    while 1:
      print_cmds()
      u = raw_input('\nEnter Command => ')
      # Quit the test
      if u.upper() == 'Q':
        break
          
      # Print Control/Status registers    
      elif u.upper() == 'D':
        reg_dump()
      
      # Display the FPGA core temperature        
      elif u.upper() == 'T':
        get_xadc_temp()
      
      # Display the Current Timer Count        
      elif u.upper() == 'C':
        get_timer()
      
      # Set IO Enables        
      elif u.upper() == 'I':
        show_enables()
        x = 0
        c = raw_input('Enable IO Group A Outputs? <y/n> => ')
        if c == 'y':
          x = bit_0
        else:
          c = raw_input('Enable IO Group B Outputs? <y/n> => ')
          if c == 'y':
            x = bit_1
        c = raw_input('Enable PMOD IO Outputs? <y/n> => ')
        if c == 'y':
          x = x + bit_2          
        set_output_enables(x)
        show_enables()
        
      # Write to an IO Group        
      elif u.upper() == 'W':
        v1 = 0
        v2 = 0
        c = raw_input('Enter GPIO Group (a,b or p) => ')
        if c.upper() == 'A':
          v1 = 1
        elif c.upper() == 'B':   
          v1 = 2
        elif c.upper() == 'P':   
          v1 = 3
        else:
          print('Invalid Selection')
          break          
        c = raw_input('Enter GPIO Value in hex digits => ')
        v2 = int(c,16)
        set_gpio(v1, v2)       
        
      # SRAM read/write        
      elif u.upper() == 'S':
        c = raw_input('Enter Address in hex digits => ')
        va = int(c,16)
        c = raw_input('Read or Write? (r,w) => ')
        if c.upper() == 'W':
          c = raw_input('Enter Data in hex digits => ')
          vd = int(c,16)
          write_sram(va,vd)
        read_sram(va)
        
      # Change the Tri-color LED display        
      elif u.upper() == 'L':
        lr = 2
        lb = 2
        lg = 2
        c = raw_input('Enter Value for Red LED Intensity (0 to 31) => ')
        if int(c) < 31:
          lr = int(c)
        c = raw_input('Enter Value for Blue LED Intensity (0 to 31) => ')
        if int(c) < 31:
          lb = int(c)
        c = raw_input('Enter Value for Green LED Intensity (0 to 31) => ')
        if int(c) < 31:
          lg = int(c)     
        set_pwm_rgb(lr, lg, lb)
        TestData = 'R ' + pwm_prescaler + ' \x0D\x0A'
        ser.write(TestData)
        ResponseData = ser.read(regrd_length)
        x = 100000000/int(ResponseData[4:regrd_last_data_digit],16)
        print('Current PWM Frequency: ', str(x))
        c = raw_input('Enter PWM Trigger Frequency in Hz ( or Enter ) => ')
        if len(c) > 1:
          x = 100000000/int(c)
          if x > 10:
            set_pwm_interval(x)
          
      else:
        print('\nNot a valid Command')
    
  ser.close

