#!/usr/bin/env python
# -*- coding: utf-8 -*-

import click
import os
import cv2
import numpy as np
#from . import _proc


class Color:
    def __init__(self):
        pass

    def from_hex(self, hexstring:str):
        self.r = 00
        self.g = 00
        self.b = 00
        self.hex = hexstring
        self._proc_hex()
        self.bgr_array = [self.b, self.g, self.r]
        self.rgb_array = [self.r,self.g,self.b]

    def from_rgb(self, r:int, g:int, b:int):
        self.r = r
        self.g = g
        self.b = b
        self.hex = ''
        self.bgr_array = [self.b, self.g, self.r]
        self.rgb_array = [self.r,self.g,self.b]
    
    def _proc_hex(self):
        try:
            string = self.hex
            self.b =int( string[-2:],16)
            self.g =int( string[2:-2],16)
            self.r =int( string[:2],16)
        except ValueError:
            print(f"Error parsing hex string {self.hex}, please enter hex string in format: #000000.")
            raise Exception


def create_wallpaper(resolution: list[int], color: Color):
    res = [resolution[1],resolution[0],3]
    img = np.full(res, color.bgr_array)
    return img


DEFAULT_PATH = os.path.expanduser('~/flatwall/wallpaper.png')

@click.command()
@click.option('--hexstr', '-x', help='The hex value of the color prefixed with a \'#\'.', type=str )
@click.option('--rgb', help='RGB values for color in format: \'RR GG BB\'. Note: must include quotes.')
@click.option('--resolution', '-r', help="Screen Resolution in format: 1920x1080.", type=str, default='1920x1080')
@click.option('--output', '-o', help='Path to output file. Default: ~/flatwall/wallpaper.png',type=str,default=DEFAULT_PATH)
def main(hexstr,resolution,output,rgb):
    click.echo("Thank you for using flatwall!")
    
    # Check Resolution - Use default
    try:
        resolution = [int(val) for val in resolution.split('x')]

    except ValueError as ve:
        print(f"Incorrect format for Resolution, should match the following example: 1920x1080")
        return
    
    # Check if color is valid
    color = Color()
    if hexstr == None and rgb == None:
        print('Please specify a color for the wallpaper. Use options -x or --rgb, and see --help for more information.')
        return

    elif hexstr != None and rgb != None:
        print("Please enter only one color format, use either the -x/--hexstr format or the --rgb format. See --help for more information.")
        return

    elif hexstr != None:
        hexstr = hexstr.strip('#')

        if len(hexstr) != 6:
            print('Hex color format is incorrect, please use format: #000000.')
            return

        color.from_hex(hexstr)
    
    elif rgb != None:
        rgb = rgb.split(' ')
        if len(rgb)!= 3:
            print('RGB color format incorrect, please use format: \'RR GG BB\'.')
            return
        try:
            r,g,b = [int(num) for num in rgb]
        except ValueError:
            print('RGB color format incorrect, please use format: \'RR GG BB\'.')
            return

        color.from_rgb(r,g,b)


    #Check Settings:
    print('Wallpaper Info:')
    print(f'    Resolution: {resolution[0]}x{resolution[1]}')
    print(f'    Color (RGB): {color.rgb_array}')
    print('')


    # Create wallpaper
    wallpaper = create_wallpaper(resolution, color)
    # Find and check path for output

    path = output[:output.rindex('/')]

    if not os.path.exists(path):
        if (check := input(f'Chosen path {path} does not exist, would you like to create it? (y/n): ')) == 'y':
            pass
        elif check=='n':
            return
        else:
            return
        print(f'Creating path: {path}')
        os.mkdir(path)


    # Save wallpaper
    
    if not cv2.imwrite(output, wallpaper):
        print('There was an error writing the wallpaper to the given path.')
        return
    else:
        print('Wallpaper Sucessfully Generated!')
        print(f'    Wallpaper can be found here: {output}')




if __name__=="__main__":
    main()
