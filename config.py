import os

class Static():
	
	def save(self, user, passw):
		with open("upload_config", "w+") as f:
			f.write(user + "\r" + passw)
			
	def load(self):
		if os.path.isfile("upload_config"):
			with open("upload_config", "r") as f:
				text = f.read()
				parts = text.split("\r")
				if len(parts) == 2:
					return {"user": parts[0], "passw": parts[1]}
