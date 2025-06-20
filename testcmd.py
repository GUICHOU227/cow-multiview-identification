import subprocess

# 定義 CMD 指令
cmd = [
    'python',
    'detect_cow_shed.py',
    '--weights',
    'C:/Users/User/PycharmProjects/pythonProject/yolov7-main/exp25/weights/best.pt',
    '--source',
    'C:/Users/User/PycharmProjects/pythonProject/yolov7-main/carrect_1635_30s',
    '--save-txt',
    '--name',
    'exp25_carrect_1635_30s',
    '--augment',
    '--save-conf'
]

# 執行 CMD 指令
result = subprocess.run(cmd, capture_output=True, text=True)

# 檢查執行結果
if result.returncode == 0:
    print("命令成功執行")
    print("輸出結果:")
    print(result.stdout)
else:
    print("命令執行失敗")
    print("錯誤訊息:")
    print(result.stderr)