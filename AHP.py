import math
originmatrix=[[0,0,0],[0,0,0],[0,0,0]]
crimeprice=[5,1/3,1/9]
crimefood=[1/3,1/5,1/3]
pricecrime=[7,3,1/5]
pricefood=[3,9,7]
foodprice=[1/3,5,7]
foodcrime=[1/9,1/3,5]
def makematrix(matrix,ratiolist):
    for i in range(3):
        matrix[i][i]=1
    matrix[0][1] = ratiolist[0]
    matrix[1][0] = 1/ratiolist[0]
    matrix[0][2] = ratiolist[1]
    matrix[2][0] = 1/ratiolist[1]
    matrix[1][2] = ratiolist[2]
    matrix[2][1] = 1/ratiolist[2]
    return matrix
def ahpmatrix(matrix):
    sum=0
    rootproductslist=[]
    for row in matrix:
        rootproducts=math.pow(row[0]*row[1]*row[2], 1/3)
        row.append(rootproducts)
        rootproductslist.append(rootproducts)
        sum+=rootproducts
    for i in range(3):
        rootproductslist[i]=rootproductslist[i]/sum
        matrix[i].append(rootproductslist[i])
    for row in matrix:
        mmult=row[0]*rootproductslist[0]+row[1]*rootproductslist[1]+row[2]*rootproductslist[2]
        row.append(mmult/row[4])
    return matrix
def calculateCIRI(matrix):
    cisum=0
    for row in matrix:
        cisum+=row[5]
    ci=(cisum/3-3)/2
    ri=0.58
    ratio=ci/ri
    return [float('%.8f' % ci),ri,float('%.8f' % ratio)]
def makeweightlist(matrix):
    weightlist=[]
    for row in matrix:
        weightlist.append(float('%.2f' % row[4]))
    return weightlist
k=makematrix(originmatrix,foodcrime)
j=ahpmatrix(k)
print(j)
a=calculateCIRI(j)
print(a)
j=makeweightlist(j)
print(j)


