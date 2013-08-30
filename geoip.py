#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Author:  SeTX[X] --<setx [at] s3tx [dot] ru>
# Purpose: 
# Created: 08/30/2013
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
# Note: 
#   1. FreeGeoIP online database is used, there are 10k requests per hour limitation
#   2. As I see, FreeGeoIP support just IPv4
#   3. IP addresses are cheked for version and if malformated
# 

from sys import exit, argv
from os import path
import sys, os
import urllib2
import argparse
#from socket import inet_aton, inet_pton, AF_INET6
import socket
import json

#----------------------------------------------------------------------
def checkArgs():
    """"""
    if len(argv) < 2:
        parser.print_help()
        exit(-1)
        
        
        

########################################################################
class utils:
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        
    #----------------------------------------------------------------------
    def chk_IP(self, ip):
        """Check the IP address version, and if is a molformated"""
        _ip_v4 = None
        _ip_v6 = None
        e_v4 = None
        e_v6 = None
        
        try:
            _ip_v4 = socket.inet_aton(ip)
            return 4
        except Exception, e:
            #print '[!] Error: IP "' + ip + '" is not IPv4 or malformated, check the parser or IP please.\n[!] Error: ' + e
            e_v4 = 'IPv4'
        
        try:
            _ip_v6 = socket.inet_pton(socket.AF_INET6, ip)
            return 6
        except Exception, e:
            #print '[!] Error: IP "' + ip + '" is not IPv6 or malformated, check the parser or IP please.\n[!] Error: ' + e
            e_v6 = 'IPv6'
        
        error =  '[!] Error: IP "' + ip + '" is not ' + e_v4 + ', ' + e_v6 + ' or malformated, check the parser or IP please.\n[!] Error: ' + str(e)
        return error
            
    #----------------------------------------------------------------------
    def get_geo_Data(self, ip):
        """Request Geo data from FreeGeoIP"""
        url = None
        try:
            url = "https://freegeoip.net/json/" + ip
            req = urllib2.urlopen(url)
            if req.getcode() == 200:
                return req.read()
            if req.getcode() == 403:
                print '[!] Error: 403 response has been received on "https://freegeoip.net". \nThe limit is up or there are some problem on the server, trying with "http://freegeoip.net"'
                url = "http://freegeoip.net/json/" + ip
                req = urllib2.urlopen(url)
                if req.getcode() == 200:
                    return req.read()
                else:
                    print '[!] Error: ' + req.getcode() + ' response has been received on "http://freegeoip.net". \nThe limit is up or there are some problem on the server.'
                    exit(-1)
            else:
                print '[!] Error: ' + req.getcode() + ' response has been received on "http://freegeoip.net". \nThe limit is up or there are some problem on the server.'
                exit(-1)
        except Exception, e:
            print '[!] Error: ' + e
            exit(-1)
            
    
    #----------------------------------------------------------------------
    def get_ips_FromFile(self, list_File):
        """
        Prse IP file returning a list with IPs
        """
        ip_list = []
        f = file(list_File, 'r')
        fr = f.readlines()
        for line in fr:
            if line:
                ip_list.append(line.replace('\n','').replace(' ',''))
        
        f.close()
        ip_list = filter(None, ip_list)
        
        return ip_list
    
    #----------------------------------------------------------------------
    def format_json(self, js):
        """Print formated date IP: x.x.x.x Countre: Xxxx Regior: Xxxx City: Xxxx"""
        data = json.loads(js)
        f_data = 'IP: ' + data['ip'] + '\tCountry:(' + data['country_code'] + ') ' + data['country_name'] + '\tRegion: ' + data['region_name'] + '\tCity: ' + data['city']
        return f_data
        
    #----------------------------------------------------------------------
    def output_Write(self, output, data):
        """"""
        
        f = open(output, 'w')
        for line in data:
            f.write(line + '\n')
        f.close()
        

#----------------------------------------------------------------------
def main(ip = None, file = None, output = None):
    """Main function"""

    output_data = []
    chk = None
    line = None
    
    if ip:
        chk = utils().chk_IP(ip)
        if chk == 4:
            json_data = utils().get_geo_Data(ip)
            line = utils().format_json(json_data)
            if output:
                output_data.append(line)
                print line
            else:
                print line
        elif str(chk).startswith('[!] Error:'):
            print chk
            output_data.append(chk)
            
        if output:
            utils().output_Write(output, output_data)
            
    elif file:
        if path.exists(file) and path.isfile(file):
            ip_list = utils().get_ips_FromFile(file)
            for ip in ip_list:
                chk = utils().chk_IP(ip)
                if chk == 4:
                    json_data = utils().get_geo_Data(ip)
                    line = utils().format_json(json_data)
                    if output:
                        output_data.append(line)
                        print line
                    else:
                        print line
                elif str(chk).startswith('[!] Error:'):
                    print chk
                    output_data.append(chk)
            
        if output:
            #print output_data
            utils().output_Write(output, output_data)


if __name__ == '__main__':
      
    parser = argparse.ArgumentParser(description='Version - GeoIP v0.2b', prog='GeoIP.py', usage=' Main options \n- %(prog)s ( -i ip_address / -f file ) [-o output_file]\n', epilog='Для получения любой информации обращайтесь всё тудаже')
    
    gr1 = parser.add_argument_group('Main Options')
    gr1.add_argument('-f', '--file=', action='store', dest='ip_list_file', default=None, help='Text file with list of IP addresses to be parsed')
    gr1.add_argument('-i', '--ip=', action='store', dest='ip_address', default=None, help='IP addres')
    gr1.add_argument('-o', '--output=', action='store', dest='output_file', default=None, help='Output file')
    gr1.add_argument('-v', '--version', action='version', version='%(prog)s v0.1.1a')
  
    checkArgs()
    args = parser.parse_args()
    
    if args.ip_address:
        main(ip = args.ip_address, output = args.output_file)
    if args.ip_list_file:
        main(file = args.ip_list_file, output = args.output_file)
    
    print '[*] Work Done!'