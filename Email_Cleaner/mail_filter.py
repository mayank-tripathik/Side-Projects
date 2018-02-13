import imaplib
import email
class email_bot:
	def __init__(self,config_filename, keyword_filename):
		config_file = open(config_filename,'r')
		self.host = config_file.readline().strip()
		self.port = config_file.readline().strip()
		self.username = config_file.readline().strip()
		self.password = config_file.readline().strip()
		self.keywords = open(keyword_filename,'r').read().split()

	def establish_connection(self):
		self.mail_client = imaplib.IMAP4_SSL(self.host,self.port)
		try:
			self.mail_client.login(self.username, self.password)
		except:
			print("Login failed!")

	def select_folder(self,foldername):
		self.mail_client.select(foldername)

	def get_mail_content(self,mail_num):
		res, current_mail = self.mail_client.fetch(mail_num, ("RFC822"))
		mail_content = ""
		if res == "OK":
			mail_content = email.message_from_bytes(current_mail[0][1])
		return mail_content

	def keyword_present_in_subject(self,subject):
		if len(subject) != 0:
			for delete_word in self.keywords:
				if delete_word in subject:
					return True
		return False

	def delete_mails_having_keywords(self):
		response, mails = self.mail_client.search(None,"ALL")
		if response == "OK":
			for mail_num in mails[0].split():
				mail_content =  self.get_mail_content(mail_num)
				print("Mail number ", mail_num , " is under process!")
				if mail_content:
					try:
						subject = email.header.make_header(email.header.decode_header(mail_content['Subject']))
						subject = str(subject).lower()
						if self.keyword_present_in_subject(subject):
							self.mail_client.store(mail_num, '+FLAGS', '\\Deleted')
							print("Mail with ID : ",mail_num, "is deleted")
					except:
						continue
				else:
					print("Can't get mail of this ID : ",mail_num)
			self.mail_client.expunge()
			print("Mails having keywords are deleted successfully!")
		else:
			print("Can't fetch mails!")

	def delete_mails_from_sender(self,sender):
		response, mails = self.mail_client.search(None,"FROM",sender)
		if response == "OK":
			for mail_num in mails[0].split():
				mail_content =  self.get_mail_content(mail_num)
				print("Mail number ", mail_num , " is under process!")
				if mail_content:
					self.mail_client.store(mail_num, '+FLAGS', '\\Deleted')
					print("Mail with ID : ",mail_num, "is deleted")
				else:
					print("Can't get mail of this ID : ",mail_num)
			self.mail_client.expunge()
			print("Mails from the sender are deleted successfully!")
		else:
			print("Can't fetch mail from this sender")

# This file contains email and password in seperated lines
CONFIG_FILENAME = "config_user"

# This file contains words that needs to be in the subject to delete it
KEYWORD_FILENAME = "cuss_words"

# Getting instance of email bot
email_autobot = email_bot(CONFIG_FILENAME,KEYWORD_FILENAME)

# Establishes connection through email and password provided in confif file.
# If you are using different mailbox than gmail, replace host and port in the constructor
# with appropriate entries.
email_autobot.establish_connection()

# Give the name of the folder you want to move in.
email_autobot.select_folder("INBOX")

# Give the name of the sender in the parameter whom mails you want to delete
email_autobot.delete_mails_from_sender("Abhilash")

# delete mails if their subject have any words from the keyword file provided
email_autobot.delete_mails_having_keywords()

