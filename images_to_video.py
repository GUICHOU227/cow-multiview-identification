# images_to_video
import cv2
import glob
import re
import os
def images2video(path, result_name, fps = 1): # 設定fps
    # 有幾張影像
    frame_list = sorted(glob.glob(path))
    print("frame count: ",len(frame_list))
    
    # fps = 5 # 設定fps
    # fps = 12 # 設定fps
    # 設定大小
    shape = cv2.imread(frame_list[0]).shape # delete dimension 3
    size = (shape[1], shape[0])
    print("frame size: ",size)
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(result_name, fourcc, fps, size)
    
    for idx, path in enumerate(frame_list):
        frame = cv2.imread(path)
        # print("\rMaking videos: {}/{}".format(idx+1, len(frame_list)), end = "")
        current_frame = idx+1
        total_frame_count = len(frame_list)
        percentage = int(current_frame*30 / (total_frame_count+1))
        print("\rProcess: [{}{}] {:06d} / {:06d}".format("#"*percentage, "."*(30-1-percentage), current_frame, total_frame_count), end ='')
        out.write(frame)
    
    out.release()
    print()
    print("Finish making video !!!")

if __name__ == '__main__':
    # 來源資料夾
    path = input("請輸入來源資料夾：")
    name = re.search(r'[\w]*$', path).group()
    path += r"\*.jpg"
    result_name = input("請輸入目的地資料夾：")
    result_name += r"/output.mp4"
    images2video(path, result_name, fps=15*5)
    
    
    
    
    
    
    
    
    