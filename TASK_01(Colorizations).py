import numpy as np
import cv2


prototxt_path =  "E:/PPYTHON/TXON INTERNSHIP/Task-01/colorization-caffe/models/colorization_deploy_v2.prototxt"
model_path = "E:/PPYTHON/TXON INTERNSHIP/Task-01/colorization_release_v2.caffemodel"
kernel_path = 'E:/PPYTHON/TXON INTERNSHIP/Task-01/colorization-caffe/resources/pts_in_hull.npy'
image_path  = 'E:/PPYTHON/TXON INTERNSHIP/Task-01/colorization-caffe/demo/imgs/leaf.jpg'

net = cv2.dnn.readNetFromCaffe(prototxt_path,model_path)
points= np.load(kernel_path)

points = points.transpose().reshape(2,313,1,1)
net.getLayer(net.getLayerId("class8_ab")).blobs = [points.astype(np.float32)]
net.getLayer(net.getLayerId("conv8_313_rh")).blobs = [np.full([1,313],2.606,dtype="float32")]


bw_image =  cv2.imread(image_path)
normalized  = bw_image.astype("float32")/255.0
lab = cv2.cvtColor(normalized,cv2.COLOR_BGR2LAB)

resized = cv2.resize(lab,(230,230))
L= cv2.split(resized)[0]
L -= 50
net.setInput(cv2.dnn.blobFromImage(L))
ab = net.forward()[0,:,:,:].transpose((1,2,0))

ab=cv2.resize(ab,(bw_image.shape[1],bw_image.shape[0]))
L= cv2.split(lab)[0]


colorized= np.concatenate((L[:,:,np.newaxis],ab),axis=2)
colorized = cv2.cvtColor(colorized,cv2.COLOR_LAB2BGR)
colorized = (255.0* colorized).astype("uint8")

# Display the colorized image
cv2.imshow("Black and White Images",bw_image)
cv2.imshow("After colorization",colorized)
cv2.waitKey(0)
cv2.destroyAllWindows()