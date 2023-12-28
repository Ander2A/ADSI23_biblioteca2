import datetime
from .Connection import Connection
from .tools import hash_password

db = Connection()

class Session:
	def __init__(self, hash, time):
		self.hash = hash
		self.time = time

	def __str__(self):
		return f"{self.hash} ({self.time})"

class User:
	def __init__(self, id, username, email, admin):
		self.id = id
		self.username = username
		self.email = email
		print(admin, type(admin))
		self.admin = admin

	def __str__(self):
		return f"{self.username} ({self.email})"

	def new_session(self):
		now = float(datetime.datetime.now().time().strftime("%Y%m%d%H%M%S.%f"))
		session_hash = hash_password(str(self.id)+str(now))
		db.insert("INSERT INTO Session VALUES (?, ?, ?)", (session_hash, self.id, now))
		return Session(session_hash, now)

	def validate_session(self, session_hash):
		s = db.select("SELECT * from Session WHERE user_id = ? AND session_hash = ?", (self.id, session_hash))
		if len(s) > 0:
			now = float(datetime.datetime.now().strftime("%Y%m%d%H%M%S.%f"))
			session_hash_new = hash_password(str(self.id) + str(now))
			db.update("UPDATE Session SET session_hash = ?, last_login=? WHERE session_hash = ? and user_id = ?", (session_hash_new, now, session_hash, self.id))
			return Session(session_hash_new, now)
		else:
			return None

	def delete_session(self, session_hash):
		db.delete("DELETE FROM Session WHERE session_hash = ? AND user_id = ?", (session_hash, self.id))
	
	def get_books_read(self):
		# Obtener la lista de libros leídos por el usuario desde la base de datos
		books_read = db.select("SELECT book_id FROM UserBooks WHERE user_id = ?", (self.id,))
		return [book[0] for book in books_read]

	def get_book_topics(self, book_id):
		# Obtener los temas del libro desde la base de datos
		topics = db.select("SELECT topic FROM BookTopics WHERE book_id = ?", (book_id,))
		return [topic[0] for topic in topics]
		
	def get_lagunen_zerrenda(self):
		return True
		
	
	def get_irakurritako_liburuak(self):
		books_read = db.select("SELECT * FROM ErreserbenHistoriala T, Book T2 WHERE T.userId = ? AND T2.id = T.bookId", (self.id,))
		print("User ID:", self.id)
		books = [
			Book(b[0],b[1],b[2],b[3],b[4])
			for b in books_read
		]
		print(len(books_read))
		if len(books_read) > 0:
			print("AAAAAAAAAAAAAAAAAAAAAAAAA")
		else:
			print("EEEEEEEEEEEEEEEEEEEEEEEEEE")
		return books


		
		
		
		
		
		
		
		
		
		
		
		
		
