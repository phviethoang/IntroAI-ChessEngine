import matplotlib.pyplot as plt
import os

def plot_performance(move_times, move_counts, save_path='performance_charts'):
    # Tạo thư mục lưu biểu đồ nếu chưa tồn tại
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Vẽ biểu đồ thời gian xử lý
    plt.figure(figsize=(10, 5))
    plt.plot(move_times, label='Thời gian xử lý (s)')
    plt.title('Thời Gian Xử Lý Cho Mỗi Nước Đi')
    plt.xlabel('Nước đi')
    plt.ylabel('Thời gian (s)')
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



