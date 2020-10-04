print('')
print('+------------------------------------------------------------------+')
print('|  StackWalk Ver 1 (August 2020). Python implementation.           |')
print('|  Lattice Stacker and Maximal Chain Computer                      |')
print('+------------------------------------------------------------------+')
print('')
# point p is encoded as a number whose base k+m+1 representation gives coordinates of the point 

def generatePoints(k,n,m):
    return 0

def isValidPoint(num,k, n, m):
    point=decodePoint(num, k, n, m)
    for i in range(1,n):
        if point[i]<k:
            if point[i]<point[i-1]:
                return False
    return True

def encodePoint(point, k, n, m):
    num=0
    for i in range(0,n):
        num=num+((k+m+1)**(n-1-i))*point[i]
    return num

def decodePoint(num, k, n, m):
    point=[]
    while num:
        point.insert(0,int(num % (k+m+1)))
        num = int(num / (k+m+1))
    while n-len(point):
        point.insert(0,0)
    return point

def pointHeight(num, k, n, m):
    point=decodePoint(num, k, n, m)
    height=0
    for i in range(0,n):
        height=height+point[i]
    return height

def isNext(point1, point2, n):
    distance=0
    for i in range(0,n):
        if point2[i]<point1[i]:
            return False
        distance=distance+(point2[i]-point1[i])
    if distance==1:
        return True
    return False

def assignWeights(k,n,m):
    weight=[0 for i in range(0,(k+m+1)**n)]
    weight[0]=1
    for h in range(0,(k+m)*n):
        for i in range(0,(k+m+1)**n):
            if pointHeight(i,k,n,m)==h and isValidPoint(i, k, n, m):
                point1=decodePoint(i,k,n,m)
                for j in range(0,(k+m+1)**n):
                    if pointHeight(j,k,n,m)==h+1 and isValidPoint(j, k, n, m):
                        point2=decodePoint(j,k,n,m)
                        if isNext(point1,point2,n):
                            weight[j]=weight[j]+weight[i]
    return weight

def printLattice(k,n,m):
    print('digraph G{')
    print('graph[splines="line",rankdir="LR",dpi = 300];')
    print('node[imagescale=false,fixedsize="false",width="0",height="0",color="gray"];')
    print('edge[arrowhead=vee, arrowsize=0.5];')
    weight=assignWeights(k,n,m)
    for i in range(0,(k+m+1)**n):
        if isValidPoint(i,k,n,m):
            print(str(i)+'[label="'+str(weight[i])+'"];')
    for i in range(0,(k+m+1)**n):
        if isValidPoint(i, k, n, m):
            point1=decodePoint(i,k,n,m)
            for j in range(0,(k+m+1)**n):
                if isValidPoint(j, k, n, m):
                    point2=decodePoint(j,k,n,m)
                    if isNext(point1,point2,n):
                        print(str(i)+' -> '+str(j))
    print('}')

def printTikz(k,n,m,xvec,yvec):    
    print('\\begin{tikzpicture}')
    print('\\node at(0,-1){$\\Sigma^'+str(k)+'_'+str(n)+'C^'+str(n)+'_'+str(m)+'$};')
    print('\\tikzset{every node/.style={shape=circle,draw=black,fill=white,inner sep=1pt,outer sep=0pt}}')

    coordinates=getCoordinates(k,n,m,xvec,yvec)
    for i in range(0,(k+m+1)**n):
        if isValidPoint(i,k,n,m):
            print('\\node ('+str(i)+') at('+str(coordinates[i][0])+','+str(coordinates[i][1])+'){};')
    
    for i in range(0,(k+m+1)**n):
        if isValidPoint(i, k, n, m):
            point1=decodePoint(i,k,n,m)
            for j in range(0,(k+m+1)**n):
                if isValidPoint(j, k, n, m):
                    point2=decodePoint(j,k,n,m)
                    if isNext(point1,point2,n):
                        print('\\path ('+str(i)+') edge ('+str(j)+');')
    
    print('\\end{tikzpicture}')

def getCoordinates(k,n,m,xvec,yvec):
    coordinates=[]
    for i in range(0,(k+m+1)**n):
        point=decodePoint(i, k, n, m)
        xcoordinate=0
        ycoordinate=0
        for j in range(0,n):
            xcoordinate=xcoordinate+point[j]*xvec[j]
            ycoordinate=ycoordinate+point[j]*yvec[j]
        coordinates.append([xcoordinate,ycoordinate])
    return coordinates

    
def test(what):
    if what=='point encoder decoder':
        for i in range(0,10):
            print(decodePoint(i,2,4,1))
            print(encodePoint(decodePoint(i,2,4,1),2,4,1))
    if what=='valid point':
        for i in range(0,100):
            print(str(decodePoint(i,2,4,1))+' is valid: '+str(isValidPoint(i,2,4,1)))
    if what=='point height':
        for i in range(0,50):
            print(str(decodePoint(i,2,4,1))+' has height: '+str(pointHeight(i,2,4,1)))
    if what=='is next point':
        print(isNext([0,1,0,3],[0,2,0,2],4))
    if what=='assign weights':
        for m in range(1,2):
            print('When m='+str(m)+':')
            for k in range(5,6):
                output=('Iteration k='+str(k)+': ')
                for n in range(0,5):
                    output=output+str(assignWeights(k,n,m)[(k+m+1)**n-1])+', '
                print(output)
    if what=='get coordinates':
        print(getCoordinates(1,3,2,[1,1,0],[0,1,1]))


printTikz(1,0,2,[0],[0])
printTikz(1,1,2,[0.7],[0.5])
printTikz(1,2,2,[-0.5,0.7],[1,0.5])
printTikz(1,3,2,[1,-0.5,0.7],[0.2,1,0.5])
printTikz(1,4,2,[-0.3,1,-0.5,0.7],[1.6,0.2,1,0.5])