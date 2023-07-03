from pysondb import db
from datetime import datetime

class Data:
	
	def __init__(self):
		self.db = db.getDb("libs/notetackerdatabase/notes.json")

	def save_note(self,title:str,content:str):
		self.db.add({
			"title":f"{title}",
			"content":f"{content}",
			"date":f"{datetime.now().date()}"
			})

	def delete_note(self,id:int):
		self.db.deleteById(id)

	def get_notes(self) -> iter:
		data = self.db.getAll()
		return data 
	def update_note(self,id,new_data_set):
		

		self.db.updateById(id,new_data_set)




