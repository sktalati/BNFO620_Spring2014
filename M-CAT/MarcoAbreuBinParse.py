#__author__ = 'Marco Abreu'
from __future__ import division
import subprocess
import sys
import os
import re
from MCATpipline import B2_PLAN
#import argparse


Source = '/home/bnfo620/M-CAT/sampledata/simulatddata/1x/'
Source_Index1 = '/home/bnfo620/M-CAT/All_Bacteria_1'
Source_Index2 = '/home/bnfo620/M-CAT/All_Bacteria_2'
Results_to = os.getcwd()+"/"
samtools = '/home/bnfo620/bin/samtools'
Bin_Size = 1000
#GenSource = "/home/bnfo620/M-CAT"
#Source = ""
#Results_to = os.getcwd()
### program as arguments accepts the directory with flagstat files and a filename to be written to
try:
    if len(sys.argv)<2:
        print "USAGE: python sys.argv[0] [location and RefGenome] [location and Dump_file] [location refgenome] [location of index1] [location if index2]\n",
        print "Attempting default value test parameters...."
        #GenSource = 'C:/Users/Owner/PycharmProjects/Homework/mcattest.txt'
        #Dump = 'C:/Users/Owner/PycharmProjects/Homework/dump.txt'
        #GenSource = 'C:/Users/bccl_user/Desktop/Bnfo691_602/testgenome.txt'
        #Dump = 'C:/Users/bccl_user/Desktop/Bnfo691_602/dump.txt'
        #Results_to = ''
        #GenSource = "/home/bnfo620/M-CAT/All_Bacteria_clean_test.fna"
        #Dump = "/home/bnfo620/M-CAT/gi_taxid_nucl.dmp"
        GenSource = "/home/bnfo620/M-CAT/test/All_Bacteria_clean_test.fna"
        #Dump = "/home/bnfo620/M-CAT/test/gi_taxid_nucl_test.dmp"
        Dump = "/home/abreuma/dump.txt"
    else:
        GenSource = sys.argv[1]
        Dump = sys.argv[2]
        Source = sys.argv[3]
        Source_Index1 = sys.argv[4]
        Source_Index2 = sys.argv[5]
        #Results_to = sys.argv[2]
except IOError:
    print "Error in input"
print "Source: ",GenSource, "\n", Dump

#Takein arguments from commandline, and run script which runs 3 programs

def TaxID_to_GI(Dump):
    print "TaxIN to gi...START",
    f =open(Dump)
    dump_hash = {}
    #print "process lines"
    count = 0
    for line in f:
        #print 'x',line
        gi, tax_id = line.split()
        #print 'g',gi,tax_id,count,count%10000
        if int(tax_id) not in dump_hash.keys():
            dump_hash[int(tax_id)] = {}
            dump_hash[int(tax_id)][int(gi)]={}
        else:
            dump_hash[int(tax_id)][int(gi)]={}
        count +=1
        clock = count%250000
        if clock == 1:
            print "Lines read",count
    print "TaxID_to_GI...END\n"
    #print dump_hash
    return dump_hash

def Genome_Binner(dump_hash,GenSource, Bin_Size = 1000):
    print "Genome_Binner... START",
    f =open(str(GenSource))
    Gen_Bin_Array = []
    sequence_count = 0
    Genome_name = ""
    for line in f:
        if line[0] == ">":
            #print sequence_count
            if sequence_count != 0:
                bin = Scount_bin(sequence_count,Bin_Size)
                Gen_Bin_Array.append([Genome_name,sequence_count])
                #print "HERE!!!",dump_hash
                for key in dump_hash.keys():
                    #print "Key",key,dump_hash[key],":",Genome_name
                    if Genome_name in dump_hash[key]:
                        #print "test:",key, Genome_name,bin
                        dump_hash[key][Genome_name]=bin
                    else:
                        pass
            sequence_count = 0
            temp = line.split("|")
            Genome_name = int(temp[1])
        else:
            Gen_Bin_Array=[] #reset to 0
            sequence_count += len(line)
            #Gen_Bin_Array.append([Genome_name,sequence_count])
        #print Gen_Bin_Array
    print "Genome_Binner...END\n"
    #outfileprint(dump_hash)
    #print dump_hash
    return dump_hash

