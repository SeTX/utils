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
    
    -s "i>b"     -> eval(gzinflate(base64_decode('Code')))
    -s "i>r>b"   -> eval(gzinflate(str_rot13(base64_decode('Code'))))
    -s "i>b>r"   -> eval(gzinflate(base64_decode(str_rot13('Code'))))
    -s "i>b>b>r" -> eval(gzinflate(base64_decode(base64_decode(str_rot13('Code')))))
    -s "u>b"     -> eval(gzuncompress(base64_decode('Code')))
    -s "u>r>b"   -> eval(gzuncompress(str_rot13(base64_decode('Code'))))
    -s "u>b>r"   -> eval(gzuncompress(base64_decode(str_rot13('Code'))))
    -b           -> eval(base64_decode('Code'))
    -s "r>i>b"   -> eval(str_rot13(gzinflate(base64_decode('Code'))))
    -s "i>b>t>r" -> eval(gzinflate(base64_decode(strrev(str_rot13('Code')))))
    -s "i>b>t"   -> eval(gzinflate(base64_decode(strrev('Code'))))
    -s "i>b>r"   -> eval(gzinflate(base64_decode(str_rot13('Code'))))
    -s "i>b>r>t" -> eval(gzinflate(base64_decode(str_rot13(strrev('Code')))))
    -s "b>u>b"   -> eval(base64_decode(gzuncompress(base64_decode('Code'))))
    -s "i>b>l"   -> eval(gzinflate(base64_decode(rawurldecode('Code'))))
"""



from sys import argv, exit
import zlib
import argparse
from urllib import quote, unquote


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
    def rot_13(self, data = None, encode = False):
        """"""
        try:
            if not encode:
                if data:
                    return data.decode("rot_13")
                else:
                    return self.data.decode("rot_13")
            else:
                if data:
                    return data.encode("rot_13")
                else:
                    return self.data.encode("rot_13")
        except Exception, e:
            return '[!] Error Rot_13: %s.' % e
        
    #----------------------------------------------------------------------
    def strrev(self, data = None):
        """"""
        try:
            if data:
                return data[::-1]
            else:
                return self.data[::-1]
        except Exception, e:
            return '[!] Error strrev: %s.' % e
        
    #----------------------------------------------------------------------
    def rawurldecode(self, data = None, encode = False):
        """"""
        try:
            if not encode:
                if data:
                    return unquote(data)
                else:
                    return unquote(self.data)
            else:
                if data:
                    return quote(data)
                else:
                    return quote(self.data)
        except Exception, e:
            return '[!] Error rawurldecode: %s.' % e
    #----------------------------------------------------------------------
    def output_Write(self, output_file, data):
        """Writes the parsed output to file"""
        try:
            f = open(output_file, 'wb')
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
        elif method == 'r':
            return self.rot_13(encode = encode, data = data)
        elif method == 't':
            return self.strrev(data = data)
        elif method == 'l':
            return self.rot_13(encode = encode, data = data)
        else:
            return '[!] Error Sequence: No data recieved as method.'


#----------------------------------------------------------------------
def main(input_data, file, encode = False, xor = False, base64 = False, zlib_gzun = False, hex = False, output_file = None, zlib_gzin = False, sequence = False, rot_13 = False, strrev = False, rawurldecode = False):
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
    elif rot_13:
        if encode:
            out = dec.rot_13(encode = True)
        else:
            out = dec.rot_13()
    elif strrev:
        out = dec.strrev()
    elif rawurldecode:
        if encode:
            out = dec.rawurldecode(encode = True)
        else:
            out = dec.rawurldecode()
    
    if output_file:
        print dec.output_Write(output_file = output_file, data = out)
    else:
        print '[*] Decoder on work...'
        print '*********************************'
        print out
        print '[*] Work Done!'


if __name__ == '__main__':

    
    
    parser = argparse.ArgumentParser(description='Version - Decoder v0.4b', prog='Decoder.py', usage=' Main options \n- %(prog)s [-e] (-s/-b/-i/-u/-x) ( -i data / -f file ) [-o output_file]\n', epilog='Для получения любой информации обращайтесь всё тудаже')
    
    gr1 = parser.add_argument_group('Main Options')
    gr1.add_argument('-f', '--file=', action='store', dest='file', default=None, help='Text file with data to be decoded or encoded')
    gr1.add_argument('-d', '--data=', action='store', dest='input_data', default=None, help='Input data')
    gr1.add_argument('-o', '--output=', action='store', dest='output_file', default=None, help='Output file')
    gr1.add_argument('-e', action='store_true', dest='encode', default=False, help='Encode/compress data, default action is decoding/decompressing')
    gr1.add_argument('-b', action='store_true', dest='base64', default=False, help='Base64 encode/decode method')
    gr1.add_argument('-u', action='store_true', dest='zlib_gzun', default=False, help='Zlib "gzuncompress" compress/decompress method')
    gr1.add_argument('-i', action='store_true', dest='zlib_gzin', default=False, help='Zlib "gzinflate" compress/decompress method')
    gr1.add_argument('-x', action='store_true', dest='hex', default=False, help='Hex encode/decode method')
    gr1.add_argument('-r', action='store_true', dest='rot_13', default=False, help='rot_13 encode/decode method')
    gr1.add_argument('-t', action='store_true', dest='strrev', default=False, help='strrev encode/decode method')
    gr1.add_argument('-l', action='store_true', dest='rawurldecode', default=False, help='rawurldecode encode/decode method')
    gr1.add_argument('-s', action='store', dest='sequence', default=None, help='Decoding sequence e.g.(-s "b>i>b")')
    gr1.add_argument('-v', '--version', action='version', version='%(prog)s v0.3b')
    
    
    
    checkArgs()
    args = parser.parse_args()
    xor = False
    main(args.input_data, args.file, args.encode, xor, args.base64, args.zlib_gzun, args.hex, args.output_file, args.zlib_gzin, args.sequence, args.rot_13, args.strrev, args.rawurldecode)
    


    
    
    