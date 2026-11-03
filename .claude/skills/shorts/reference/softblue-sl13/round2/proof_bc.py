import sys,pathlib,json,cv2
sys.path.insert(0,str(pathlib.Path(__file__).parent));import batch as B
B.cv2=cv2
for S in 'BC':
 B.cmd_plan(S);B.cmd_track(S);B.cmd_cues(S);B.cmd_proof(S)
print('BC PROOF COMPLETE',flush=True)
