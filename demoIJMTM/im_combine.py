import cv2
import numpy as np,sys

def pyramid_Hblending(img):
    #read picture

    #img=[]
    x=len(img)
    #for n in path:
     #   img.append(cv2.imread(n))
    

    #same the height
    height=500
    for i,n in enumerate(img):
        wr=float(height)*n.shape[1]/n.shape[0]
        wr=int(wr)
        img[i]=cv2.resize(img[i],(wr,height),interpolation=cv2.INTER_AREA)
        #print wr


        
    #resize for 2**
    
    #for hi 
    hi=0
    
    while(2**hi<height):
        hi=hi+1
    #if (2*height)<(2**hi+2**(hi-1)):
    hi=hi-1
    #new_height=2**hi

    #for wi
    wi=[]
    #new_width=[]
    
    for n in img:
        w=0
        while(2**w<n.shape[1]):
            w=w+1
        #if(2*n.shape[1])<(2**w+2**(w-1)):
        w=w-1
        wi.append(w)
        #new_width.append(2**w)
        #print 2**w

    '''#resize img to 2**
    imgr=[]
    for i,n in enumerate(img):
        Tr=cv2.resize(n,(new_width[i],new_height),interpolation=cv2.INTER_AREA)
        imgr.append(Tr)'''

    imgr=img



    #find smallest
    m=min(wi,hi)

    if m>6:
        m=6

    M=m-1
    #print m



    #pyramid blending

    #Generate Gaussion pyramid for imgr
    gp=[]
    for j,n in enumerate(imgr):
        G=n.copy()
        gpn=[G]
        for i in xrange(m):
            G=cv2.pyrDown(G)
            gpn.append(G)
        gp.append(gpn)
            
        

    #Generate Laplacian Pyramid for img1
    lp=[]
    for j,n in enumerate(gp):
        lpn=[n[M]]
        for i in xrange(M,0,-1):
            GE=cv2.pyrUp(n[i])
            GE=cv2.resize(GE,(n[i-1].shape[1],n[i-1].shape[0]),interpolation=cv2.INTER_AREA)
            L=cv2.subtract(n[i-1],GE)
            lpn.append(L)
        lp.append(lpn)
    X=M+1
    #print X

        

    #Now add halves of image in each level
    LS=[]
    for i in xrange(0,X):
        ls=lp[0][i][:,0:(lp[0][i].shape[1]/x)]
        for j in xrange(1,x):
            ls = np.hstack((ls, lp[j][i][:,(lp[j][i].shape[1]*j/x):(lp[j][i].shape[1]*(j+1)/x)]))
        LS.append(ls)
            
        
    


    #now reconstruct
    
    for i in xrange(1,X):
        LS[i]=cv2.resize(LS[i],(2*LS[i-1].shape[1],2*LS[i-1].shape[0]),interpolation=cv2.INTER_AREA)

    ls_=LS[0]
    for i in xrange(1,m):
        ls_=cv2.pyrUp(ls_)
        ls_=cv2.add(ls_,LS[i])

    return ls_







def pyramid_Vblending(img):
    #read picture
    #img=[]
    x=len(img)
    #for n in path:
     #   img.append(cv2.imread(n))
    

    #same the width
    width=700
    for i,n in enumerate(img):
        hr=float(width)*n.shape[0]/n.shape[1]
        hr=int(hr)
        img[i]=cv2.resize(img[i],(width,hr),interpolation=cv2.INTER_AREA)
        #print hr


        
    #resize for 2**
    
    #for wi 
    wi=0
    
    while(2**wi<width):
        wi=wi+1
    #if (2*height)<(2**hi+2**(hi-1)):
    wi=wi-1
    #new_height=2**hi

    #for hi
    hi=[]
    #new_width=[]
    
    for n in img:
        h=0
        while(2**h<n.shape[0]):
            h=h+1
        h=h-1
        hi.append(h)

        #print 2**h

    '''#resize img to 2**
    imgr=[]
    for i,n in enumerate(img):
        Tr=cv2.resize(n,(new_width[i],new_height),interpolation=cv2.INTER_AREA)
        imgr.append(Tr)'''

    imgr=img



    #find smallest
    m=min(wi,hi)

    if m>6:
        m=6

    M=m-1
    #print m



    #pyramid blending

    #Generate Gaussion pyramid for imgr
    gp=[]
    for j,n in enumerate(imgr):
        G=n.copy()
        gpn=[G]
        for i in xrange(m):
            G=cv2.pyrDown(G)
            gpn.append(G)
        gp.append(gpn)
            
        

    #Generate Laplacian Pyramid for img1
    lp=[]
    for j,n in enumerate(gp):
        lpn=[n[M]]
        for i in xrange(M,0,-1):
            GE=cv2.pyrUp(n[i])
            GE=cv2.resize(GE,(n[i-1].shape[1],n[i-1].shape[0]),interpolation=cv2.INTER_AREA)
            L=cv2.subtract(n[i-1],GE)
            lpn.append(L)
        lp.append(lpn)
    X=M+1
    #print X

        

    #Now add halves of image in each level
    LS=[]
    for i in xrange(0,X):
        ls=lp[0][i][0:(lp[0][i].shape[0]/x),:]
        for j in xrange(1,x):
            ls = np.vstack((ls, lp[j][i][(lp[j][i].shape[0]*j/x):(lp[j][i].shape[0]*(j+1)/x),:]))
        LS.append(ls)
            
        
    


    #now reconstruct
    
    for i in xrange(1,X):
        LS[i]=cv2.resize(LS[i],(2*LS[i-1].shape[1],2*LS[i-1].shape[0]),interpolation=cv2.INTER_AREA)

    ls_=LS[0]
    for i in xrange(1,m):
        ls_=cv2.pyrUp(ls_)
        ls_=cv2.add(ls_,LS[i])

    return ls_
    



