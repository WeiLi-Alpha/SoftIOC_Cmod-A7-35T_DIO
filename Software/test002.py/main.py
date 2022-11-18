# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

class ArtyA735T_DIO(object):
    def __init__(self,PORT_NUM):
    super(ArtyA735T_DIO,self).__init__()
        import serial
        import time
        import math
        import sys
        self.xadc_read_reg             = '0'
        self.xadc_write_reg            = '1'
        self.gpio_control_reg          = '2'
        self.iogroup_a_read_reg        = '3'
        self.iogroup_a_write_reg       = '4'
        self.iogroup_b_read_reg        = '5'
        self.iogroup_b_write_reg       = '6'
        self.iopmod_read_reg           = '7'
        self.iopmod_write_reg          = '8'
        self.pwm_prescaler             = '9'
        self.pwm_control_reg           = 'A'
        self.timer_capture_reg         = 'B'
        self.sram_address_reg          = 'C'
        self.sram_data_write_reg       = 'D'
        self.sram_data_read_reg        = 'E'
        self.sram_control_reg          = 'F'

        # Control and Status bit field assignments
        ## Reg0
        self.xadc_temp_ot_alarm_mask   = 0x80000000
        self.xadc_alarm_mask           = 0x7F000000
        self.xadc_read_data_mask       = 0x0000FFFF
        ## Reg1
        self.xadc_wr_bit_mask          = 0x80000000
        self.xadc_address_mask         = 0x01FF0000
        self.xadc_write_data           = 0x0000FFFF
        ## Reg2
        self.io_a_output_enable_mask   = 0x00000001
        self.io_b_output_enable_mask   = 0x00000002
        self.pmod_output_enable_mask   = 0x00000004
        self.enable_mask               = 0x00000007
        ## Reg3, REG4
        self.io_a_data_mask            = 0x001FFFFF
        ## Reg5, REG6
        self.io_b_data_mask            = 0x007FFFFF
        ## Reg7, REG8
        self.pmod_data_mask            = 0x000000FF
        ## Reg9
        self.pwm_red_on_mask           = 0x0000001F
        self.pwm_blue_on_mask          = 0x00001F00
        self.pwm_green_on_mask         = 0x001F0000
        ## Reg10
        self.pwm_prescaler_mask        = 0x0FFFFFFF
        ## Reg11
        self.timer_count_mask          = 0xFFFFFFFF
        ## Reg12
        self.sram_address_mask         = 0x0003FFFF
        ## Reg13, Reg14
        self.sram_data_mask            = 0x000000FF
        ## Reg15

        # Global values
        self.bit_31      = 2147483648
        self.bit_24      = 16777216
        self.bit_16      = 65536
        self.bit_8       = 256
        self.bit_2       = 4
        self.bit_1       = 2
        self.bit_0       = 1

        self.regrd_last_data_digit     = 14
        self.regrd_length              = 15

        self.uart_port = PORT_NUM

    def
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

