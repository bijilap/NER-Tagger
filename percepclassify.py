import operator
import sys


class pclassify:
    weights={}
    labels={}

    def __init__(self,fname):
        f=open(fname,'r')
        lline=f.readline().rstrip().split(' ')
	#print lline
        for l in lline:
            val=l.split('\t')
	    #print val
            self.labels[val[0]]=int(val[1])
            self.weights[val[0]]={}
        for l in f:
            param=l.split()
            self.weights[param[0]][param[1]]=float(param[2])
        f.close()
        #print self.labels

    def predict(self,features,fx):
        wi={}
        for l in self.labels:
            wi[l]=0.0
        for feature in fx:
            for l in self.labels:
                if self.weights[l].has_key(feature)==False:
                    continue
                wi[l]+=self.weights[l][feature]*fx[feature]
        zlabel=max(wi.iteritems(), key=operator.itemgetter(1))[0]
        return zlabel
    
    def classify(self):
        #fl=open(tfile,'r')
	fl=sys.stdin
        for line in fl:
            features=line.split()
            fx={}
            for feature in features:
                if fx.has_key(feature)==False:
                    fx[feature]=1
                else:
                    fx[feature]+=1
            zlabel=self.predict(features,fx)
            print zlabel
        fl.close()

pc=pclassify(str(sys.argv[1]))
#pc.classify(str(sys.argv[2]))
pc.classify()
