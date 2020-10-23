library(tidyverse)
library(sp)
library(sf)
library(tmap)
library(pracma)
library(scales)
#read and clean data
getdata<-function(){
  setwd('E:/R/final')
  crime <- read_csv("Crime.csv") 
  food<-read_csv("Yelp.csv")
  price<-read_csv("Trulia.csv")
  
  
  pricefoodcrime<-price%>% 
    left_join(food,by="zipcode")%>% 
    left_join(crime,by="zipcode")
  
  
  pricefoodcrime<-pricefoodcrime%>% 
    filter(Restau>0) %>% #no NA
    select(address,zipcode,lat,lng,beds,price,Restau,crime)
  pricefoodcrime<-distinct(pricefoodcrime)
  #for zipcode level analysis
  #zipsummary<-pricefoodcrime%>% 
  #group_by(zipcode)%>% 
  #summarize(meanprice=mean(price),meancrime=mean(crime),meanrestaueant=mean(Restau))
  return(pricefoodcrime)
}

#inputFilter
inputFilter <- function(){
  price <- readline(prompt="Enter the price range(1:0~250,000, 2:250,000~500,000, 3:500,000~1,000,000, 4:>1,000,000): ")
  bed <- readline(prompt="Enter the number of bedrooms you want (0:studio, 1:1bedroom...4:>4bedrooms): ")
  return(c(price,bed))
}

#filter data
filterData<-function(data,filter){
  if(filter[1]=='1'){data<-data%>%filter(price<=250000)}
  else if(filter[1]=='2'){data<-data%>%filter(price<=500000,price>250000)}
  else if(filter[1]=='3'){data<-data%>%filter(price<=1000000,price>500000)}
  else if(filter[1]=='4'){data<-data%>%filter(price>1000000)}
  if(filter[2]=='0'){data<-data%>%filter(beds==0)}
  else if(filter[2]=='1'){data<-data%>%filter(beds==1)}
  else if(filter[2]=='2'){data<-data%>%filter(beds==2)}
  else if(filter[2]=='3'){data<-data%>%filter(beds==3)}
  else{data<-data%>%filter(beds>=4)}
  return(data)
}

#input
inputImportant <- function(){
  first <- readline(prompt="Enter the most important factor(1:price, 2:restaurant, 3:crime): ")
  second <- readline(prompt="Enter the second most important factor(1:price, 2:restaurant, 3:crime): ")
  order<-paste0(first,second)
  #Preset value for different options
  crimeprice=c(5,1/3,1/9)#crime>price>food
  crimefood=c(1/3,1/5,1/3)
  pricecrime=c(7,3,1/5)
  pricefood=c(3,9,7)
  foodprice=c(1/3,5,7)
  foodcrime=c(1/9,1/3,5)
  statement<-switch(order,
                    "12" = pricefood,
                    "13" = pricecrime,
                    "21" = foodprice,
                    "23" = foodcrime,
                    "31" = crimeprice,
                    "32" = crimefood
  )
  if (is.null(statement)){
    print("wrong input")
  }
  else{return(statement)} 
}

#make matrix based on user's choice
makematrix <- function(ratio) {
  #original matrix for AHP
  matrix<-data.frame(price=rep(0,times=3),food=0,crime=0)
  for (i in 1:3){
    matrix[i,i]=1
    }
    matrix[1,2] = ratio[1]
    matrix[2,1] = 1/ratio[1]
    matrix[1,3] = ratio[2]
    matrix[3,1] = 1/ratio[2]
    matrix[2,3] = ratio[3]
    matrix[3,2] = 1/ratio[3]
    return(matrix) 
}

#apply AHP on matrix
ahp <- function(matrix) {
  sum=0
  rootproductsvector=c(0,0,0)
  newmatrix<-matrix%>% 
    mutate(rootproducts=nthroot(price*food*crime,3))%>% 
    mutate(Eigenvector=rootproducts/sum(rootproducts))
  Eigenvector=newmatrix[,"Eigenvector"]
  newmatrix<-newmatrix%>% 
    mutate(consistencyMeasure=(price*Eigenvector[1]+food*Eigenvector[2]+crime*Eigenvector[3])/Eigenvector)
  return(newmatrix)
}

#judge whether AHP method can be accepted
calculateCIRI<- function(matrix){
    ci=(sum(matrix$consistencyMeasure)/3-3)/2
    ri=0.58
    cr=ci/ri
    return (data.frame(CI=ci,CR=cr))
}

#rescale three variables
rescalePCR<-function(data){
  newdata<-data %>%
    distinct(address,.keep_all = TRUE)%>%#remove duplicated
    mutate(scaleprice=scale(price)[,1],
           scalefood=scale(Restau)[,1],
           scalecrime=scale(crime)[,1])
  return(newdata)
}

#list top ten high score houses
getTopten<-function(weight,data){
  weightdata<-data%>% 
    mutate(score=-weight[1]*scaleprice+weight[2]*scalefood-weight[3]*scalecrime)%>%
    arrange(desc(score))
  weightdata$score<-rescale(weightdata$score,to = c(0, 100))
  return(weightdata[1:10,])
}

#list top ten houses according to user's choice
main<-function(input,data){
  originmatrix<-makematrix(input)
  ahpmatrix<-ahp(originmatrix)
  judgevalue<-calculateCIRI(ahpmatrix)
  print(judgevalue)#CI,CR<0.1
  weightvector<-ahpmatrix$Eigenvector
  rescaledata<-rescalePCR(data)
  toptenhouse<-getTopten(weightvector,rescaledata)
  return (toptenhouse)
}


############################################################################################################
############################################################################################################

#main

input1<-inputFilter()
ATLdata<-getdata()
FilteredData<-filterData(ATLdata,input1)
input2<-inputImportant()
topTen<-main(input2,FilteredData)

topTen



