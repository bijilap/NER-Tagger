import sys
import subprocess

class netrain:
    feature_set={}
    features_fname='ne.in'
    model_fname="ne.model"
    
    def __init__(self,mname):
        self.model_fname=mname
        
        
    def read_training_file(self,fname):
        f=open(fname,'r')
        fout=open(self.features_fname,'w')
        for line in f:
            #print line
            pword='BOS' #previous word
	    ppostag='BOS' #previous POS tag
            nword='EOS' #next word
	    npostag='EOS'
	    pnetag='None' #previous netag
	    pwprefix='None'
	    wprefix='None'
	    nwprefix='None'
            words_tags=line.split()
            for i in range(len(words_tags)):
		#print words_tags[i]+' '+str(len(words_tags[i].split('/')))
		#if len(words_tags[i].split('/'))>3:
			#print 'here'
			#continue
		word_list=words_tags[i].split('/')
		postag=word_list[len(word_list)-2]
		netag=word_list[len(word_list)-1]
		word=words_tags[i][:len(words_tags[i])-((len(postag)+len(netag))+2)]
                #(word,postag,netag)=
		wprefix=word[0]
                #word=word+'/'+postag
                #print word+" "+tag
                if i+1>=len(words_tags):
                    nword='EOS'
	    	    npostag='EOS'
		    nwprefix='None'
                else:
		    word_list=words_tags[i+1].split('/')
		    npostag=word_list[len(word_list)-2]
                    nword=words_tags[i+1][:len(words_tags[i+1])-((len(word_list[len(word_list)-2])+len(word_list[len(word_list)-1]))+2)]
		    #nwprefix=nword[0]
                feature=netag+" "+"pw:"+str(pword)+" w:"+str(word)+" nw:"+str(nword)+" pnetag:"+str(pnetag)+" ppostag:"+str(ppostag)+" postag:"+str(postag)+ " npostag:"+str(npostag)+'\n'
		#print feature
		pnetag=netag
                pword=word
		ppostag=postag
		#pwprefix=pword[0]
                fout.write(feature)
                #print feature
        f.close()
        fout.close
        
    def learn(self):
        subprocess.call('python ./perceplearn.py '+self.features_fname+' '+self.model_fname+' -i 20',shell=True)

fname=sys.argv[1]
mname=sys.argv[2]
pobj=netrain(mname)
pobj.read_training_file(fname)
pobj.learn()
pobj.read_training_file(fname)