def direct_Hcon(img):
    #read picture
    #img=[]
    x=len(img)
    #for n in path:
     #   img.append(cv2.imread(n))
    

    #same the height
    height=500
    for i,n in enumerate(img):
        wr=float(height)*n.shape[1]/n.shape[0]
        wr=int(wr)
        img[i]=cv2.resize(img[i],(wr,height),interpolation=cv2.INTER_AREA)

    #hstack
    fim=img[0][:,0:(img[0].shape[1]/x)]
    for i in xrange(1,x):
        fim = np.hstack((fim, img[i][:,(img[i].shape[1]*i/x):(img[i].shape[1]*(i+1)/x)]))

    return fim



def direct_Vcon(img):
    #read picture
    #img=[]
    x=len(img)
    #for n in path:
     #   img.append(cv2.imread(n))
    

    #same the width
    width=700
    for i,n in enumerate(img):
        hr=float(width)*n.shape[0]/n.shape[1]
        hr=int(hr)
        img[i]=cv2.resize(img[i],(width,hr),interpolation=cv2.INTER_AREA)

    #hstack
    fim=img[0][0:(img[0].shape[0]/x),:]
    for i in xrange(1,x):
        fim = np.vstack((fim, img[i][(img[i].shape[0]*i/x):(img[i].shape[0]*(i+1)/x),:]))

    return fim



'''def weighted_pyr_H(path):
    front_path=path[0:-1]
    #print front_path

    front_img = pyramid_Hblending(front_path)

    back_img = cv2.imread(path[-1])

    height = 500

    #resize
    wr=float(height)*front_img.shape[1]/front_img.shape[0]
    wr=int(wr)
    front_img=cv2.resize(front_img,(wr,height),interpolation=cv2.INTER_AREA)

    wr=float(height)*back_img.shape[1]/back_img.shape[0]
    wr=int(wr)
    back_img=cv2.resize(back_img,(wr,height),interpolation=cv2.INTER_AREA)

    if front_img.shape[1]<back_img.shape[1]:
        back_mask=back_img[:,0:front_img.shape[1]]
        left_mask=cv2.addWeighted(front_img,0.6,back_mask,0.4,0)
        fim=np.hstack((left_mask,back_img[:,front_img.shape[1]:]))
    else:
        front_mask=front_img[:,0:back_img.shape[1]]
        left_mask=cv2.addWeighted(front_mask,0.6,back_img,0.4,0)
        fim=np.hstack((left_mask,front_img[:,back_img.shape[1]:]))

    return fim'''


def weighted_pyr_H(img):
    #front_path=path[0:-1]
    #print front_path
    x_img=len(img)

    if x_img==1:
        front_img = pyramid_Hblending([img[0]])
    else:
        front_img = pyramid_Hblending(img[0:-1])
        


    back_img = img[-1]




    #resize
    height = 500
    wr=float(height)*back_img.shape[1]/back_img.shape[0]
    wr=int(wr)
    back_img=cv2.resize(back_img,(wr,height),interpolation=cv2.INTER_AREA)


    front_img=cv2.resize(front_img,(back_img.shape[1],back_img.shape[0]),interpolation=cv2.INTER_AREA)

    fim=cv2.addWeighted(front_img,0.7,back_img,0.3,0)



    return fim