def Scount_bin(counts, size):
    bin={}
    bin_number = float(float(counts)/float(size))
    bin_flag=0
    #print "Sbin",bin_number
    if bin_number >= 1:
        remainder = bin_number-int(bin_number)
        if remainder >= .5:
            bin_number=int(bin_number)+1
            bin_flag = 1
        else:
            bin_number=int(bin_number)
        for i in xrange(bin_number):
            if i==bin_number-1 and bin_flag == 0:
                bin[i]=[0,str(str(i*size)+"-"+str(((i+1)*size)-1))]
                bin[i]=[0,str(str((i)*size)+"-"+str(((i+1)*size)+int(remainder*size)))]

            elif i==bin_number-1 and bin_flag == 1:
                bin[i]=[0,str(str(i*size)+"-"+str(((i+1)*size)-1))]
                bin[i+1]=[0,str(str((i+1)*size)+"-"+str(((i+1)*size)+int(remainder*size)))]
            elif i == 0:
                bin[i]=[0,str(str(i*size)+"-"+str((size)-1))]
            else:
                bin[i]=[0,str(str(i*size)+"-"+str(((i+1)*size)-1))]
    else:
        bin[0]=[0,str("0-"+str(counts)),counts]
        #print bin
    return bin



def TaxID_gi_bin_hasher(Dump,GenSource, Bin_Size=1000):
    print "TaxID_gi_bin_Hasher... START\n",
    if 'MarcoAbreuResult.txt' not in os.listdir(str(os.getcwd()+"/")):
        Hash = TaxID_to_GI(Dump) #hash[gi]=tax id
        taxID_bins = Genome_Binner(Hash,GenSource) #gi_num, sequence length
        outfileprint(taxID_bins)
    else:
        print "Results already exist:", 'MarcoAbreuResult.txt'


def fileProcess(Source):
    for filename in os.listdir(Source):
        print "filename:", filename

def fileParse(file):
    pass

def outfileprint(Hash): #Test by printing created outfile
    #f =open(str(os.getcwd()+"/MarcoAbreuResult.txt"))
    outFile = open('MarcoAbreuResult.txt','w')
    toString = "TaxID\tGiNumber\tBin\tBin Range\tCount\n"
    for key in sorted(Hash.keys()):
        for key1 in sorted(Hash[key].keys()):
            for key2 in sorted(Hash[key][key1].keys()):
                toString += str(key)+"\t"+str(key1)+"\t"+str(key2)+"\t"+str(Hash[key][key1][key2][1])+"\t"+str(Hash[key][key1][key2][0])+"\n"
    print "Write...",
    outFile.write(toString)
    print "Close", outFile
    outFile.close()
    return "Write Complete"

def refined_hash(hash_source=""):
    hash_source=open('MarcoAbreuResult.txt')
    f=hash_source
    tax_list = []
    tax_hash = {}
    count = 1
    for line in f:
        if count == 1:
            pass
        else:
            #print 'line',line
            seg = line.split('\t')
            #print seg[0],seg[1],seg[2]
            taxID = int(seg[0])
            giID = int(seg[1])
            binNum = str(seg[2])
            if str(taxID) not in tax_list:
                tax_list.append(str(taxID))
                tax_hash[taxID]={}
                tax_hash[taxID][giID]=[0]
            elif giID not in tax_hash[taxID].keys():
                tax_hash[taxID][giID].append(0)
            else:
                tax_hash[taxID][giID].append(0)
        count +=1
    return tax_hash


def SAMREADER(Hash,thresh=3):
    for filename in os.listdir(str(os.getcwd()+"/")):
        name_end = filename[len(filename)-8:]
        list = []
        #print filename
        if name_end == 'CSAM.sam':
            f = open(os.getcwd()+"/"+filename)
            print "SAMREADER READS:",filename
            i = 0
            cline = ""
            for line in f:
                #print line
                if line[:2] == 'gi':
                    cline=line+cline
                    if len(cline) > 125:
                        #try:
                        #print cline
                        try:
                            ginum,taxnum,score,start_pos = giRead(cline)
                        except TypeError:
                            ginum,taxnum,score,start_pos=0,0,0,0
                        #print ginum
                        #if ginum == str(164421336) and str(240016) in Hash.keys():
                        #    temp = int(int(start_pos)/1000)
                        #    print ginum,score,start_pos,temp
                            #print ginum,score,start_pos,int(start_pos/1000)
                            #return

                        for key in Hash.keys():
                            #print "Present",key,ginum
                            if int(ginum) in Hash[int(key)].keys():
                                print "Present",key,ginum,len(Hash[key][ginum]),Hash[key][ginum]
                                bins=int(int(start_pos)/Bin_Size)
                                #print "Present",key,ginum,bins,Hash[key]
                                #bins=int(start_pos/Bin_Size)
                                #Hash[key][int(ginum)][bins].append([score,taxnum])
                                #Hash[key][int(ginum)][bins].update
                                Hash[key][int(ginum)][bins]+=1
                                print "Test",Hash[key][int(ginum)]
                            else:
                                pass
                                #print "Lost:", ginum
                        #except TypeError:
                        #    pass
                            #print 'end\n'
                            #return Hash
                        cline = ""
                else:
                    cline+=line
                i+=1
    #print cline
    return Hash


