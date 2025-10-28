try:
  f = open("demofile.txt" , 'w')
  print("File opened successfully")
  try:
    f.write("Lorum Ipsum\n")
    f.write("  This is a demo file\n")
    print("File written successfully")
  except:
    print("Something went wrong when writing to the file")
  finally:
    f.close()
except:
  print("Something went wrong when opening the file")  
