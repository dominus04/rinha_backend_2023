import psycopg2, json

class Conn:
    conn = psycopg2.connect(
        host="0.0.0.0",
        port="5432",
        dbname="python_test",
        user="postgres",
        password="1234"
    )

    cur = conn.cursor()
    def insert(self, content):
        with self.conn:
            try:
                query = "INSERT INTO users (apelido, nome, nascimento, stack) VALUES (%s, %s, %s, %s) RETURNING id"
                self.cur.execute(query, (content['apelido'], content['nome'], content['nascimento'], content['stack']))
                rows = self.cur.fetchone()
                self.conn.commit()
                return rows[0]
            except Exception as err:
                raise ValueError(422)
            
    def search_by_uuid(self, uuid):
        with self.conn:
            try:
                query = "SELECT id, apelido, nome, nascimento, stack FROM users WHERE id = %s"
                self.cur.execute(query, (uuid,))
                row = self.cur.fetchone()
                self.conn.commit()
                if row[4]:
                    stack = row[4].replace('{', '').replace('}', '').split(',')
                else:
                    stack = row[4]
                dict_json = {
                    "id": row[0],
                    "apelido": row[1],
                    "nome": row[2],
                    "nascimento": str(row[3]),
                    "stack": stack
                }
                
                return json.dumps(dict_json, ensure_ascii=False)
                
            except Exception as err:
                raise ValueError(404)
            
    def search_by_term(self, term):
        if not term:
            raise ValueError(400)
        
        with self.conn:
            try:
                query = "SELECT id, apelido, nome, nascimento, stack FROM users WHERE campo_busca ILIKE %s ESCAPE '=';"
                self.cur.execute(query, ('%' + term + '%',))
                rows = self.cur.fetchall()
                self.conn.commit()
                list_json = []
                for row in rows:
                    if row[4]:
                        stack = row[4].replace('{', '').replace('}', '').split(',')
                    else:
                        stack = row[4]
                    temp_dict = {
                        "id": row[0],
                        "apelido": row[1],
                        "nome": row[2],
                        "nascimento": str(row[3]),
                        "stack": stack
                    }
                    list_json.append(temp_dict) 
                    
                return json.dumps(list_json, ensure_ascii=False)
            except Exception as err:
                raise err
            
    def get_total_pessoas(self):
        try:
            self.cur.execute('SELECT COUNT (id) FROM users;')
            rows = self.cur.fetchone()
            self.conn.commit()
            return str(rows[0])
        except Exception as err:
            print(err)