import os
import pypandoc


def convert_md_to_rst(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.md'):
                md_file_path = os.path.join(root, file)
                rst_file_name = os.path.splitext(file)[0] + '.rst'
                rst_file_path = os.path.join(root, rst_file_name)
                try:
                    output = pypandoc.convert_file(md_file_path, 'rst')
                    with open(rst_file_path, 'w', encoding='utf-8') as rst_file:
                        rst_file.write(output)
                    print(f"已将 {md_file_path} 转换为 {rst_file_path}")
                except Exception as e:
                    print(f"转换 {md_file_path} 时出错: {e}")


if __name__ == "__main__":
    folder_path = '.'  # 当前文件夹
    convert_md_to_rst(folder_path)
    