def giRead(line):
    raw = line.split("\t")
    #print "X",line
    info = []
    for part in raw:
        lok = part.strip('\n')
        if len(lok)>1:
            #print len(lok),lok
            info.append(lok)
    if len(info)>7:
        try:
            #print '\n',"info",info[0],info[1],info[2],info[3],info[4],info[len(info)-2] #,info
            raw_mdz = str(info[len(info)-2]).split(':')
            mdz = raw_mdz[2]
            gi = str(info[0]).split("|")
            ginum = gi[1]
            if len(info[1])>5:
                cigar = info[3]
                tax = str(info[1]).split("|")
                taxnum = tax[1]
                ginum = taxnum
                start_pos = info[2]
                #print "A:"
            else:
                start_pos = info[3]
                cigar = info[4]
                tax = str(info[2]).split("|")
                taxnum = tax[1]
                ginum = taxnum
                #print 'B:'
            #print "raw",len(info),'gi:',ginum,'tax:',taxnum,'cig:',cigar,'md:',mdz,'SP:',start_pos
            mz = int(mdz_score(mdz))
            cig = int(cigar_score(cigar))
            if cig > 0:
                score = ((mz)/(cig))*100
            else:
                score = 'NA'
            return ginum,taxnum,score,start_pos
        except IndexError:
            pass
    else:
        pass

def mdz_score(score):
    code = re.findall(r'(\D+|\d+)',score)
    score = 0
    #print code
    for i in xrange(len(code)-1):
        try:
            score += int(code[i])
        except ValueError:
            #score+=len(str(code[i]))
            pass
    return int(score)

def cigar_score(score):
    code = re.findall(r'(\D+|\d+)',score)
    score = 0
    #print code
    for i in xrange(len(code)-1):
        if i < len(code)-1:
            if code[i+1]=='M':
                #print i,code[i]
                score+=int(code[i])
    #print "Score",score
    return (score)

def Endprint(Hash): #Test by printing created outfile
    #f =open(str(os.getcwd()+"/MarcoAbreuFinalResult.txt"))
    outFile = open('MarcoAbreuFinalResult.txt','w')
    toString = "TaxID\tGiNumber\tBin\tBin Range\tCount\n"
    for key in sorted(Hash.keys()):
        for key1 in sorted(Hash[key].keys()):
            for i,bin in enumerate(Hash[key][key1]):
            #for key2 in sorted(Hash[key][key1]):
                toString += str(key)+"\t"+str(key1)+"\t"+str(i)+"\t"+"\t"+str(Hash[key][key1][i])+"\t"+"\t"+"\n"

            print 'T:',key,"G",key1,'#Bins',len(Hash[key][key1]),"Max-filled",max(Hash[key][key1]),Hash[key][key1][i]
    print "Write...",
    outFile.write(toString)
    print "Close", outFile
    outFile.close()
    return "Write Complete"


print "START"
print "Check for merged bowtie files"
if file in os.listdir(str(os.getcwd()+"/")):
    look = file.split(".")
    if look[len(look)-1].endswith("_CSAM.sam"):
        print file, 'Pass'
    else:
        Genetics = B2_PLAN(Source,Results_to,Source_Index1,Source_Index2)
        Genetics.master_run()
        #SAMREADER(hashX)
        #print TaxID_gi_bin_hasher(Dump,GenSource)
print "Check for results"
TaxID_gi_bin_hasher(Dump,GenSource, Bin_Size=1000)
print "Run bins"
Endprint(SAMREADER(refined_hash()))
print "END"

