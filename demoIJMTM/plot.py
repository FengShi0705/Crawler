import matplotlib.pyplot as plt
import matplotlib
import cv2
import matplotlib.gridspec as gridspec
import time


def im_plot(img,nouns,show_text,show_or_draw):

    for i,n in enumerate(img):
        img[i]=n[:, :, ::-1].copy()

    x=len(img)
    print 'show_im '+str(show_or_draw)



    #if show_or_draw==1:
    plt.close()
    plt.figure(1,figsize=(16,12))






    if x==1:
        plt.imshow(img[-1])
        plt.title(show_text,fontsize=25, fontweight='bold',color='red')
        plt.xticks([]), plt.yticks([])

    else:
        gs1=gridspec.GridSpec(5, (x-1))
        gs1.update(left=0.02, right=0.98, top=0.95, bottom=0.02, wspace=0.0 ,hspace=0.17)


        for i,n in enumerate(img[:-1]):
            plt.subplot(gs1[0:2,i])
            plt.imshow(n)
            plt.title(nouns[i],fontsize=22)
            plt.xticks([]), plt.yticks([])



        fig = plt.subplot(gs1[2:,:])
        fig.spines['bottom'].set_color('red')
        fig.spines['top'].set_color('red')
        fig.spines['left'].set_color('red')
        fig.spines['right'].set_color('red')


        fig.spines['bottom'].set_linewidth('5')
        fig.spines['top'].set_linewidth('5')
        fig.spines['left'].set_linewidth('5')
        fig.spines['right'].set_linewidth('5')



        plt.imshow(img[-1])
        plt.title(show_text,fontsize=25, fontweight='bold',color='red')
        plt.xticks([]), plt.yticks([])



    plt.draw()









