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
#  11/14/22  W.L.  2.00     Rename the file as "ArtyA735T_DIO".
#                           Reorganized the functions into a class.
#                           Modified the script and function to run with python3.
#                           Add set_gpio_pin() to enable configuration of individual pins;
#                           Add get_gpio() and get_gpio_pin() to read the status of pins;
#-----------------------------------------------------------------------------
# Original package and information can be found in https://forum.digilent.com/topic/2866-cmod-a7-35t-demo-project/:
#
# This script has already be mofidied by W.L, and it's tested using python 3.8.
#-----------------------------------------------------------------------------
# CmodA735_DIO.py was designed to simplify set and read the GPIO and PMOD pin status on the Cmod A7 board
# using a USB UART interface.
# CmodA735_DIO requires that the Cmod A7 to be configured with CmodA735T_Demo.bit
#
# Useage in python:
#   import CmodA735T_DIO
#   device = CmodA735T_DIO.CMODA(<PORT>) #  <PORT> is the USB port
#   device.get_gpio(<GROUP>)  # <GROUP> is 'A' or 'B' or 'P'
#   device.set_gpio(<GROUP>,VAL)  # <GROUP> is 'A' or 'B' or 'P'
#   device.get_gpio_pin(<GROUP>,<PIN_INDEX>)  # <PIN_INDEX> is the index of pin in  <GROUP>, starting from 0,
#                                             # return a boolean value of 0 or 1
#   device.set_gpio(<GROUP>,<PIN_INDEX>,<1/0>)  # <1/0> for <ON/OFF>
#
#   <PORT> is in the format of 'COMXX' in Window, and '/dev/ttyUSBXX' in CentOS 7
#-----------------------------------------------------------------------------
# NOTES:
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
import struct

