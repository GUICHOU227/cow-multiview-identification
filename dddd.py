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
            'C:/Users/User/PycharmProjects/pythonProject/yolov7-main/exp51/weights/best.pt',
            '--source',
            'C:/Users/User/PycharmProjects/pythonProject/yolov7-main/temp',
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

            predicted_image_folder = 'C:/Users/User/PycharmProjects/pythonProject/yolov7-main/runs/detect/imgs-posture'  # 預測後的圖片資料夾路徑
            predicted_image_paths = sorted(glob.glob(os.path.join(predicted_image_folder, '*.jpg')))  # 取得所有預測後的圖片路徑
            video_path = os.path.join(r'C:\Users\User\PycharmProjects\pythonProject\yolov7-main\runs\posture', 'output.mp4')  # 影片輸出路徑
            images_to_video(predicted_image_paths, video_path)  # 將圖片轉換為影片
            # delete_runs_files()
            return render_template("detectpp.html", video_path=video_path)

        else:
            print("命令執行失敗")
            print("錯誤訊息:")
            print(result.stderr)