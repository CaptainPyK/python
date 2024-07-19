#! /usr/bin/python

import argparse
import sys
import pyodbc as po

NAGIOSUNKNOWN = -1
NAGIOSOK = 0
NAGIOSWARNING = 1
NAGIOSCRITICAL = 2

#Read the args
def read_args():
    parser = argparse.ArgumentParser(
       description= "Execute an SQL Procedure,",
       epilog= ":)"
    )
    parser.add_argument("-H", "--host", help="--> Enter the IP's or fqdn's server ",required=True)
    parser.add_argument("-P","--port",help="--> Optionnal Enter: The port for sql server, ",default="1433")
    parser.add_argument("-D","--database",help="--> Enter the name of the database where the procedure is",required=True)
    parser.add_argument("-U","--user",help="--> Enter the username",required=True)
    parser.add_argument("-PWD","--password",help="--> Enter the username's password",required=True)
    parser.add_argument("-PROC","--sqlprocedurename",help="--> Enter the procedure name",required=True)
    parser.add_argument("-w","--warning",type=int, help="--> warning value for desired capacity",required=True)
    parser.add_argument("-c","--critical",type=int, help="--> critical value for desired capacity",required=True)
    args=parser.parse_args()
    return args

def db_connection(server,port,database,username,password):
   try:
        cnxn = po.connect('DRIVER={ODBC Driver 18 for SQL Server};\
                          SERVER=tcp:'+server+','+port+';\
                          DATABASE='+database+';\
                          ENCRYPT=yes;\
                          UID='+username+';\
                          PWD='+ password + ';\
                          TrustServerCertificate=yes')
        
        cursor = cnxn.cursor()
        return cnxn,cursor
   except:
        print("Error Connection, please check your credentials or host information ")
        sys.exit(NAGIOSUNKNOWN)

def terminate_cursor(cursor):
    try:
        cursor.close()
        del cursor
    except:
        print("terminate cursor error")
        sys.exit(NAGIOSUNKNOWN)

def db_close(cnxn):
    try:
        cnxn.close()
    except:
        print("db clossing error")
        sys.exit(NAGIOSUNKNOWN)


def execute_procedure(cursor,procedure_name):
    try:
        storedproc = 'Exec {0}'.format(procedure_name)
        cursor.execute(storedproc)
        row = cursor.fetchone()
        return row
    except:
        print("procedure not found")
        sys.exit(NAGIOSUNKNOWN)

def iterate_cursor(cursor,row):
    try:
        if row:
            return row[0]
        else:
            print("No result")
            sys.exit(NAGIOSUNKNOWN)
    except:
        print("iterate cursor not ok")
        sys.exit(NAGIOSUNKNOWN)

#customer case
def result_procedure(result,critical,warning):
    if result < critical:
        print('CRITICAL: Retour procedure non conforme - valeur resultat {0}'.format(result))
        sys.exit(NAGIOSCRITICAL)
    elif result < warning:
        print('WARNING: Retour procedure non conforme - valeur resultat {0}'.format(result))
        sys.exit(NAGIOSWARNING)
    else:
        print('OK: Retour procedure conforme - valeur resultat {0}'.format(result))
        sys.exit(NAGIOSOK)

def main():
    param_checks = read_args()
    cnxn,cursor=db_connection(param_checks.host,param_checks.port,param_checks.database,param_checks.user,param_checks.password)
    row=execute_procedure(cursor,param_checks.sqlprocedurename)
    result=iterate_cursor(cursor,row)
    terminate_cursor(cursor)
    db_close(cnxn)
    result_procedure(result,param_checks.critical,param_checks.warning)



if __name__ == '__main__':
  main()