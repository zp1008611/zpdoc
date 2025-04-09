import os


def remove_readme_rst(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file == 'README.rst':
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"已删除 {file_path}")
                except Exception as e:
                    print(f"删除 {file_path} 时出错: {e}")


if __name__ == "__main__":
    folder_path = '.'  # 当前文件夹
    remove_readme_rst(folder_path)
    