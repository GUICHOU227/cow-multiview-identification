from flask import render_template
from flask import Flask, request
from werkzeug.utils import secure_filename
import subprocess
import cv2
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import copy
from os.path import join
from tracking_jpg_onlycow import tracking

#進食時長：exp25_414 -> tracking_jpg_EatingTime
#軌跡追蹤：exp42_691 -> tracking_jpg_onlycow
#姿勢辨識：exp51_313 -> images_to_video
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = r'C:\Users\ZongZhun\PycharmProjects\pythonProject\yolov7-main\temp'  # 指定暫存目錄
app.config['RUNS_FOLDER'] = r'C:\Users\ZongZhun\PycharmProjects\pythonProject\yolov7-main\runs\detect'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'jpg'}  # 允許的檔案類型

def allowed_file(filename):
    # 檢查檔案副檔名是否在允許的檔案類型中
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route("/") #函式的裝飾
def index():
    return render_template("index.html")

@app.route("/detectp")
def detectp():
    return render_template("detectp.html")

@app.route("/detectt")
def detectt():
    return render_template("detectt.html")

@app.route("/detecte")
def detecte():
    return render_template("detecte.html")


def images_to_video(image_paths, video_path, fps=10.0):
    img = cv2.imread(image_paths[0])
    height, width, _ = img.shape

    # 修改編碼器為 H.264 (MP4)
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    video = cv2.VideoWriter(video_path, fourcc, fps, (width, height))

    for image_path in image_paths:
        img = cv2.imread(image_path)
        video.write(img)

    video.release()

@app.route('/uploadp', methods=['GET', 'POST'])
def upload_folderp():
    if request.method == 'POST':
        folder = request.files.getlist('folder')  # 取得上傳的檔案列表
        file_paths = []  # 儲存上傳檔案的路徑
        for file in folder:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
        cmd = [
            'python',
            'detect_cow_shed.py',
            '--weights',
            'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/exp51/weights/best.pt',
            '--source',
            'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/temp',
            '--save-txt',
            '--name',
            'imgs-posture',
            '--augment',
            '--save-conf'
        ]
        # 執行 CMD 指令
        result = subprocess.run(cmd, capture_output=True, text=True)
        # 檢查執行結果
        if result.returncode == 0:
            delete_temp_files()
            print("命令成功執行")
            print("輸出結果:")
            print(result.stdout)

            predicted_image_folder = 'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/runs/detect/imgs-posture'  # 預測後的圖片資料夾路徑
            predicted_image_paths = sorted(glob.glob(os.path.join(predicted_image_folder, '*.jpg')))  # 取得所有預測後的圖片路徑
            video_path = os.path.join(r'C:\Users\ZongZhun\PycharmProjects\pythonProject\yolov7-main\runs\posture', 'output.mp4')  # 影片輸出路徑
            images_to_video(predicted_image_paths, video_path)  # 將圖片轉換為影片
            # delete_runs_files()
            return render_template("detectpp.html", video_path=video_path)

        else:
            print("命令執行失敗")
            print("錯誤訊息:")
            print(result.stderr)

@app.route('/uploadt', methods=['GET', 'POST'])
def upload_foldert():
    if request.method == 'POST':
        folder = request.files.getlist('folder')  # 取得上傳的檔案列表
        file_paths = []  # 儲存上傳檔案的路徑
        for file in folder:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
        cmd = [
            'python',
            'detect_cow_shed.py',
            '--weights',
            'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/exp42/weights/best.pt',
            '--source',
            'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/temp',
            '--save-txt',
            '--name',
            'imgs-track',
            '--augment',
            '--save-conf'
        ]
        # 執行 CMD 指令
        result = subprocess.run(cmd, capture_output=True, text=True)
        # 檢查執行結果
        if result.returncode == 0:
            delete_temp_files()
            print("命令成功執行")
            print("輸出結果:")
            print(result.stdout)
            # 將處理結果返回給使用者
            predicted_image_folder = 'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/runs/detect/imgs-track'  # 預測後的圖片資料夾路徑
            # predicted_image_paths = sorted(glob.glob(os.path.join(predicted_image_folder, '*.jpg')))  # 取得所有預測後的圖片路徑
            # video_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp4')  # 影片輸出路徑
            a = r'C:\Users\ZongZhun\PycharmProjects\pythonProject\yolov7-main\runs\tracking'
            tracking(predicted_image_folder, a)  # 將圖片轉換為影片
            # delete_runs_files()
            return render_template("detecttt.html")

        else:
            print("命令執行失敗")
            print("錯誤訊息:")
            print(result.stderr)

@app.route('/uploade', methods=['GET', 'POST'])
def upload_foldere():
    if request.method == 'POST':
        folder = request.files.getlist('folder')  # 取得上傳的檔案列表
        file_paths = []  # 儲存上傳檔案的路徑
        for file in folder:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
        cmd = [
            'python',
            'detect_cow_shed.py',
            '--weights',
            'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/exp25/weights/best.pt',
            '--source',
            'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/temp',
            '--save-txt',
            '--name',
            'imgs-eating',
            '--augment',
            '--save-conf'
        ]
        # 執行 CMD 指令
        result = subprocess.run(cmd, capture_output=True, text=True)
        # 檢查執行結果
        if result.returncode == 0:
            delete_temp_files()
            print("命令成功執行")
            print("輸出結果:")
            print(result.stdout)

            predicted_image_folder = 'C:/Users/ZongZhun/PycharmProjects/pythonProject/yolov7-main/runs/detect/imgs-eating'  # 預測後的圖片資料夾路徑
            predicted_image_paths = sorted(glob.glob(os.path.join(predicted_image_folder, '*.jpg')))  # 取得所有預測後的圖片路徑
            video_path = os.path.join(r'C:\Users\ZongZhun\PycharmProjects\pythonProject\yolov7-main\runs\eating', 'output.mp4')  # 影片輸出路徑
            images_to_video(predicted_image_paths, video_path)  # 將圖片轉換為影片
            # delete_runs_files()
            return render_template("detectee.html")

        else:
            print("命令執行失敗")
            print("錯誤訊息:")
            print(result.stderr)

def delete_temp_files():
    # 刪除 TEMP 目錄下的檔案
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    for file_name in file_list:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        os.remove(file_path)

def delete_runs_files():
    # 刪除 detect 目錄下的檔案
    file_list = os.listdir(app.config['RUNS_FOLDER'])
    for file_name in file_list:
        file_path = os.path.join(app.config['RUNS_FOLDER'], file_name)
        os.remove(file_path)




app.run(host="0.0.0.0", port=5000)
#ngrok http 5000

