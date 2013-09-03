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
"""
    Tipical and most used combinations
    
    eval(gzinflate(base64_decode('Code')))
    eval(gzinflate(str_rot13(base64_decode('Code'))))
    eval(gzinflate(base64_decode(str_rot13('Code'))))
    eval(gzinflate(base64_decode(base64_decode(str_rot13('Code')))))
    eval(gzuncompress(base64_decode('Code')))
    eval(gzuncompress(str_rot13(base64_decode('Code'))))
    eval(gzuncompress(base64_decode(str_rot13('Code'))))
    eval(base64_decode('Code'))
    eval(str_rot13(gzinflate(base64_decode('Code'))))
    eval(gzinflate(base64_decode(strrev(str_rot13('Code')))))
    eval(gzinflate(base64_decode(strrev('Code'))))
    eval(gzinflate(base64_decode(str_rot13('Code'))))
    eval(gzinflate(base64_decode(str_rot13(strrev('Code')))))
    eval(base64_decode(gzuncompress(base64_decode('Code'))))
    eval(gzinflate(base64_decode(rawurldecode('Code'))))
"""



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
    def __init__(self, input_data = None, file = False):
        """Constructor"""
        
        if file:
            f = open(file, 'rb')
            self.data = f.read()
            f.close()
            
        elif input_data:
            self.data = input_data
        else:
            return None
        
    
    #----------------------------------------------------------------------
    def base64(self, data = None, encode = False):
        """Return the encoded or decoded in Base64, string or file data"""
        try:
            if not encode:
                if data:
                    return data.decode("base64")
                else:
                    return self.data.decode("base64")
            else:
                if data:
                    return data.encode("base64")
                else:
                    return self.data.encode("base64")
        except Exception, e:
            return '[!] Error Base64: %s.' % e
        
        
    #----------------------------------------------------------------------
    def zlib_gzun(self, compress = False, data = None):
        """Return the compressed or decompressed with Zlib, string or file data"""
        if not compress:
            try:
                if data:
                    return zlib.decompress(data)
                else:
                    return zlib.decompress(self.data)
            except Exception, e:
                return '[!] Error Zlib decompress: %s.' % e
        else:
            try:
                if data:
                    return zlib.compress(data)
                else:
                    return zlib.compress(self.data)
            except Exception, e:
                return '[!] Error Zlib compress: %s.' % e
            
    #----------------------------------------------------------------------
    def zlib_gzin(self, compress = False, data = None):
        """Return the compressed or decompressed object with Zlib, string or file data"""
        if not compress:
            try:
                if data:
                    return zlib.decompressobj().decompress('x\x9c' + data)
                else:
                    return zlib.decompressobj().decompress('x\x9c' + self.data)
            except Exception, e:
                return '[!] Error Zlib inflate decompress: %s.' % e
        else:
            try:
                if data:
                    return ((zlib.compress(data))[2:])[:-4]
                else:
                    return ((zlib.compress(self.data))[2:])[:-4]
            except Exception, e:
                return '[!] Error Zlib inflate compress: %s.' % e
                    
        
    #----------------------------------------------------------------------
    def hex(self, encode = False, data = None):
        """Return the encoded or decoded in Hex, string or file data"""
        
        out = ""
        
        if data:
            if data.upper().startswith('0X'):
                array = data.split('0x')
                array = filter(None, array)
                for char in array:
                    out += char
            else:
                out = data
        else:
            if self.data.upper().startswith('0X'):
                array = self.data.split('0x')
                array = filter(None, array)
                for char in array:
                    out += char
            else:
                out = self.data
        
        if not encode:
            try:
                return out.decode("hex")
            except Exception, e:
                return '[!] Error HEX decoding: %s.' % e
        else:
            try:
                return out.encode("hex")
            except Exception, e:
                return '[!] Error HEX encoding: %s.' % e
            
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
    def sequence(self, sequence, encode = False):
        """
        Parses sequence of methods to be applied
        e.g.
        b>i>b
        Base64(data) then Zlib_inflate(data) and then another Base64(date) 
        methods will be applied
        """
        array = []
        
        try:
            out = self.data
            array = filter(None, sequence.split('>'))
            for method in array:
                out = self.wrapper(method = method, data = out, encode = encode)
            return out
        except Exception, e:
            return '[!] Error Sequence: %s.' % e
        
    #----------------------------------------------------------------------
    def wrapper(self, method, data = None, encode = False):
        """Returns the parsed data with the function according to the indicated method"""
        if method == 'b':
            return self.base64(data = data, encode = encode)
        elif method == 'i':
            return self.zlib_gzin(compress = encode, data = data)
        elif method == 'u':
            return self.zlib_gzun(compress = encode, data = data)
        elif method == 'x':
            return self.hex(encode = encode, data = data)
        else:
            return '[!] Error Sequence: No data recieved as method.'


