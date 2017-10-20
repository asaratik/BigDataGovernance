import  utility as utl
import sys
import constant as constant

DEBUG = True
DEBUG = False
def debug(str):
	#print str
	pass

class PyJSOb:

	def __init__(self,tag=None,path=None, type="OBJECT"):
		self.key = tag
		self.path = path
		self.label = None
		self.children = []
		self.prim_mem = []
		self.obj_mem = []
		self.array_mem = []
		self.type = type
		self.label = constant.DEFAULT_LABEL
		self.label_path = "None"

	# if a label is applied it means which ob-path the label comes from
	def set_label_path(self,path):
		self.label_path = path

	def set_type(self, type="OBJECT"):
		self.type = type

	def set_key (self,tag):
		self.key = tag

	def add_child (self,child):
		self.children.append(child)

	def add_prim_mem(self,key=None, value=None):
		if key:
			self.prim_mem.append({key:value})
		else:
			self.prim_mem.append(value)

	def add_obj_mem(self,key = None, value=None):
		
		if key:
			#value.set_key(key)
			self.obj_mem.append( {key:value} )
		else:
			self.obj_mem.append(obj)

	def add_array_mem(self,key=None, value=[]):
		self.set_type("ARRAY")
		#if key:
		if value:
			self.array_mem.append(value)
		#else:
		#	self.array_mem.append(value)

	def set_label (self,label):
		self.label = label
	
	def get_prim_mem(self):
		return self.prim_mem
	
	def set_path(self,path):
		self.abs_path = path

	
	def _print_array(self, arr):
		json = ""

		
		if arr.type == "ARRAY":
			json = json + " [ "
		commaFlg = False

		if DEBUG:
			lv = "\"{}\"".format(arr.label)
			json = json + lv + ","
			lv = "\"{}\"".format(arr.label_path)
			json = json + lv + ","
			lv = "\"{}\"".format(arr.abs_path)
			json = json + lv + ","
			lv = "\"{}\"".format(id(arr))
			json = json + lv
			commaFlg = True               


		# print primitive members first.
		for a in arr.prim_mem:
			if commaFlg :
				json = json + " , "
			if type(a) is str:
				json = json + "\"" +  str(a) + "\""
			elif type(a) is int or type(a) is float:
				json = json + str(a)
			else:
				#print a, type(a)
				json = json + "\"" + str(a) + "\""
			commaFlg = True
		
		for a in arr.array_mem:
			
			if commaFlg:
				json = json + " , "
			if a.type == "ARRAY":
				json = json + self._print_array(a)
			elif a.type == "OBJECT":
				json = json + self._print_obj(a)
			else:
				pass
			commaFlg = True
		

		if arr.type == "ARRAY":
			json = json + "]"
		

		return json
	

	def _print_obj(self,obj):
		json = ""
		commaFlg=False
		#if  obj.key :
		#	json =  "\"" + obj.key + "\"" + " : "
			

		json = json + " { "

		# get primitive member first.

                if DEBUG:
			lv = "\"{}\":\"{}\"".format("label",obj.label)
                        json = json + lv  + "," 
			lv = "\"{}\" : \"{}\"".format("label_from",obj.label_path)
                        json = json + lv + "," 
			lv = "\"{}\" : \"{}\"".format("path",obj.abs_path)
			json = json + lv + ","			
			lv = "\"{}\" : \"{}\"".format("object_id",id(obj))
			json = json + lv
                        commaFlg = True 

		for kv in obj.prim_mem:
			for (k,v) in kv.items():
				if commaFlg: 
					json = json + " , "  				
				json = json + "\""+str(k) + "\"" + " : " + "\"" + str(v) + "\""
				commaFlg = True

		# get obj member...
		for o in obj.obj_mem:
			for (k,v) in o.items():
				if commaFlg :
					json = json + " , "
				if v.type == "OBJECT": #!!!!!
					#json = json +  self._print_obj(o)
					json = "{} \"{}\":{}".format(json,k,self._print_obj(v))
				elif v.type == "ARRAY":
					#json = json + self._print_array(o)
					json = "{} \"{}\" : {}".format(json,k,self._print_array(v))
				else:
					pass
			commaFlg = True
			
		json = json + " } "

		return json

	def print_json (self):
		if self.type == "OBJECT":
			return self._print_obj(self)
		elif self.type == "ARRAY":
			return self._print_array(self)
		else:
			return {"error":"Neting obj nor Array"}

	def pretty_print(self):
		return 	utl.pretty_print( self.print_json())
			
'''
	this class represent the whole object tree of the json data
'''
class PyObjTree:

	def __init__(self, jsonObj):
		self.root = self.buildTree(jsonObj,"")
		#return self.root
	def get_root(self):
		return self.root
	
	def buildTree(self,jsonObj,path):

		#py_obj = PyJSOb(type="OBJECT")
		#print jsonObj
		#jsonObj.set_path(path)
		if type(jsonObj) is dict:
			py_obj = PyJSOb(type="OBJECT")			
			#print "setting path = {}----------------".format(path)
			py_obj.set_path(path)

			#print "setting path = {} on object id {}----------------".format(py_obj.abs_path,id(py_obj))
			for (k,v) in jsonObj.items():
				#print k, v
				t_path = "{}/{}".format(path,k)
				if type(v) is dict:
					py_obj.add_obj_mem( key=k, value = self.buildTree(v,t_path) )

				elif type(v) is list:
					py_obj.add_obj_mem(key=k, value = self.buildTree(v,t_path))

				elif type(v) is str or type(v) is int or type(v) is float:
					#print v
					py_obj.add_prim_mem(key=k, value = v)
				else:					
					py_obj.add_prim_mem(key=k, value = v)
					#print type(v)
					pass
			return py_obj
		
		elif type (jsonObj) is list:
			py_obj = PyJSOb(type="ARRAY")
			py_obj.set_path(path)

			index = 0
			for arr in jsonObj:
				t_path = "{}[{}]".format(path,index)
				if type(arr) is list:
					py_obj.add_array_mem( value=self.buildTree(arr,t_path))
				elif type(arr) is dict:
					py_obj.add_array_mem(value=self.buildTree(arr,t_path))

				elif type(arr) is str or type(arr) is int or type(arr) is float:
					py_obj.add_prim_mem(value = arr)
				else:
					py_obj.add_prim_mem(value = arr)

				index = index + 1
			return py_obj
		else:
			pass