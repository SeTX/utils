#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Author:  SeTX[X] --<setx [at] s3tx [dot] ru>
# Purpose: Data decoder
# Created: 09/02/2013
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 2 of the License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#


from sys import argv, exit
import zlib
import argparse



#----------------------------------------------------------------------
def checkArgs():
    """"""
    if len(argv) < 2:
        parser.print_help()
        exit(-1)


########################################################################
class decoder:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, input_data = False, file = False):
        """Constructor"""
        
        if file:
            f = open(file, 'r')
            self.data = f.read()
            f.close()
        elif input_data:
            self.data = input_data
        else:
            return None
        
    
    #----------------------------------------------------------------------
    def base64(self):
        """Return the encoded or decoded in Base64, string or file data"""
        try:
            return self.data.decode("base64")
        except Exception, e:
            return '[!] Error Base64: %s.' % e
        
        
    #----------------------------------------------------------------------
    def zlib(self, decompress = False):
        """Return the compressed or decompressed with Zlib, string or file data"""
        if decompress:
            try:
                return zlib.decompress(self.data)
            except Exception, e:
                return '[!] Error Zlib decompress: %s.' % e
        else:
            try:
                return zlib.compress(self.data)
            except Exception, e:
                return '[!] Error Zlib compress: %s.' % e
            
    #----------------------------------------------------------------------
    def hex(self, decode = False):
        """Return the encoded or decoded in Hex, string or file data"""
        
        data = ""
        
        if self.data.upper().startswith('0X'):
            array = self.data.split('0x')
            array = filter(None, array)
            for char in array:
                data += char
        else:
            data = self.data
        
        if decode:
            try:
                return data.decode("hex")
            except Exception, e:
                return '[!] Error HEX encoding: %s.' % e
        else:
            try:
                return data.encode("hex")
            except Exception, e:
                return '[!] Error HEX decoding: %s.' % e
            
    #----------------------------------------------------------------------
    def output_Write(self, output_file, data):
        """Writes the parsed output to file"""
        try:
            f = open(output_file, 'w')
            f.write(data)
            f.close
            return '[*] Work Done! File "%s" has been saved.' % output_file
        except Exception, e:
            return '[!] Error Output Write: %s.' % e
        
        


#----------------------------------------------------------------------
def main(input_data, file, encode, xor = False, base64 = False, zlib = False, hex = False, output_file = None):
    """Simple main function"""
    
    if input_data:
        dec = decoder(input_data = input_data)
    elif file:
        dec = decoder(file = file)
    else:
        print '[!] Error Input Data: The data is not specified.'
        
    if xor:
        print ' [!] Error: Not yet support.'
        exit(0)
    elif base64:
        out = dec.base64()
    elif zlib:
        if encode:
            out = dec.zlib()
        else:
            out = dec.zlib(decompress = True)
    elif hex:
        if encode:
            out = dec.hex()
        else:
            out = dec.hex(decode = True)
    
        
    
    if output_file:
        print dec.output_Write(output_file = output_file, data = out)
    else:
        print out
    


if __name__ == '__main__':

    #print '[*] Decoder on work...'
    #print '*********************************'
    
    parser = argparse.ArgumentParser(description='Version - Decoder v0.2b', prog='Decoder.py', usage=' Main options \n- %(prog)s [-e] (-b/-z/-x) ( -i data / -f file ) [-o output_file]\n', epilog='Для получения любой информации обращайтесь всё тудаже')
    
    gr1 = parser.add_argument_group('Main Options')
    gr1.add_argument('-f', '--file=', action='store', dest='file', default=None, help='Text file with data to be decoded or encoded')
    gr1.add_argument('-i', '--input=', action='store', dest='input_data', default=None, help='Input data')
    gr1.add_argument('-o', '--output=', action='store', dest='output_file', default=None, help='Output file')
    gr1.add_argument('-e', action='store_true', dest='encode', default=False, help='Encode/compress data, default action is decoding/decompressing')
    gr1.add_argument('-b', action='store_true', dest='base64', default=False, help='Base64 encode/decode method')
    gr1.add_argument('-z', action='store_true', dest='zlib', default=False, help='Zlib compress/decompress method')
    gr1.add_argument('-x', action='store_true', dest='hex', default=False, help='Hex encode/decode method')
    gr1.add_argument('-v', '--version', action='version', version='%(prog)s v0.2b')

    checkArgs()
    args = parser.parse_args()
    
    main(input_data = args.input_data, file = args.file, encode = args.encode, xor = False, base64 = args.base64, zlib = args.zlib, hex = args.hex, output_file = args.output_file)
    
    #print '[*] Work Done!'
    
    
    
    