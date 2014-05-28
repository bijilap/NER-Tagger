import sys
import operator


class nclassify:
    weights={}
    labels={}

    def __init__(self,fname):
        f=open(fname,'r')
        lline=f.readline().rstrip().split(' ')
    #print lline
        for l in lline:
            val=l.split('\t')
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
    
    def classify(self,tfile):
        fl=open(tfile,'r')
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
        
    def classify_line(self,line):
        features=line.split()
        fx={}
        for feature in features:
            if fx.has_key(feature)==False:
                fx[feature]=1
            else:
                fx[feature]+=1
        zlabel=self.predict(features,fx)
        return zlabel


class netag:
    pc=object 
    def __init__(self,fname):
        self.pc=nclassify(fname)

    def classify(self):
        
        f=sys.stdin
        for line in f:
            words=line.split()
            pword='BOS' #previous word
	    ppostag='BOS'
            nword='EOS' #next word
	    npostag='EOS'
	    pnetag='None' #previous netag
            outline=''
	    pwprefix='None'
	    wprefix='None'
	    nwprefix='None'
            for i in range(len(words)):
		word_list=words[i].split('/')
		postag=word_list[len(word_list)-1]
                word=words[i][:len(words[i])-((len(postag))+1)]
		#wprefix=word[0]
                #print word+" "+tag
                if i+1>=len(words):
                    nword='EOS'
		    npostag='EOS'
		    nwprefix='None'
                else:
		    word_list=words[i+1].split('/')
		    npostag=word_list[len(word_list)-1]
                    nword=words[i+1][:len(words[i+1])-((len(npostag))+1)]
                    #nword=words[i+1]
		    #print words[i+1]
		    #nwprefix=nword[0]
                feature="pw:"+str(pword)+" w:"+str(word)+" nw:"+str(nword)+" pnetag:"+str(pnetag)+" ppostag:"+str(ppostag)+" postag:"+str(postag)+ " npostag:"+str(npostag)
		#print feature
                label=self.pc.classify_line(feature)
		pnetag=label
	        ppostag=postag
                pword=word
		#pwprefix=pword[0]
                outline=outline+word+'/'+postag+'/'+label+' '
       	    print outline
            #sys.stdout.write(outline+'\n') 
        f.close()
        
mod_file=sys.argv[1]
pt=netag(mod_file)
pt.classify()
