import json, os, threading, time, copy, traceback
from config import Config, DummyLog
import sys
reload(sys)


_config=Config(DummyLog())
_config.loadConfig()
_encoding=_config.config["General"]["encoding"]
# we probably should not be doing this, but it is probably ok as long as it is UTF-8 or if using python 2.x
# http://stackoverflow.com/questions/3828723/why-should-we-not-use-sys-setdefaultencodingutf-8-in-a-py-script
sys.setdefaultencoding(_encoding)

class Storage:
	def __init__(self, name, isWorld=None, root="wrapper-data/json"):
		self.name = name
		self.root = root
		
		self.data = {}
		self.dataOld = {}
		self.load()
		self.abort = False
		self.time = time.time()
		
		t = threading.Thread(target=self.periodicSave, args=())
		t.daemon = True
		t.start()
	def __del__(self):
		self.abort = True
		self.save()
	def __getitem__(self, index):
		if not type(index) == str:
			raise Exception("A string must be passed to the stuff")
		return self.data[index]
	def __setitem__(self, index, value):
		if not type(index) == str:
			raise Exception("A string must be passed to the stuff")
		self.data[index] = value
		return self.data[index]
	def __delattr__(self, index):
		if not type(index) == str:
			raise Exception("A string must be passed to the stuff")
		del self.data[index]
	def __delitem__(self, index):
		if not type(index) == str:
			raise Exception("A string must be passed to the stuff")
		del self.data[index]
	def __iter__(self):
		for i in self.data:
			yield i
	def periodicSave(self):
		while not self.abort:
			if time.time() - self.time > 60:
				if not self.data == self.dataOld:
					try:
						self.save()
					except:
						print traceback.format_exc()
					self.time = time.time()
			time.sleep(1)
	def mkdir(self, path):
		l = ""
		for i in path.split("/"):
			l += i + "/"
			if not os.path.exists(l):
				try: os.mkdir(l)
				except: pass 
	def load(self):
		self.mkdir(self.root)
		if not os.path.exists("%s/%s.json" % (self.root, self.name)):
			self.save()
		with open("%s/%s.json" % (self.root, self.name), "r") as f:
			try:
				self.data = json.loads(f.read(),_encoding)
			except:
				print "Failed to load '%s/%s.json' - fresh" % (self.root, self.name)
				return
		self.dataOld = copy.deepcopy(self.data)
	def save(self):
		if not os.path.exists(self.root):
			self.mkdir(self.root)
		with open("%s/%s.json" % (self.root, self.name) , "w") as f:
			f.write(json.dumps(self.data,ensure_ascii=False))
		self.flush = False
	def key(self, key, value=None):
		if value == None:
			return self.getKey(key)
		else:
			self.setKey(key, value)
	def getKey(self, key):
		if key in self.data:
			return self.data[key]
		else:
			return None
	def setKey(self, key, value=None):
		if value == None:
			if key in self.data: del self.data[key]
		else:
			self.data[key] = value
		self.flush = True
