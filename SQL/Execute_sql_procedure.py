#test dont judge me bastard


import pyodbc as po

#chaine de connection

server = 'tcp:IP,1439' 
database = 'database_name' 
username = 'username' 
password = 'password' 

cnxn = po.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+ password + ';TrustServerCertificate=yes')
#print('cnxn:', cnxn)


cursor = cnxn.cursor()

storedproc1 = "Exec sonde.SONDE_NAGIOS_COMPTE_ENTITES"
storedproc2 = "Exec sonde.SONDE_NAGIOS_COMPTE_LIEUX"
params = ""

cursor.execute(storedproc2)
row = cursor.fetchone()

print(row)
#
# for r in row:
#    print(r)


 
# while row:
#
# 
#     print(row[0])
#    row = cursor.fetchone()

# Close the cursor and delete it
cursor.close()
del cursor
cnxn.close()

#print('cursor:', cursor)

#cursor.execute("SELECT @@version;") 
#row = cursor.fetchone()
#print(row[0])
#while row: 
#    #print(row[0])
#    row = cursor.fetchone()
#    print(row)
#