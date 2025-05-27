import os
import glob
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# 根目錄，裡面有各子資料夾
root_dir = '/Users/quma/Downloads/data'

# 要處理的子資料夾清單
subdirs = [
    '515', '523', '526',
    'reversi_05-18--23-26',
    'reversi_05-25--19-25',
    'reversi_05-27--15-18'
]

# 對應 subdirs 的「標題用日期」（mm/dd 格式）
title_dates = [
    '05/15',
    '05/23', '05/26',
    '05/18', '05/25', '05/27'
]

# x 軸刻度顯示成 1k、1M
def human_format(x, pos):
    if x >= 1e6:
        return f'{x/1e6:.1f}M'
    elif x >= 1e3:
        return f'{x/1e3:.0f}k'
    else:
        return str(int(x))

for sub, title_date in zip(subdirs, title_dates):
    dir_path = os.path.join(root_dir, sub)
    if not os.path.isdir(dir_path):
        print(f"跳過不存在的資料夾：{dir_path}")
        continue

    # 在子資料夾下建立 fig/ 資料夾
    fig_dir = os.path.join(dir_path, 'fig')
    os.makedirs(fig_dir, exist_ok=True)

    # 檔名用的日期（把 '/' 換成 '-'）
    filename_date = title_date.replace('/', '-')

    # 逐一處理該資料夾底下所有 .csv
    for csv_path in glob.glob(os.path.join(dir_path, '*.csv')):
        # 取出不含副檔名的檔名
        fname = os.path.splitext(os.path.basename(csv_path))[0]

        # 讀取 CSV（欄位：Wall time, Step, Value）
        df = pd.read_csv(csv_path)

        # 繪圖
        plt.figure(figsize=(10, 6))
        plt.plot(df['Step'], df['Value'], linewidth=0.8)

        # 標題：在原檔名之前加上 mm/dd
        plt.title(f"{title_date}  {fname}")

        plt.xlabel('Step')
        plt.ylabel('Value')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(human_format))
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.tight_layout()

        # 儲存檔名：mm-dd_原檔名.png
        out_name = f"{filename_date}_{fname}.png"
        out_path = os.path.join(fig_dir, out_name)
        plt.savefig(out_path)
        plt.close()

        print(f"已儲存：{out_path}")
