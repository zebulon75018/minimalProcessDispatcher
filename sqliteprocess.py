import sqlite3
import traceback


#
# class consumator / consumer to send in background process.
#
class SqliteProcess:
    def __init__(self):
        self._error = False
        self.errorException = None
        self.conn = sqlite3.connect('process.db')
        self._createtable()

    ##########################################################
    def _createtable(self):
    #
    # Create Table if not exists ...
    #
        try:
            c = self.conn.cursor()
            c.execute("""CREATE TABLE IF NOT EXISTS process (
                            id  INTEGER PRIMARY KEY AUTOINCREMENT, 
                            status TEXT  NOT NULL DEFAULT 'W',
                            processcmd TEXT,
                            creationdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP ,
                            launchdate TIMESTAMP DEFAULT 0,
                            finishdate TIMESTAMP DEFAULT 0)
                      """
                    )

        except Exception as e:
            self.errorHappened(e)

    ##########################################################
    def createEntry(self,cmd):
        #
        # Create a new entry 
        # return id  
        #
        cur = self.conn.cursor()
        cur.execute(" INSERT INTO process (processcmd) VALUES (\"%s\");" % ( cmd) )
        self.conn.commit()
        idprocess =  cur.lastrowid
        return idprocess

    ##########################################################
    def reserveProcess(self, id ):
        # reserve the process then no other launch it.
        try:
            cursor = self.conn.execute("UPDATE process SET launchdate = CURRENT_TIMESTAMP WHERE id =%d" % (id))
            self.conn.commit()
        except Exception as e:
            self.errorHappened(e)


    ##########################################################
    def getNextProcess(self):
        #
        # get next process to launch.
        #
        try:
            cursor = self.conn.execute("SELECT id,processcmd FROM process WHERE launchdate =0")
            rows = cursor.fetchall()
            if len(rows)>0 :
                return rows[0]
            return None

        except Exception as e:
            self.errorHappened(e)

   
    ##########################################################
    def processIsDone(self, id ):
        self._updateprocess(id,"D")
    
    ##########################################################
    def processFailed(self, id ):
        self._updateprocess(id,"E")
        
    ##########################################################
    def _updateprocess(self, id , status):
        try:
            cursor = self.conn.execute("UPDATE process SET status = '%s', finishdate =CURRENT_TIMESTAMP WHERE id =%d" % (status, id))
            self.conn.commit()
        except Exception as e:
            self.errorHappened(e)

        ##########################################################
    def errorHappened(self, e):
        traceback.print_stack()
        print(e)
        self._error = True
        self.errorException = e  

    ##########################################################
    def closeDB(self):
        self.conn.close()
    ##########################################################
    def IsErrorHappened(self):
        return self._error
