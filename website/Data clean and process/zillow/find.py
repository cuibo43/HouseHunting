#r = open("sample.txt","r")
import ast
def findInfo(text,zipcode):
	
	homeinfo_dict = {}
	pos = text.find("homeInfo\"")
	if pos != -1:
		beg = pos + 10
		pos = beg + 1
		end = text.find("homeStatus")
		
		if end != -1:
			homeinfo = text[beg:end-2]+"}"
			pos = 1
			while(homeinfo.find("\\")!= -1):
				pos = homeinfo.find("\\")
				homeinfo = homeinfo[:pos]+homeinfo[pos+1:]
			
			homeinfo_dict = ast.literal_eval(homeinfo)
		
	a1 = "streetAddress" in homeinfo_dict.keys() and homeinfo_dict["streetAddress"]
	a2 = "price" in homeinfo_dict.keys() and homeinfo_dict["price"]
	a3 = "bathrooms" in homeinfo_dict.keys() and homeinfo_dict["bathrooms"]
	a4 = "bedrooms" in homeinfo_dict.keys() and homeinfo_dict["bedrooms"]
	a5 = "livingArea" in homeinfo_dict.keys() and homeinfo_dict["livingArea"]
	a6 = "homeType" in homeinfo_dict.keys() and homeinfo_dict["homeType"]
	if a1 and a2 and a3 and a4 and a5 and a6:
		return homeinfo_dict
	return {}