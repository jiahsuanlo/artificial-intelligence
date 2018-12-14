# -*- coding: utf-8 -*-
import os
import re

def ParseResultFile(filename):
    results={}
    
    with open(filename, mode= 'r') as f:
        read_next= False
        for line in f:
            # read plan stats
            if read_next:
                items= re.findall("[0-9.]+", line)
                results["NumOfActions"]= int(items[0])
                results["NumOfExpansions"]= int(items[1])
                results["NumOfGoalTests"]= int(items[2])
                results["NumOfNewNodes"]= int(items[3])
            
            
            if line.startswith('#'):
                read_next= True
            elif line.startswith("Plan"):
                items= re.findall("[0-9.]+", line)
                results["ElapsedTime"]= float(items[1])
                results["PlanLength"]= int(items[0])
                read_next= False
            else:
                read_next= False
                                   
    return results 

def BatchRunSearch(probs, algs):
    for pb in probs:
        for ag in algs:
            out_file= "out_p%d_s%d.txt"%(pb,ag)
            cmd_str= "python run_search.py -p %d -s %d > %s"%(pb, ag, out_file)
            os.system(cmd_str)
            
def PostProcResults(probs, algs, filename= "summary.csv"):
    fid= open(filename, mode="w")
    fid.write("Problem,Alg,Actions,Expansions,GoalTests,NewNodes,PlanLength,ElapsedTime\n")
    for pb in probs:
        for ag in algs:
            out_file= "out_p%d_s%d.txt"%(pb,ag)
            res= ParseResultFile(out_file)
            fid.write("%d,%d,%d,%d,%d,%d,%d,%f\n"%(pb,ag,\
                                             res["NumOfActions"],\
                                             res["NumOfExpansions"],\
                                             res["NumOfGoalTests"],\
                                             res["NumOfNewNodes"],\
                                             res["PlanLength"],\
                                             res["ElapsedTime"]))
    fid.close()     
            
        
    
if __name__=="__main__":
    
    probs=[1,2]
    algs= [1,2,3,4,5,6,7,8,9,10,11]
    
    probs=[1]
    algs= [1,2,3,4]
    
    # batch run
    BatchRunSearch(probs, algs)
    
    # Post Proc Results
    PostProcResults(probs, algs)




