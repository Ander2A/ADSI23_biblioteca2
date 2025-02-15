from model import Connection, Book, User
from model.tools import hash_password

db = Connection()

class LibraryController:
	__instance = None

	def __new__(cls):
		if cls.__instance is None:
			cls.__instance = super(LibraryController, cls).__new__(cls)
			cls.__instance.__initialized = False
		return cls.__instance


	def search_books(self, title="", author="", limit=6, page=0):
		count = db.select("""
				SELECT count() 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
		""", (f"%{title}%", f"%{author}%"))[0][0]
		res = db.select("""
				SELECT b.* 
				FROM Book b, Author a 
				WHERE b.author=a.id 
					AND b.title LIKE ? 
					AND a.name LIKE ? 
				LIMIT ? OFFSET ?
		""", (f"%{title}%", f"%{author}%", limit, limit*page))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in res
		]
		return books, count

	def get_user(self, email, password):
		user = db.select("SELECT * from User WHERE email = ? AND password = ?", (email, hash_password(password)))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][4])
		else:
			return None

	def get_user_cookies(self, token, time):
		user = db.select("SELECT u.* from User u, Session s WHERE u.id = s.user_id AND s.last_login = ? AND s.session_hash = ?", (time, token))
		if len(user) > 0:
			return User(user[0][0], user[0][1], user[0][2], user[0][4])
		else:
			return None
			
	def liburuaGehitutaZegoen(self, libId):
		emaitza = db.select("SELECT * FROM BOOK WHERE id = ?", (libId,))
		if emaitza:
			return True
		else:
			return False
			
	def liburua_gehitu(self, libId, titulua, autorea, azala, deskribapena):
		db.insert("INSERT INTO AUTHOR VALUES (?)", (autorea))
	#	autoreaa = db.select("SELECT id FROM AUTHOR WHERE name = ?", (autorea))
	#	db.insert("INSERT INTO BOOK VALUES (?, ?, ?, ?, ?)", (libId, titulua, autorea, azala, deskribapena))


	def get_autore_baten_liburuak(self,author,autore="",title=""):
		autorearen_liburuak = db.select("SELECT T.* FROM Book T, Author T2 WHERE T2.name = ? AND T2.id = T.author AND T.title LIKE ? AND T2.name LIKE ?",(author.name,f"%{title}%", f"%{autore}%"))
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in autorearen_liburuak
		]
		return books
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