def weighted_pyr_V(img):

    x_img=len(img)

    if x_img==1:
        front_img = pyramid_Vblending([img[0]])
    else:
        front_img = pyramid_Vblending(img[0:-1])
        
    

    back_img = img[-1]




    #resize
    width = 700
    hr=float(width)*back_img.shape[0]/back_img.shape[1]
    hr=int(hr)
    back_img=cv2.resize(back_img,(width,hr),interpolation=cv2.INTER_AREA)


    front_img=cv2.resize(front_img,(back_img.shape[1],back_img.shape[0]),interpolation=cv2.INTER_AREA)

    fim=cv2.addWeighted(front_img,0.7,back_img,0.3,0)



    return fim


    
##################################################################
def Pure_overlapping(img):
    #read picture
    #img=[]
    x=len(img)
    #for n in path:
    #    img.append(cv2.imread(n))


    #same the height
    height=500
    width=float(height)*img[0].shape[1]/img[0].shape[0]

    #resize
    for i,n in enumerate(img):
        dim=(int(width),int(height))
        img[i]=cv2.resize(img[i],dim,interpolation=cv2.INTER_AREA)



    #method 1:
    if x==1:
        fim=img[0]
    else:
        fim=cv2.addWeighted(img[0],1/float(x),img[1],1/float(x),0)
        for i in xrange(2,x):
            fim=cv2.addWeighted(fim,1,img[i],1/float(x),0)



    #method 2
    #for i in xrange(0,x):
    #    if i==0:
    #        fim=cv2.addWeighted(img[0],1/float(x),img[1],1/float(x),0)
    #    else:
    #        fim=cv2.addWeighted(fim,1,img[i],1/float(x),0)


    return fim

#############################################################
def HTri(img):

    #read picture
    #img=[]
    x=len(img)
    #for n in path:
    #    img.append(cv2.imread(n))

    #same the height
    height=500
    r=float(height)/img[0].shape[0]
    width=img[0].shape[1]*r
    width=int(width)

    hfheight=int(height)/2
    hfwidth=int(width)/2

    #resize
    dim=(int(width),int(height))
    resized1=cv2.resize(img[0],dim,interpolation=cv2.INTER_AREA)
    resized2=cv2.resize(img[1],dim,interpolation=cv2.INTER_AREA)

    cropped=np.ndarray(shape=(int(height),int(width),3),dtype='uint8')

    mask1 = np.zeros(resized1.shape, dtype=np.uint8)
    roi_corners1 = np.array([[(hfwidth,0), (0,hfheight), (hfwidth,height)]], dtype=np.int32)
    white1 = (255, 255, 255)
    cv2.fillPoly(mask1, roi_corners1, white1)

    mask2 = np.zeros(resized1.shape, dtype=np.uint8)
    roi_corners2 = np.array([[(hfwidth,0), (width,hfheight), (hfwidth,height)]], dtype=np.int32)
    white2 = (255, 255, 255)
    cv2.fillPoly(mask2, roi_corners2, white2)

    masked_image1 = cv2.bitwise_and(resized1, mask1)
    masked_image2 = cv2.bitwise_and(resized2, mask2)

    fim=np.ndarray(shape=(int(height),int(width),3),dtype='uint8')

    fim[0:,0:hfwidth]=masked_image1[0:,0:hfwidth]
    fim[0:,hfwidth:]=masked_image2[0:,hfwidth:]

    return fim


def VTri(img):

    #read picture
    #img=[]
    x=len(img)
    #for n in path:
    #    img.append(cv2.imread(n))

    #same the width
    width=700
    r=float(width)/img[0].shape[1]
    height=img[0].shape[0]*r
    height=int(height)

    hfheight=int(height)/2
    hfwidth=int(width)/2

    #resize
    dim=(int(width),int(height))
    resized1=cv2.resize(img[0],dim,interpolation=cv2.INTER_AREA)
    resized2=cv2.resize(img[1],dim,interpolation=cv2.INTER_AREA)

    cropped=np.ndarray(shape=(int(height),int(width),3),dtype='uint8')

    mask1 = np.zeros(resized1.shape, dtype=np.uint8)
    roi_corners1 = np.array([[(0,hfheight), (hfwidth,height), (width,hfheight)]], dtype=np.int32)
    white1 = (255, 255, 255)
    cv2.fillPoly(mask1, roi_corners1, white1)

    mask2 = np.zeros(resized1.shape, dtype=np.uint8)
    roi_corners2 = np.array([[(0,hfheight), (hfwidth,0), (width,hfheight)]], dtype=np.int32)
    white2 = (255, 255, 255)
    cv2.fillPoly(mask2, roi_corners2, white2)

    masked_image1 = cv2.bitwise_and(resized1, mask1)
    masked_image2 = cv2.bitwise_and(resized2, mask2)

    fim=np.ndarray(shape=(int(height),int(width),3),dtype='uint8')

    fim[hfheight:,0:]=masked_image1[hfheight:,0:]
    fim[0:hfheight,0:]=masked_image2[0:hfheight,0:]


    return fim


























    
    
