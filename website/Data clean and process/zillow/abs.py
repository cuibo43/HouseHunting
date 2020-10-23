import urllib2
import find as fi
import csv
import time

def getRentals(zipcode):
	rentalList=[]
	i=0
	while (i<20):
		i=i+1
		request = urllib2.Request("http://www.zillow.com/homes/for_sale/GA-"+str(zipcode)+"/house,condo,apartment_duplex,mobile,townhouse_type/"+str(i)+"_p/", headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.103 Safari/537.36'})
		page_text = urllib2.urlopen(request).read()
		#response = urllib2.urlopen("http://www.zillow.com/homes/for_sale/GA-"+str(zipcode)+"/house,condo,apartment_duplex,mobile,townhouse_type/"+str(i)+"_p/")
		#page_text = response.read()
		#print "http://www.zillow.com/homes/for_rent/GA-"+str(zipcode)+"house,condo,apartment_duplex,mobile,townhouse_type/"+str(i)+"_p/"
		#w.write(page_text)
		articleTimes = page_text.count("article")
		w = open("rentalList.txt","w")
		w.write(page_text)
		print i
		#print articleTimes
		
		if articleTimes ==1:
			break
		findArticle = page_text.find("article",0)
		for j in range((articleTimes-1)/2):
			findArticle = page_text.find("article",findArticle+5)
			beg=findArticle
			findArticle = page_text.find("article",findArticle+5)
			end=findArticle
			
			rentalList.append(fi.findInfo(page_text[beg:end],zipcode))
			time.sleep(0.1)
	return rentalList
zips = ['30363','30368','30369','30370','30371','30374','30375']
for zip in zips:
	d = getRentals(zip)
	

	filename = zip +".csv"
	with open(filename,"wb") as f:
		w = csv.writer(f)
		for s in range(len(d)):	
			if (d[s]):
				w.writerow([d[s]["streetAddress"],d[s]["price"],d[s]["bathrooms"],d[s]["bedrooms"],d[s]["livingArea"],d[s]["homeType"],zip])


