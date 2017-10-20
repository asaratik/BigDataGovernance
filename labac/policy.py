import utility as utl
import PythonJsonObj as PyObjTree
import ObQuery as Query
import constant as constant


class Enforcement:
	def __init__():
		pass

class NodeLabeling:
	def __init__(self,obj_tree , label_file = None, label_str=None):
		self.obj_tree = obj_tree
		self.label_file = label_file
		self.label_str = label_str
		self.query_ob = Query.ObQuery(self.obj_tree)

	def appy_labels(self):
		self._labelling()
		return self.obj_tree

	# labels object tree for each (path, label)
	def _labelling(self):
		( lbls, conds ) = self._labels()
		for l in lbls:
			(path, label) = l
			self._ob_tree_labelling(path,label)
		
		#print conds
		cond_path=[]
		cond_path_label = []
		for cond_l in conds:
			(cond, label) = cond_l
			# find equ paths from a given condition
			cond_path += self.path_from_condition(cond,self.obj_tree)
			# for each path add (path,label) entry
			for p in cond_path:
				cond_path_label += [(p,label)]
		
		#print cond_path_label
		for pl in cond_path_label:
			(p,l) = pl
			self._ob_tree_labelling(p,l)
		pass
	
	#read (path, label) from input file, and returns [(path,label),..]
	def _labels(self):
		if self.label_file:
			j = utl.LoadJSON(path=self.label_file)
		elif self.label_str:
			j = utl.LoadJSON(str=self.label_str)
		js = j.get_json()
		r = []
		c_l = []
		for ob in js:
			if  'target' in ob and ob['target']:
				r.append((ob['target'],ob['label']))
			elif 'condition' in ob:
				c_l += [ (ob['condition'], ob['label']) ]
			else:
				pass
		return (r , c_l)

	#def _conditional_label(self):

        def _condition(self, value1, op, value2):
               	if op == "=":
                        return value1 == value2
               	elif op == ">" :
                        return value1 > value2
                elif op == ">=":
                        return value1 >= value2
                elif op == "<":
                        return value1 < value2
                elif op == "<=":
                        return value1 <= value2
                else:
                        return False
	def path_from_condition(self, condition, jsob):
    
                #print condition
                member = condition['path']
                op = condition['op']
                value = condition['value']

                res = []

                # check if jsob 
                if jsob.type == "OBJECT":
                        # first check any member satisfy the condition
                        for p_m in jsob.prim_mem:
                                (k,v) = p_m.items()[0]
                                if member == k  and self._condition(v, op, value):
                                        return  [jsob.abs_path]
                            
                        for obj in jsob.obj_mem:
                                (k,v) = obj.items()[0]
                                res += self.path_from_condition(condition, v)
                        return res 
                elif jsob.type == "ARRAY":
                        for obj in jsob.array_mem:
                                res += self.path_from_condition(condition, obj)

                                 
                        return res 
                else:
                        return res 		

	def _ob_tree_labelling(self, path, label):
		# here path can be absolute or relative path
		res = self.query_ob.query(path)

		for r in res:
			#print "labeling----------------"
			#print r
			if isinstance(r,PyObjTree.PyJSOb):
				# r.path is eqv to path, because path matched r and r.abs_path is absolute 
				#print "labeling object with id{}---------".format(id(r))
				#self._labeling_on_condition(r,label,r.abs_path) 
				self.recursive_labeling(r,label, r.abs_path)
				pass
		
		pass

	def _labeling_on_condition(self, job, object_label, object_path):
		#print job
		if job.label == constant.DEFAULT_LABEL:
			job.set_label(object_label)
			job.set_label_path(object_path)
		elif utl.json_subpath(object_path, job.label_path):
			job.set_label(object_label)
			job.set_label_path(object_path)
			#print "############"

			#utl.pretty_print (job.print_json())
			pass
		else:
			pass
	def recursive_labeling(self,job, label, path):
		#job.set_label(label)

		#print "labeling object with id {} with label {} with path{}---------".format(id(job),label,path)
		self._labeling_on_condition(job,label,path)
		if job.type == "OBJECT":
			# all members in obj_mem is either ob, or array
			for ob in job.obj_mem:
				(k,v) = ob.items()[0]
				self.recursive_labeling(v,label,path)

		elif job.type == "ARRAY":
			for ob in job.array_mem:
				self.recursive_labeling(ob,label,path)

		else:
			pass