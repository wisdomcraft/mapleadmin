import mysql.connector
from config import config
from flask  import abort, Response

class mysqlClass:


    config          = {}
    database        = 'default'
    host            = 'slave'
    connect         = {
        'default':{
            'master': None,
            'slave' : None
        },
        'market':{
            'master': None,
            'slave' : None
        }
    }
    


    def __init__(self):
        if config.get('mysql') == None:
            abort(Response('{"code":0, "message":"mysql config not exist in config file"}'))
        self.config = config.get('mysql')
        return None


    def __connect(self):
        database        = self.database
        selfconfig      = self.config
        if selfconfig.__contains__(database) == False:
            return {'code':0, 'message':'error, database parameter is incorrect, mysqlClass.py #39'}

        host            = self.host
        if host!='master' and host!='slave':
            return {'code':0, 'message':'error, host parameter is incorrect, mysqlClass.py #70'}

        connect         = self.connect
        connectCurrent  = connect[database][host]
        if connectCurrent != None: return connectCurrent

        database        = self.database
        configCurrent   = selfconfig.get(database, None)
        if configCurrent == None:
            return {'code':0, 'message':'error, mysql config empty, mysqlClass.py #79'}
        configCurrent   = configCurrent.get(host, None)
        if configCurrent == None:
            return {'code':0, 'message':'error, mysql config empty, mysqlClass.py #82'}

        try:
            connectCurrent  = mysql.connector.connect(
                host        = configCurrent['host'], 
                user        = configCurrent['user'], 
                password    = configCurrent['password'], 
                database    = configCurrent['database'], 
                port        = configCurrent['port'], 
                connection_timeout = 5, 
                buffered    = True
            )
            self.connect[database][host] = connectCurrent
            return connectCurrent
        except mysql.connector.Error as error:
            return {'code':0, 'message':'error, connect mysql server failed, mysqlClass.py #97, ' + format(error)}
        finally:
            self.database   = 'default'
            self.host       = 'slave'


    def set(self, setting):
        for key in setting:
            if key == 'database':
                self.database   = setting[key]
                continue
            if key == 'host':
                self.host       = setting[key]
                continue
        return self


##-------------------------------------------
    def query(self, sql=None):
        if sql == None:
            return {'code':0, 'message':'error, sql empty in query(), mysqlClass.py #115'}

        connect = self.__connect()
        cursor  = connect.cursor()
        try:
            cursor.execute(sql)
            return cursor;
        except mysql.connector.Error as error:
            return {'code':0, 'message':'error, connect mysql server failed, mysqlClass.py #123, ' + format(error)}


##-------------------------------------------
    def find(self, sql=None, value=None):
        if sql == None:
            return {'code':0,'message':'error, sql empty in find(), mysqlClass.py #98'}

        connect = self.__connect()
        if isinstance(connect, dict):
            return connect
        cursor  = connect.cursor()
        try:
            cursor.execute("SET NAMES 'utf8'")
            if value == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value)
            row = cursor.fetchone()
            if row == None:
                return {'code':1, 'message':'', 'data':None}
            data= dict(zip(cursor.column_names, row))
            cursor.close()
            return {'code':1, 'message':'', 'data':data}
        except mysql.connector.Error as error:
            return {'code':0, 'message':'error, select sql failed, mysqlClass.py #109, ' + format(error)}


##-------------------------------------------
    def select(self, sql):
        if sql == None:
            return {'code':0, 'message':'error, sql empty in select(), mysqlClass.py #156'}

        connect = self.__connect()
        if isinstance(connect, dict):
            return connect
        cursor  = connect.cursor()

        try:
            cursor.execute("SET NAMES 'utf8'")
            cursor.execute(sql)
            data    = []
            for row in cursor.fetchall():
                data.append(dict(zip(cursor.column_names, row)))
            cursor.close()

            if data == []:
                return {'code':1, 'message':'', 'data':None}

            return {'code':1, 'message':'', 'data':data}
        except mysql.connector.Error as error:
            return {'code':0, 'message':'error, select sql failed, mysqlClass.py #140, ' + format(error) + ', ' + sql}


##-------------------------------------------
    def insert(self, sql=None, value=None):
        if sql == None:
            return {'code':0,'message':'error, sql empty in insert(), mysqlClass.py #132'}

        self.hostServer = 'master'

        connect = self.__connect()
        if isinstance(connect, dict):
            return connect
        cursor  = connect.cursor()
        try:
            cursor.execute("SET NAMES 'utf8'")
            if value == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value)
            connect.commit()
            data = {'insert_id':cursor.lastrowid}
            return {'code':1, 'message':'', 'data':data}
        except mysql.connector.Error as error:
            return {'code':0,'message':'error, insert sql failed, mysqlClass.py #152, ' + format(error)}


