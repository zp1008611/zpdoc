import re  

# 读取文件  
with open('README.md', 'r', encoding='utf-8') as file:  
    content = file.read()  

# 正则表达式匹配特定格式的 <div> 标签  
pattern = r'<div\s+style="text-align:\s*center;">\s*<img\s+src="(.*?)"\s+alt="(.*?)"\s+style="width:\d+%;\s*height:auto;">\s*</div>'  
replacement = r'![\2](\1)'  

# 替换内容  
new_content = re.sub(pattern, replacement, content, flags=re.S)  

# 写入新的内容到文件  
with open('README.md', 'w', encoding='utf-8') as file:  
    file.write(new_content)  

print("替换完成！")  