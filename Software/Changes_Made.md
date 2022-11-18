## Changes made to the .vhd file

- change the condition of enable

Note:
- Group A GPIO has 21 pins, i.e. the maximum input number is $2^21-1$ or `1FFFFF`. 
  The pin sequence is [1:14 17:23].
- Group B GPIO has 23 pins, i.e. the maximum input number is $2^23-1$ or `7FFFFF`.
  The pin sequence is [48:35 32:25 33:34].

## changes made in the C7Test.py to make it work with Python3.

1. Change codes related to the `serial` module:

The `serial` module in python2 and python3 is slightly different, to 
make it work in python3, we need to make changes to `ser.write` and 
`ser.read`. Also the `raw_input` should be replaced with `input` in
python3.
 - replace all the `ser.write(TestData)` with `ser.write(TestData.encode())` 
 - replace all the `ser.read(regrd_length)` with `ser.read(regrd_length).decode()`
 - replace all the `raw_input` with `input`.

2. Allow enabling both GPIO group A and group B (each group represents the GPIO 
  pins on each side).
- in `print_cmds`, after `if uart_port_is_open=True`, change the following lines 
``` 
c = input('Enable IO Group B Outputs? <y/n> => ')
if c == 'y':
  x = bit_1
```
to 
```
c = input('Enable IO Group B Outputs? <y/n> => ')
if c == 'y':
  x = x + bit_1
```

3. Change the serial port definition

Change 
`uart_port = 'COM34'` to the correct uart port, in my case it's `uart_port = 'COM12'`.
also change `cmd_line_options = get_options(sys.argv)` to `cmd_line_options = uart_port`. 


4. Add `return x` by the end of function `show_enables`, so that the current status can
   be read for configuration.

5. add function `get_gpio(p)`


## Program configuration flash
1. Export the `.bit` file
- File => Export => Export bitstream file 
- Enter the filename to be saved.

Check the sie of the bit file, to check that it's smaller than the 
size of the flash memory. If not, try to generate a smaller compressed
`.bit` file. For example, the flash memory size of 
CmodA7 35T is 4M, the available memory is about 2M, a `.bit` file larger
than 2M might fail to be programed to the board.

Generate compressed `.bit` file as follows:
- click the  `Settings` button, which is on the top of the left 
 `Flow Nevigation` pannel.
- `Bitstream`, check on `-bin_file*`
- click on `Configure additional bitstream settings`, change
    `Enable Bitstream Compresssion` to `TRUE`.
- Press `OK`.

Press `Generate Bitstream`, until finished. Then, `export`.

2. Generate memory configuration file 
- Tool => Generate memory configuration file
- Format: MSC 
- Memory part: choose the part of your device 
  - information can be found online;
  - if set wrong, the error message should report the 
    correct part number, then do it again. 
  - The memory part number of my Cmod A7-35T board was 
    found online as [MX25L3233F], see [here](https://digilent.com/reference/programmable-logic/cmod-a7/reference-manual?redirect=1)
    the part number of `Macronix`. 
- Filename: select directory and filename to save, forexample: boot.mcs 
- check `Load bitstream file`
- Bitfile: select the `.bit` file exported.
- Check the boxes of `Overwrite`, 

3. Program the flash
- Open hardware manager and connect to the hardware.
- right click the memory part number [mx25l3233f in my case].
- click `Program Configuration Memory Deviec`
- Configuration file: select the `.mcs` file generated;
- Address range: choose `Entire Configuration Memory Device`
- check boxes of `Erase`,`Program`, and `Veryfy`
- click `OK`

4. In the `Hardware Manager` panel

Click "Program Device".

Then the program will be run automatically uppon power on.



