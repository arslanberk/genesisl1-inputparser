from ast import Not
import os, sys, getopt

KEY_ID      = "[ID]"
KEY_PRIMARY = "[PRIMARY]"
KEY_EVOLUTIONARY = "[EVOLUTIONARY]"
KEY_MASK = "[MASK]"


def write_to_file(outputFile, lineContent):
   with open(outputFile, 'a') as the_file:
      the_file.write(lineContent+'\n')
   
def prepare_id_line(idItems):
   text = '"'
   text += '","'.join(idItems);
   return text + '","'
   
def parse_input(inputFile, outputFile):
   try:
      isData = False
      isMask = False
      idItems = []
      dataRows = []
      with open(inputFile, 'r', encoding='UTF-8') as file:
         while (l := file.readline()):
            l = l.rstrip()
            if l in ['', '\n', '\r\n']:
               pass
            elif KEY_ID in l or KEY_PRIMARY in l:
               isData = False
               isMask = False
               dataRows.append(l)
            elif KEY_EVOLUTIONARY in l:
               isData = True
               isMask = False
               dataRows.append(l)
               write_to_file(outputFile, prepare_id_line(idItems))
               idItems = []
               for d in dataRows:
                  write_to_file(outputFile, d)
               dataRows = []
            else:
               if not isData:
                  idItems.append(l)
                  dataRows.append(l)
               else:
                  if KEY_MASK in l:
                     isMask = True
                     write_to_file(outputFile, l)
                  else:
                     if isMask and ("+" in l or "-" in l):
                        l += '"'
                     write_to_file(outputFile, l)
   except Exception as ex:
      print(ex)
      sys.exit(2)
   

def print_help(file):
   print(file + ' -i <inputfile> -o <outputfile>')


def main(file, argv):
   inputFile = None
   outputFile = None
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print_help(file)
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print_help(file)
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputFile = arg
      elif opt in ("-o", "--ofile"):
         outputFile = arg
   if not inputFile or not outputFile:
      print_help(file)
      sys.exit()
   try:
      os.remove(outputFile)
   except OSError:
      pass
   parse_input(inputFile, outputFile)
   
    
if __name__ == "__main__":
    main(sys.argv[0],sys.argv[1:])