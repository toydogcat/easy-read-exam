import os
import re
import glob

def enhance_content(content):
    # 1. Heading emojis (## 第一題 -> ## 📝 第一題)
    content = re.sub(r'^(##\s+)(?![📝⚙️🔍🛡️🔑🔹])(第[一二三四五六七八九十]+題：)', r'\1📝 \2', content, flags=re.MULTILINE)
    
    # 2. Subheading emojis (### (一) -> ### 🔹 (一))
    content = re.sub(r'^(###\s+)(?![📝⚙️🔍🛡️🔑🔹])(\([一二三四五六七八九十]+\))', r'\1🔹 \2', content, flags=re.MULTILINE)
    
    # 3. List item bold term enhancements with emojis
    replacements = {
        r'\*\*優點\*\*': '🟢 **優點**',
        r'\*\*缺點\*\*': '🔴 **缺點**',
        r'\*\*核心目標\*\*': '🎯 **核心目標**',
        r'\*\*安全重點\*\*': '🛡️ **安全重點**',
        r'\*\*定義\*\*': '📖 **定義**',
        r'\*\*解題關鍵\*\*': '🔑 **解題關鍵**',
        r'\*\*參考答案\*\*': '✅ **參考答案**',
        r'\*\*公式\*\*': '🧮 **公式**',
        r'\*\*注意\*\*': '⚠️ **注意**',
        r'\*\*說明\*\*': 'ℹ️ **說明**',
        r'\*\*步驟\*\*': '🐾 **步驟**',
        r'\*\*分析\*\*': '📊 **分析**',
        r'\*\*結論\*\*': '🏁 **結論**',
        r'\*\*特性\*\*': '⚙️ **特性**',
        r'\*\*優勢\*\*': '⚡ **優勢**',
        r'\*\*劣勢\*\*': '⚠️ **劣勢**',
        r'\*\*影響\*\*': '📈 **影響**',
        r'\*\*挑戰\*\*': '💥 **挑戰**',
        r'\*\*改善方式\*\*': '💡 **改善方式**',
        r'\*\*解決方案\*\*': '💡 **解決方案**',
        r'\*\*目標\*\*': '🎯 **目標**',
        r'\*\*原則\*\*': '📜 **原則**',
        r'\*\*核心概念\*\*': '🧠 **核心概念**',
    }
    
    for pattern, repl in replacements.items():
        # Only replace if not already prefixed by emoji
        # We search for the exact pattern and replace it
        content = re.sub(r'(?<![🟢🔴🎯🛡️📖🔑✅🧮⚠️ℹ️🐾📊🏁⚙️⚡📈💥💡📜🧠]\s)' + pattern, repl, content)
        
    return content

def main():
    base_dir = 'TMP/資訊處理考古題'
    pattern = os.path.join(base_dir, '**', '*.md')
    files = glob.glob(pattern, recursive=True)
    
    print(f"Found {len(files)} markdown files to enhance.")
    
    modified_count = 0
    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()
            
        enhanced = enhance_content(original)
        
        if enhanced != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(enhanced)
            modified_count += 1
            
    print(f"Successfully enhanced {modified_count} files.")

if __name__ == '__main__':
    main()
