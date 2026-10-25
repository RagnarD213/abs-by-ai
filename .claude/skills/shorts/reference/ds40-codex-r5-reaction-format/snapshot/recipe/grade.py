import numpy as np,cv2

def grade(x,mode):
 if mode=='natural': gains=[.985,1,1.035];sat=.94;exposure=1.035;con=1.035
 elif mode=='warm': gains=[1.01,1,1.015];sat=1.04;exposure=1.035;con=1.045
 else:gains=[.985,1.005,1.035];sat=.98;exposure=1.075;con=1.055
 x=x*np.array(gains,np.float32);y=np.sum(x*np.array([.2126,.7152,.0722]),-1,keepdims=True)
 x=y+sat*(x-y);x=np.maximum(x,0)**.97*exposure;x=(x-.18)*con+.18
 return np.clip(x,0,1)
