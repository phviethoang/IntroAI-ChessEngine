import csv

import matplotlib.pyplot as plt
import os
import pandas as pd


def plot_performance(move_times, move_counts, save_path='performance_charts'):
    # Kiểm tra và tạo thư mục nếu chưa tồn tại
    if not os.path.exists(save_path):
        os.makedirs(save_path)  # Tạo thư mục lưu trữ nếu chưa có

    # Tạo DataFrame từ dữ liệu
    df = pd.DataFrame({'row1': move_times})

    # Ghi DataFrame vào file CSV
    df.to_csv(os.path.join(save_path, 'your_file.csv'), index=False)

    # Vẽ biểu đồ thời gian xử lý
    plt.figure(figsize=(10, 5))
    plt.plot(move_times, label='Thời gian xử lý (ms)')
    plt.title('Thời Gian Xử Lý Cho Mỗi Nước Đi')
    plt.xlabel('Nước đi')
    plt.ylabel('Thời gian (ms)')
    plt.legend()
    plt.savefig(os.path.join(save_path, 'move_times.png'))  # Lưu biểu đồ
    plt.show()

    # Vẽ biểu đồ số lượng nước đi được xem xét
    plt.figure(figsize=(10, 5))
    plt.plot(move_counts, label='Số lượng nước đi')
    plt.title('Số Lượng Nước Đi Được Xem Xét Cho Mỗi Nước Đi')
    plt.xlabel('Nước đi')
    plt.ylabel('Số lượng nước đi')
    plt.legend()
    plt.savefig(os.path.join(save_path, 'move_counts.png'))  # Lưu biểu đồ
    plt.show()

    # Ghi dữ liệu vào file CSV
    with open(os.path.join(save_path, 'data.csv'), 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Thời gian xử lý', 'Số lượng nước đi'])
        for time, count in zip(move_times, move_counts):
            writer.writerow([time, count])





