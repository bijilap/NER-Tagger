import operator
import sys
import random


class plearn:
    weights={}
    weights_avg={}
    labels={}
    min_file_content=[]
    
    def __init__(self):
        f=open(sys.argv[1],'r')
        file_content=[]
        value=1
        sign=1
        for line in f:
            file_content.append(line)
            words=line.split()
            if self.labels.has_key(words[0])==False: #line[0] is the label
                self.labels[words[0]]=value
                self.weights[words[0]]={}
                self.weights_avg[words[0]]={}
                sign=sign*-1
                if sign==1:
                    value=abs(value)+1
                value=value*sign
                
                
        for line in file_content:
            features=line.split()
            ylabel=features[0]
            del features[0]         
            fx={}
            for feature in features:
                if fx.has_key(feature)==False:
                    fx[feature]=1
                else:
                    fx[feature]+=1
                for k in self.labels:
                    if self.weights[k].has_key(feature)==False:
                        self.weights[k][feature]=0
            pair=[ylabel,fx]
            self.min_file_content.append(pair)
            
        #f.close()
        #print self.labels
        
        
    def predict(self,fx):
        wi={}
        for l in self.labels:
            wi[l]=0.0
        for feature in fx:
            for l in self.labels:
                #if self.weights[l].has_key(feature)==False:
                    #continue
                wi[l]+=self.weights[l][feature]*fx[feature]
        zlabel=max(wi.iteritems(), key=operator.itemgetter(1))[0]
        return zlabel
    
    def update_weight(self,fx,ylabel,zlabel):
        for feature in fx:
            self.weights[zlabel][feature]-=fx[feature]
            self.weights[ylabel][feature]+=fx[feature]
            
    def gen_model_file(self):
        f=open(sys.argv[2],'w')
        for l in self.labels:
            f.write(l+"\t"+str(self.labels[l])+' ')
        f.write('\n')
        for l in self.labels:
            for ft in self.weights_avg[l]:
        #print ft
                f.write(l+" "+ft+" "+str(self.weights_avg[l][ft])+'\n')
        #f.close()
        
    def update_avg_weight(self):
        for l in self.labels:
            for f in self.weights[l]:
                if self.weights_avg[l].has_key(f)==False:
                    self.weights_avg[l][f]=float(self.weights[l][f])
                else:
                    self.weights_avg[l][f]=self.weights_avg[l][f]+float(self.weights[l][f])
        
        
    def calculate_avg_weight(self,N):
        for l in self.labels:
            for f in self.weights_avg[l]:
                self.weights_avg[l][f]=float(self.weights_avg[l][f]/N)
 
    def learn(self,N):
        for i in range(0,N):
        #f=open(fname,'r')
            random.shuffle(self.min_file_content)
            sys.stderr.write('iteration count:'+str(i+1)+'\n')
            for pair in self.min_file_content:
                #features=line.split()
                ylabel=pair[0]
                y=self.labels[ylabel] #the value of the label        
                fx=pair[1]           
                zlabel=self.predict(fx)
                z=self.labels[zlabel]
                if z!=y:
		    
                    self.update_weight(fx,ylabel,zlabel)
                
            self.update_avg_weight()
                
        self.calculate_avg_weight(N)
                
#fname=str(sys.argv[1]) #input file name
#oname=str(sys.argv[2]) #output file name
n=20
argc=len(sys.argv)
if argc>3:
    if sys.argv[3]=='-i':
    	n=int(sys.argv[4])
    
pl=plearn()
pl.learn(n)     
pl.gen_model_file()