##-------------------------------------------
    def update(self, sql=None, value=None):
        if sql == None:
            return {'code':0,'message':'error, sql empty in update(), mysqlClass.py #160'}

        self.hostServer = 'master'

        connect = self.__connect()
        if isinstance(connect, dict):
            return connect
        cursor  = connect.cursor()
        try:
            cursor.execute("SET NAMES 'utf8'")
            if value == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value)
            connect.commit()
            #data = {'insert_id':cursor.lastrowid}
            data = {'insert_id':123}
            return {'code':1, 'message':'', 'data':data}
        except mysql.connector.Error as error:
            return {'code':0,'message':'error, update sql failed, mysqlClass.py #170, ' + format(error)}


##-------------------------------------------
    def delete(self, sql=None, value=None):
        if sql == None:
            return {'code':0,'message':'error, sql empty in query(), mysqlClass.py #132'}

        self.hostServer = 'master'

        connect = self.__connect()
        if isinstance(connect, dict):
            return connect
        cursor  = connect.cursor()
        try:
            cursor.execute("SET NAMES 'utf8'")
            if value == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value)
            connect.commit()
            return {'code':1, 'message':''}
        except mysql.connector.Error as error:
            return {'code':0,'message':'error, delete sql failed, mysqlClass.py #197, ' + format(error)}


##-------------------------------------------
    def count(self, sql=None, value=None):
        if sql == None:
            return {'code':0,'message':'error, sql empty in count(), mysqlClass.py #212'}

        connect = self.__connect()
        if isinstance(connect, dict):
            return connect
        cursor  = connect.cursor()
        try:
            cursor.execute("SET NAMES 'utf8'")
            if value == None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, value)
            row = cursor.fetchone()
            data= row[0]
            cursor.close()
            return {'code':1, 'message':'', 'data':data}
        except mysql.connector.Error as error:
            return {'code':0, 'message':'error, select sql failed, mysqlClass.py #231, ' + format(error)}


##-------------------------------------------
    def dictToInsertSql(self, data=None, argument=None):
        if data == None:
            return {'code':0,'message':'error, data empty in dictToInsertSql(), mysqlClass.py #235'}
        if isinstance(data, dict) == False:
            return {'code':0,'message':'data type is not dict in dictToInsertSql(), mysqlClass.py #237'}

        if argument == None:
            return {'code':0,'message':'error, argument empty in dictToInsertSql(), mysqlClass.py #240'}
        if isinstance(argument, dict) == False:
            return {'code':0,'message':'argument type is not dict in dictToInsertSql(), mysqlClass.py #242'}

        table   = argument.get('table', None)
        if table == None:
            return {'code':0,'message':'error, table empty in dictToInsertSql() argument, mysqlClass.py #246'}

        keys    = []
        values  = []
        for key,value in data.items():
            keys.append('`' + key + '`')
            if isinstance(value, str)==False and isinstance(value, int)==False:
                return {'code':0,'message':'error, value must be string or int in dict data in dictToInsertSql(), mysqlClass.py #253'}
            if isinstance(value, int) == True:
                value   = str(value)
            value       = value.replace("'", "''")
            values.append("'" + value + "'")

        sql     = 'insert into `' + table + '` (' + ','.join(keys) + ') values (' + ','.join(values) +  ')'
        return {'code':1, 'data':sql}


    def multipleListToInsertSql(self, data=None, argument=None):
        if data == None:
            return {'code':0,'message':'error, data empty in multipleListToInsertSql(), mysqlClass.py #273'}
        if isinstance(data, list) == False:
            return {'code':0,'message':'data type is not list in multipleListToInsertSql(), mysqlClass.py #275'}
        if len(data) == 0:
            return {'code':0,'message':'data type is list but length zero in multipleListToInsertSql(), mysqlClass.py #277'}

        if argument == None:
            return {'code':0,'message':'error, argument empty in multipleListToInsertSql(), mysqlClass.py #278'}
        if isinstance(argument, dict) == False:
            return {'code':0,'message':'argument type is not dict in multipleListToInsertSql(), mysqlClass.py #280'}

        table   = argument.get('table', None)
        if table == None:
            return {'code':0,'message':'error, table empty in multipleListToInsertSql() argument, mysqlClass.py #284'}

        ignore  = argument.get('ignore', None)
        if ignore == True:
            ignore = 'ignore'
        else:
            ignore = ''

        keys_list    = []
        for key in data[0]:
            keys_list.append('`' + key + '`')
            del key

        values_list = []
        for i in range(0, len(data)):
            line    = []
            for value in data[i].values():
                if isinstance(value, str)==False and isinstance(value, int)==False:
                    return {'code':0,'message':'error, value must be string or int in dict data in multipleListToInsertSql(), mysqlClass.py #300'}
                if isinstance(value, int) == True:
                    value   = str(value)
                value   = value.replace("'", "''")
                line.append("'" + value + "'")
                del value
            values_list.append( '(' + ','.join(line) + ')' )
            del line

        sql     = 'insert %s into `%s` (%s) values %s' % (ignore, table, ','.join(keys_list), ','.join(values_list))
        return {'code':1, 'data':sql}


##-------------------------------------------
    def __del__(self):
        for key in self.connect:
            if self.connect[key]['master'] != None:
                self.connect[key]['master'].close()
                self.connect[key]['master'] = None

            if self.connect[key]['slave'] != None:
                self.connect[key]['slave'].close()
                self.connect[key]['slave'] = None

            del key