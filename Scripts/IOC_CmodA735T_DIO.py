#!/usr/bin/env python3

from softioc import softioc, builder, asyncio_dispatcher
import asyncio
import time
import CmodA735T_DIO

usb_port = '/dev/ttyUSB1'
board = CmodA735T_DIO.CMODA7(usb_port)

# Create an asyncio dispatcher, the event loop is now running
dispatcher = asyncio_dispatcher.AsyncioDispatcher()

# Set the record prefix
builder.SetDeviceName("CMODA7-35T")

# createOut is used to create boolOut, can be used to create a series of database
# board     board connected to the usb_port
# P         group of pins on the board, can be 'A','B','P'
# i         index of the pin number in the group, start with 0
#           A:0-20,  B:0-22,  P:0-7
def createOut(board,P,i):
    return builder.boolOut(P+str(i)+":OUT", ZNAM="OFF", ONAM="ON", initial_value=board.get_gpio_pin(P,i), \
                           always_update=True,on_update=lambda v:board.set_gpio_pin(P,i,v))
def createOut_Read(board,P,i):
    return builder.boolIn(P+str(i)+":OUT:READ", ZNAM="OFF", ONAM="ON", initial_value=board.get_gpio_pin(P,i))

n_pin_A = 21
n_pin_B = 23
n_pin_P = 8

AOUT = [0]*n_pin_A
BOUT = [0]*n_pin_B
POUT = [0]*n_pin_P
AOUT_READ = [0]*n_pin_A
BOUT_READ = [0]*n_pin_B
POUT_READ = [0]*n_pin_P
for i in range(n_pin_A):
    AOUT[i] = createOut(board,'A',i)
    AOUT_READ[i] = createOut_Read(board, 'A', i)
for i in range(n_pin_B):
    BOUT[i] = createOut(board,'B',i)
    BOUT_READ[i] = createOut_Read(board, 'B', i)
for i in range(n_pin_P):
    POUT[i] = createOut(board,'P',i)
    POUT_READ[i] = createOut_Read(board, 'P', i)

builder.LoadDatabase()
softioc.iocInit(dispatcher)

async def update():
    while True:
        for i in range(n_pin_A):
            AOUT_READ[i].set(board.get_gpio_pin('A',i))
        for i in range(n_pin_B):
            BOUT_READ[i].set(board.get_gpio_pin('B',i))                
        for i in range(n_pin_P):
            POUT_READ[i].set(board.get_gpio_pin('P',i))
        await asyncio.sleep(1)


dispatcher(update)

softioc.interactive_ioc(globals())
