#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# Author:  SeTX[X] --<setx [at] s3tx [dot] ru>
# Purpose: IP Geo parser (Supports IPv4 and IPv6)
# Created: 07/22/2013
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
#  Dependences:
#    - No dependeces, just native modules
#

from sys import argv, exit
from os import path, mkdir

import csv
import socket
import urllib2
import argparse
import gzip
from binascii import hexlify
from datetime import datetime


#----------------------------------------------------------------------
def checkArgs():
    """"""
    if len(argv) < 2:
        parser.print_help()
        exit()

        
        
########################################################################
class main:
    """"""

    #----------------------------------------------------------------------
    def __init__(self, db_File = None):
        """Constructor
        Do some checks
        if folder "geoVault" is exist
        if db file is there
        """
        __path = './geoVault'
        #__t_path = __path + '_'
        t = None
        
        if path.exists(__path):
            if path.isdir(__path):
                print '[+] The folder "geoVault" is already created'
            else:
                mkdir(__t_path)
                print '[+] The folder "geoVault_" have been created'
        else:
            mkdir(__path)
            print '[+] The folder "geoVault" have been created'
    
        
        self.dbPath = db_File
        if not db_File:
            
            __y = datetime.today().strftime('%Y')
            __m = datetime.today().strftime('%m')
            db_file_Name = '/dbip-country-' + __y + '-' + __m + '.csv'
            out_File = db_file_Name + '.gz'
            db_url = 'http://download.db-ip.com/free' + out_File
            
            
            if path.exists(__path + '' + db_file_Name):
                self.dbPath = __path + '' + db_file_Name
                print '[+] The DB file si already here in ' + __path
            else:
                req = urllib2.urlopen(db_url)
                output_File = file(__path + '' + out_File, 'wb')
                output_File.write(req.read())
                output_File.close()
                
                gz_content = gzip.open(__path + '' + out_File, 'rb')
                f = file(__path + '' + db_file_Name, 'wb')
                f.write(gz_content.read())
                f.close
                gz_content.close()
                self.dbPath = __path + '' + db_file_Name
                print '[+] The DB file have been downloaded to ' + __path
        
        


    #----------------------------------------------------------------------
    def get_DB(self, csvFile):
        """
        Parse csv file with DB list, returning a list
        """
        db = []
        with open(csvFile, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                db_line = row[0].replace('"','').split(',')
                db.append(db_line)
                #print db_line
        return db
    
    #----------------------------------------------------------------------
    def get_IPs(self, list_File):
        """
        Prse IP file returning a list with IPs
        """
        ip_list = []
        f = file(list_File, 'r')
        fr = f.readlines()
        #print fr
        for line in fr:
            if line:
                ip_list.append(line.replace('\n','').replace(' ',''))
                #get_geoLoc(line)
        
        f.close()
        return ip_list
    
    
    #----------------------------------------------------------------------
    def get_Geo(self, list_File):
        """
        IP list file is parsed and get the list
        DB file is parsed and get the list
        str IP data is Parsed
        Search in all lines of db list
        
        """
        ip_list = self.get_IPs(list_File)
        db_list = self.get_DB(self.dbPath)
        for ip in ip_list:
            try:
                _ip_v4 = int(hexlify(socket.inet_aton(ip)), 16)
            except Exception, e:
                _ip_v6 = int(hexlify(socket.inet_pton(socket.AF_INET6, ip)), 16)
            except:
                print '[!] Error: IP "' + ip + '" malformated, check the parser please..!!!'
                break
            
            if _ip_v4:
                for db_line in db_list:
                    if db_line[0].find(":") == -1:
                        ip_start = int(hexlify(socket.inet_aton(db_line[0])), 16)
                        ip_stop = int(hexlify(socket.inet_aton(db_line[1])), 16)
                        if ip_start <= _ip_v4 <= ip_stop:
                            #if IPAddress(db_line[0]) <= IPAddress(ip) <= IPAddress(db_line[1]):
                            print 'IP: ' + ip + ': \tRange (' + db_line[0] + ' - ' + db_line[1] + ') \tCountry: ' + db_line[2]
                            break
            elif _ip_v6:
                if db_line[0].find(":") == 1:
                    ip_start = int(hexlify(socket.inet_pton(socket.AF_INET6, db_line[0])), 16)
                    ip_stop = int(hexlify(socket.inet_pton(socket.AF_INET6, db_line[1])), 16)
                    if ip_start <= _ip_v6 <= ip_stop:
                            #if IPAddress(db_line[0]) <= IPAddress(ip) <= IPAddress(db_line[1]):
                            print 'IP: ' + ip + ': \tRange (' + db_line[0] + ' - ' + db_line[1] + ') \tCountry: ' + db_line[2]
                            break
    
    


if __name__ == '__main__':
      
    parser = argparse.ArgumentParser(description='Version - IP Geo Looker v0.1', prog='IPGeoLooker.py', usage=' Main options \n- %(prog)s -f (file)\n', epilog='Для получения любой информации обращайтесь всё тудаже')
    
    gr1 = parser.add_argument_group('Main Options')
    gr1.add_argument('-f', '--file', action='store', dest='ip_List', default=None, help='Text file with IP list to be parsed')
    gr1.add_argument('-d', '--db', action='store', dest='db_File', default=None, help='The DB CSV file downloaded from http://db-ip.com/')
    gr1.add_argument('-v', '--version', action='version', version='%(prog)s v0.1.1a')
  
    checkArgs()
    args = parser.parse_args()
    
    m = main(args.db_File)
    m.get_Geo(args.ip_List)

    