# Some definitions
class CMODA7:
      # FPGA UART_RegAccess Register Assignments
      xadc_read_reg = '0'
      xadc_write_reg = '1'
      gpio_control_reg = '2'
      iogroup_a_read_reg = '3'
      iogroup_a_write_reg = '4'
      iogroup_b_read_reg = '5'
      iogroup_b_write_reg = '6'
      iopmod_read_reg = '7'
      iopmod_write_reg = '8'
      pwm_prescaler = '9'
      pwm_control_reg = 'A'
      timer_capture_reg = 'B'
      sram_address_reg = 'C'
      sram_data_write_reg = 'D'
      sram_data_read_reg = 'E'
      sram_control_reg = 'F'

      # Control and Status bit field assignments
      ## Reg0
      xadc_temp_ot_alarm_mask = 0x80000000
      xadc_alarm_mask = 0x7F000000
      xadc_read_data_mask = 0x0000FFFF
      ## Reg1
      xadc_wr_bit_mask = 0x80000000
      xadc_address_mask = 0x01FF0000
      xadc_write_data = 0x0000FFFF
      ## Reg2
      io_a_output_enable_mask = 0x00000001
      io_b_output_enable_mask = 0x00000002
      pmod_output_enable_mask = 0x00000004
      enable_mask = 0x00000007
      ## Reg3, REG4
      io_a_data_mask = 0x001FFFFF
      ## Reg5, REG6
      io_b_data_mask = 0x007FFFFF
      ## Reg7, REG8
      pmod_data_mask = 0x000000FF
      ## Reg9
      pwm_red_on_mask = 0x0000001F
      pwm_blue_on_mask = 0x00001F00
      pwm_green_on_mask = 0x001F0000
      ## Reg10
      pwm_prescaler_mask = 0x0FFFFFFF
      ## Reg11
      timer_count_mask = 0xFFFFFFFF
      ## Reg12
      sram_address_mask = 0x0003FFFF
      ## Reg13, Reg14
      sram_data_mask = 0x000000FF
      ## Reg15
      gpio_data_mask = 0xFFFFFFFFFFFF

      # Global values
      bit_31 = 2147483648
      bit_24 = 16777216
      bit_23 = 8388608
      bit_21 = 2097152
      bit_16 = 65536
      bit_9 = 512
      bit_8 = 256
      bit_2 = 4
      bit_1 = 2
      bit_0 = 1

      regrd_last_data_digit = 14
      regrd_length = 15

      def __init__(self,PORT):
            # command line options
            # self.uart_port = 'COM5'
            self.uart_port = PORT
            # uart_port = '/dev/ttyUSB1'
            self.ser = self.init_connection()
            self.init_connection_test()
            self.set_output_enables()

      # Write XADC, 'Enter Reg11 data => '

      def write_xadc(self,s):
            # s = input('Enter Reg11 data => ')
            # print(s)
            ser = self.ser
            xadc_write_reg = self.xadc_write_reg

            TestData = 'W ' + xadc_write_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())

      # Display FPGA core temperature in Celsius degrees
      def get_xadc_temp(self):
            ser = self.ser
            xadc_write_reg = self.xadc_write_reg
            xadc_read_reg = self.xadc_read_reg
            regrd_last_data_digit = self.regrd_last_data_digit
            regrd_length = self.regrd_length

            TestData = 'W ' + xadc_write_reg + ' 0' + ' \x0D\x0A'
            ser.write(TestData.encode())
            time.sleep(.2)              # delay
            TestData = 'R ' + xadc_read_reg + ' \x0D\x0A'
            ser.write(TestData.encode())
            ResponseData = ser.read(regrd_length).decode()
            n = int(ResponseData[4:regrd_last_data_digit], 16)
            t = float(n)*2015.0/(16.0*16384.0) - 273.0
            print('FPGA Core Temperature = ', t)
            return t

      # function to display the contents of all registers
      def reg_dump(self):
            ser = self.ser

            x = 0
            while x < 16:
                  s = str(hex(x))
                  TestData = 'R ' + s.upper() + '\x0D\x0A'
                  ser.write(TestData.encode())
                  ResponseData = ser.read(regrd_length).decode()
                  print(ResponseData)
                  x = x + 1

      # Function to set the pwm on times
      # expects values of r,g and b to be in between 0 and 31
      def set_pwm_rgb(self, r, g, b):
            ser = self.ser
            pwm_control_reg = self.pwm_control_reg

            x = r + b*bit_8 + g*bit_16
            s = str(hex(x))
            TestData = 'W ' + pwm_control_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())

      # Function to set the pwm prescaler
      def set_pwm_interval(self, n):
            ser = self.ser
            pwm_prescaler_mask = self.pwm_prescaler_mask
            pwm_prescaler = self.pwm_prescaler

            x = n & pwm_prescaler_mask
            s = str(hex(x))
            TestData = 'W ' + pwm_prescaler + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())

      # Function to display IO Group Output enables
      def show_enables(self):
            ser = self.ser
            gpio_control_reg = self.gpio_control_reg
            regrd_length = self.regrd_length
            regrd_last_data_digit = self.regrd_last_data_digit
            io_a_output_enable_mask = self.io_a_output_enable_mask

            a = 'Off'
            b = 'Off'
            p = 'Off'
            TestData = 'R ' + gpio_control_reg + ' \x0D\x0A'
            ser.write(TestData.encode())
            ResponseData = ser.read(regrd_length).decode()
            print('show enable Responsedata:',ResponseData)
            x = int(ResponseData[4:regrd_last_data_digit],16)
            if x & io_a_output_enable_mask > 0:
                a = 'On'
            if x & io_b_output_enable_mask > 0:
                b = 'On'
            if x & pmod_output_enable_mask > 0:
                p = 'On'
            print('A GPIO IO; ', a, ' B GPIO IO; ', b, ' PMOD IO; ', p)
            return a,b,p


      # Function to Set GPIO Output Enables
      # n is an integer bewteen 0 and 7
      # enable all the pins for output
      def set_output_enables(self):
            ser = self.ser
            enable_mask = self.enable_mask
            gpio_control_reg = self.gpio_control_reg

            n = self.bit_0 + self.bit_1 + self.bit_2
            x = n & enable_mask
            # if x == 1 or x == 2:
            # Disable A and B outputs before enabling either
            TestData = 'W ' + gpio_control_reg + '0 \x0D\x0A'
            ser.write(TestData.encode())
            time.sleep(.1)
            s = str(hex(x))
            TestData = 'W ' + gpio_control_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())
            return "OK"

      # Function to write Group IO value
      # p is a char; IOA = 'A', IOB = 'B', PMOD = 'P'
      # pin_index is the index of corresponding pin
      #           IOA , in the range of 0-20
      #           IOB , in the range of 0-22
      #           PMOD, in the range of 0-8
      # val is an int, the new value, either 0 or 1;
      def set_gpio_pin(self, p, pin_index,val):

            if p=='A' and pin_index>20:
                print('Pin index of IOA should be no larger than 20')
            if p=='B' and pin_index>22:
                print('Pin index of IOB should be no larger than 22')
            if p=='P' and pin_index>8:
                print('Pin index of PMOD should be no larger than 8')

            if val!=0 and val!=1:
                print('Setting value must be either 0 or 1')

            print('Before setting value ...')
            val_curr = self.get_gpio(p)

            a = pow(2,pin_index)
            if val==1:
                val_new = a|val_curr
            else:
                if p == 'A':
                    a = self.bit_21 - 1 -a
                elif p == 'B':
                    a = self.bit_23 - 1 - a
                elif p == 'P':
                    a = self.bit_9 - 1 - a
                val_new = a&val_curr
            print('val_curr=%s, val=%s, a=%s, val_new=%s' % (val_curr, val, a, val_new))

            self.set_gpio(p,val_new)

            print('After setting value ...')
            val_curr = self.get_gpio(p)

      def set_gpio(self, p, v):
            ser = self.ser
            iogroup_a_write_reg = self.iogroup_a_write_reg
            iogroup_b_write_reg = self.iogroup_b_write_reg
            iopmod_write_reg = self.iopmod_write_reg
            io_a_data_mask = self.io_a_data_mask
            io_b_data_mask = self.io_b_data_mask
            gpio_data_mask = self.gpio_data_mask

            if p == 'A':
                  x = v & io_a_data_mask
                  s = format(x,'012x')
                  TestData = 'W ' + iogroup_a_write_reg + ' ' + s.upper() + ' \x0D\x0A'
                  ser.write(TestData.encode())
            elif p == 'B':
                  x = v & io_b_data_mask
                  s = format(x,'012x')
                  TestData = 'W ' + iogroup_b_write_reg + ' ' + s.upper() + ' \x0D\x0A'
                  ser.write(TestData.encode())
            elif p == 'P':
                  x = v & io_b_data_mask
                  s = format(x,'012x')
                  TestData = 'W ' + iopmod_write_reg + ' ' + s.upper() + ' \x0D\x0A'
                  ser.write(TestData.encode())


      # Function to read Group IO value
      # p is an int; IOA = 1, IOB = 2, PMOD = 3
      def get_gpio(self,p):
            ser = self.ser
            iogroup_a_read_reg = self.iogroup_a_read_reg
            iogroup_b_read_reg = self.iogroup_b_read_reg
            iopmod_read_reg = self.iopmod_read_reg
            regrd_length = self.regrd_length
            regrd_last_data_digit = self.regrd_last_data_digit

            if p == 'A':
                  TestData = 'R ' + iogroup_a_read_reg + ' \x0D\x0A'
                  ser.write(TestData.encode())
                  ResponseData = ser.read(regrd_length).decode()
                  d = int(ResponseData[4:regrd_last_data_digit], 16)
                  #d = struct.unpack("h",ResponseData[4:regrd_last_data_digit])
                  print('GPIO A readback:', hex(d))
                  print('GPIO A readback d:', d)
            elif p == 'B':
                  TestData = 'R ' + iogroup_b_read_reg + ' \x0D\x0A'
                  ser.write(TestData.encode())
                  ResponseData = ser.read(regrd_length).decode()
                  d = int(ResponseData[4:regrd_last_data_digit], 16)
                  print('GPIO B readback:', hex(d))
            elif p == 'P':
                  TestData = 'R ' + iopmod_read_reg + ' \x0D\x0A'
                  ser.write(TestData.encode())
                  ResponseData = ser.read(regrd_length).decode()
                  d = int(ResponseData[4:regrd_last_data_digit], 16)
                  print('PMOD readback:', hex(d))
            return d


      # Function to read Group IO value
      # p is a char; IOA = 'A', IOB = 'B', PMOD = 'P'
      # pin_index is the index of corresponding pin
      #           IOA , in the range of 0-20
      #           IOB , in the range of 0-22
      #           PMOD, in the range of 0-7
      def get_gpio_pin(self, p, pin_index):

            if p=='A' and pin_index>20:
                print('Pin index of IOA should be no larger than 20')
            if p=='B' and pin_index>22:
                print('Pin index of IOB should be no larger than 22')
            if p=='P' and pin_index>8:
                print('Pin index of PMOD should be no larger than 8')

            val_curr = self.get_gpio(p)
            a = pow(2,pin_index)

            val = val_curr & a
            if val==0:
                val = 0
                status = 'OFF'
            else:
                val=1
                status = 'ON'

            print('%s%s is %s' % (p,pin_index,status))
            return val


      # Function to read Group IO value
      # Function to Write SRAM Memory at a specific address
      def write_sram(self, a,d):
            ser = self.ser
            sram_address_reg = self.sram_address_reg
            sram_data_write_reg = self.sram_data_write_reg

            s = format(a,'012x')
            TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())
            s = format(d,'012x')
            TestData = 'W ' + sram_data_write_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())

      # Function to Read SRAM Memory from a specific address
      def read_sram(self, a):
            ser = self.ser
            sram_address_reg = self.sram_address_reg
            sram_data_read_reg = self.sram_data_read_reg
            regrd_length = self.regrd_length

            s = format(a,'012x')
            TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())
            TestData = 'R ' + sram_data_read_reg + ' \x0D\x0A'
            ser.write(TestData.encode())
            ResponseData = ser.read(regrd_length).decode()
            d = int(ResponseData[12:14],16)
            print(hex(a),hex(d))

      # Function to Write SRAM Memory at current address
      # NOTE: reading sram_data_read_reg or writing sram_data_write_reg auto-increments
      #       the sram_address_reg
      def write_sram_ca(self, d):
            ser = self.ser
            sram_data_write_reg = self.sram_data_write_reg

            s = format(d,'012x')
            TestData = 'W ' + sram_data_write_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())
            time.sleep(.1)

      # Function to Read SRAM Memory from current address
      # NOTE: reading sram_data_read_reg or writing sram_data_write_reg auto-increments
      #       the sram_address_reg
      def read_sram_ca(self):
            ser = self.ser
            sram_data_write_reg = self.sram_data_read_reg
            regrd_length = self.regrd_length

            TestData = 'R ' + sram_data_read_reg + ' \x0D\x0A'
            ser.write(TestData.encode())
            ResponseData = ser.read(regrd_length).decode()
            d = int(ResponseData[12:14],16)
            return d

      # Function to test the SRAM  by writing a block and reading it back
      def sram_test(self):
            ser = self.ser
            timer_capture_reg = self.timer_capture_reg
            regrd_length = self.regrd_length
            sram_address_reg = self.sram_address_reg
            write_sram_ca = self.write_sram_ca
            read_sram_ca = self.read_sram_ca

            e = [0,0,0,0,0,0,0,0]
            # read the timer to get a starting address
            TestData = 'R ' + timer_capture_reg + ' \x0D\x0A'
            ser.write(TestData.encode())
            ResponseData = ser.read(regrd_length).decode()
            a = int(ResponseData[10:14],16)
            d = int(ResponseData[7:9],16)
            s = format(a,'012x')
            TestData = 'W ' + sram_address_reg + ' ' + s.upper() + ' \x0D\x0A'
            ser.write(TestData.encode())
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
            ser.write(TestData.encode())
            # read back the SRAM
            c = 0
            print('Read  SRAM ', str(hex(a)), '')
            while c < 8:
                  x = read_sram_ca()
                  print(hex(x))
                  c = c + 1
            print()

      # Function to display current timer count
      def get_timer(self):
            ser = self.ser
            timer_capture_reg = timer_capture_reg
            regrd_length = self.regrd_length
            regrd_last_data_digit = self.regrd_last_data_digit

            TestData = 'R ' + timer_capture_reg + ' \x0D\x0A'
            ser.write(TestData.encode())
            ResponseData = ser.read(regrd_length).decode()
            x = float(int(ResponseData[4:regrd_last_data_digit],16))*256.0/100000000.0
            print('Timer Count = ',x)


      def print_cmds(self):
            print('\nCommands: Q D T I W S L C')

      def init_connection(self):
            uart_port = self.uart_port

            # Start by trying to open the specified UART port
            try:
                  ser = serial.Serial(port=uart_port)
                  print('doing try...')
            except:
                  uart_port_is_open = False
                  print(uart_port, ' is not available')
            else:
                  print('doing else ...')
                  uart_port_is_open = True
                  ser.baudrate = 921600
                  # select FIVEBITS, SIXBITS, SEVENBITS or EIGHTBITS of data
                  # ser.bytesize = serial.FIVEBITS
                  # ser.bytesize = serial.SIXBITS
                  # ser.bytesize = serial.SEVENBITS
                  ser.bytesize = serial.EIGHTBITS

                  # select STOPBITS_ONE, STOPBIT_TWO or STOPBITS_ONE_POINT_FIVE
                  ser.stopbits = serial.STOPBITS_ONE
                  # ser.stopbits = serial.STOPBIT_TWO
                  # ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE

                  # select PARITY_NONE, PARITY_EVEN or PARITY_ODD
                  ser.parity = serial.PARITY_NONE
                  # ser.parity = serial.PARITY_EVEN
                  # ser.parity = serial.PARITY_ODD

                  ser.xonxoff = 0
                  ser.rtscts = 0
                  # IF you don't set the timeout for reads the code will hang
                  ser.timeout = 0.5
                  # ser.parity = serial.PARITY_EVEN
                  self.uart_port_is_open = uart_port_is_open
            print(ser)
            return ser

      def init_connection_test(self):
            ser = self.ser
            uart_port_is_open = self.uart_port_is_open
            sram_control_reg = self.sram_control_reg
            regrd_length = self.regrd_length
            regrd_last_data_digit = self.regrd_last_data_digit


            # only continue if the specified UART connection exists
            if uart_port_is_open == True:

                  # Test R15 to see if we can communicate with the FPGA
                  print('Writing R15 with 0x11223344 to test interface')
                  TestData = 'W ' + sram_control_reg + ' 11223344\x0D\x0A'  # write command followed by CRLF
                  ser.write(TestData.encode())
                  TestData = 'R ' + sram_control_reg + ' \x0D\x0A'
                  ser.write(TestData.encode())
                  ResponseData = ser.read(regrd_length).decode()
                  # print('Undecoded:',ser.read(regrd_length).decode())
                  # print('decoded:',ResponseData)
                  # print('Reading R15: ',ResponseData)
                  if ResponseData[:regrd_last_data_digit] == '0xF 0x11223344':
                        print('Register write/read Test Successful')
                        has_connection = True
                  else:
                        print('Register write/read Test Failed!')
                        has_connection = False
                        # has_connection = True
            self.has_connection = has_connection