#----------------------------------------------------------------------
def main(input_data, file, encode = False, xor = False, base64 = False, zlib_gzun = False, hex = False, output_file = None, zlib_gzin = False, sequence = False):
    """Simple main function"""

    out = ''
    
    if input_data:
        dec = decoder(input_data = input_data)
    elif file:
        dec = decoder(file = file)
    else:
        print '[!] Error Input Data: The data is not specified.'
        exit(-1)
    
    if xor:
        print ' [!] Error: Not yet support.'
        exit(0)
    elif sequence:
        out = dec.sequence(sequence, encode = encode)
    elif base64:
        if encode:
            out = dec.base64(encode = True)
        else:
            out = dec.base64()
    elif zlib_gzun:
        if encode:
            out = dec.zlib_gzun(encode = True)
        else:
            out = dec.zlib_gzun()
    elif zlib_gzin:
        if encode:
            out = dec.zlib_gzin(encode = True)
        else:
            out = dec.zlib_gzin()
    elif hex:
        if encode:
            out = dec.hex(encode = True)
        else:
            out = dec.hex()
        
    
    if output_file:
        print dec.output_Write(output_file = output_file, data = out)
    else:
        print '[*] Decoder on work...'
        print '*********************************'
        print out
        print '[*] Work Done!'


if __name__ == '__main__':

    
    
    parser = argparse.ArgumentParser(description='Version - Decoder v0.3b', prog='Decoder.py', usage=' Main options \n- %(prog)s [-e] (-s/-b/-i/-u/-x) ( -i data / -f file ) [-o output_file]\n', epilog='Для получения любой информации обращайтесь всё тудаже')
    
    gr1 = parser.add_argument_group('Main Options')
    gr1.add_argument('-f', '--file=', action='store', dest='file', default=None, help='Text file with data to be decoded or encoded')
    gr1.add_argument('-d', '--data=', action='store', dest='input_data', default=None, help='Input data')
    gr1.add_argument('-o', '--output=', action='store', dest='output_file', default=None, help='Output file')
    gr1.add_argument('-e', action='store_true', dest='encode', default=False, help='Encode/compress data, default action is decoding/decompressing')
    gr1.add_argument('-b', action='store_true', dest='base64', default=False, help='Base64 encode/decode method')
    gr1.add_argument('-u', action='store_true', dest='zlib_gzun', default=False, help='Zlib "gzuncompress" compress/decompress method')
    gr1.add_argument('-i', action='store_true', dest='zlib_gzin', default=False, help='Zlib "gzinflate" compress/decompress method')
    gr1.add_argument('-x', action='store_true', dest='hex', default=False, help='Hex encode/decode method')
    gr1.add_argument('-s', action='store', dest='sequence', default=None, help='Decoding sequence e.g.(-s "b>i>b")')
    gr1.add_argument('-v', '--version', action='version', version='%(prog)s v0.3b')

    checkArgs()
    args = parser.parse_args()
    
    main(input_data = args.input_data, file = args.file, encode = args.encode, xor = False, base64 = args.base64, zlib_gzun = args.zlib_gzun, hex = args.hex, output_file = args.output_file, zlib_gzin = args.zlib_gzin, sequence = args.sequence)
    


    
    
    