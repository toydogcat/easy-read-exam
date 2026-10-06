import os
import re

PUA_MAP = {
    '\ue129': '(一)', '\ue12a': '(二)', '\ue12b': '(三)', '\ue12c': '(四)', '\ue12d': '(五)',
    '\ue12e': '(六)', '\ue12f': '(七)', '\ue130': '(八)',
    '\ue18c': '(A)', '\ue18d': '(B)', '\ue18e': '(C)', '\ue18f': '(D)',
    '\ue0c6': '1.', '\ue0c7': '2.', '\ue0c8': '3.', '\ue0c9': '4.', '\ue0ca': '5.',
    '\ue0cb': '6.', '\ue0cc': '7.', '\ue0cd': '8.', '\ue0ce': '9.', '\ue0cf': '10.',
    '\ue1a6': '(1)', '\ue1a7': '(2)', '\ue1a8': '(3)', '\ue1a9': '(4)',
    '\ue1be': '(1)', '\ue1bf': '(2)', '\ue1c0': '(3)', '\ue1c1': '(4)',
    '\ue063': '(1)', '\ue064': '(2)', '\ue065': '(3)', '\ue066': '(4)', '\ue067': '(5)',
    '\uf0ae': ' → ', '\uf0da': ' → ', '\uf02d': '-', '\uf03d': '=', '\uf02b': '+',
    '\uf0b4': ' × ', '\uf0a3': ' ≤ ', '\uf051': 'Θ', '\uf020': ' ',
    '\uf09f': '• ', '\uf06c': '• ', '\uf077': 'ω', '\uf0ce': '∈', '\uf0b9': '≠',
    '\uf0a5': '∞', '\uf0d7': '×', '\uf6ea': ' ',
    '': '(一)', '': '(二)', '': '(三)', '': '(四)', '': '(五)',
    '': '1.', '': '2.', '': '3.', '': '4.', '': '5.',
    '': '6.', '': '7.', '': '8.', '': '9.', '': '10.',
    '': '(1)', '': '(2)', '': '(3)', '': '(4)', '': '(5)',
    '': '(A)', '': '(B)', '': '(C)', '': '(D)',
    '': '(一)', '': '(二)', '': '(三)', '': '(四)', '': '(五)', '': '(六)'
}

def replace_pua(text):
    for k, v in PUA_MAP.items():
        text = text.replace(k, v)
    return text

def clean_lines(text):
    lines = text.split('\n')
    cleaned = []
    for l in lines:
        s = l.strip()
        # Filter noise
        if re.match(r'^(代號：\d+|頁次：\d+[-－]\d+|座號：|公職王歷屆試題|共\d+頁|全國最大公教職|.*老師解題)', s):
            continue
        if re.match(r'^(等\s*別：|類\s*科：|科\s*目：|考試時間：|考試別：|※注意：|不必抄題|本科目除|請以黑色鋼筆)', s):
            continue
        cleaned.append(l)
    return '\n'.join(cleaned)

def split_and_clean_113_local():
    subjects = ['資料結構', '資料庫應用', '資訊管理', '資通網路與安全']
    for sub in subjects:
        file_path = f'TMP/地方特考三等/{sub}/113{sub}.md'
        ans_path = f'TMP/地方特考三等/{sub}/113{sub}_解答.md'
        if not os.path.exists(file_path):
            continue
        with open(file_path, 'r', encoding='utf-8') as f:
            raw = f.read()
        
        raw = replace_pua(raw)
        
        chunks = re.split(r'\n(?=[一二三四五]、)', raw)
        q_sections = []
        a_sections = []
        
        for c in chunks[1:]:
            c_clean = clean_lines(c).strip()
            m = re.search(r'【(解題關鍵|擬答)】', c_clean)
            if m:
                q_part = c_clean[:m.start()].strip()
                a_part = c_clean[m.start():].strip()
                
                # Format question heading as ##
                q_part = re.sub(r'^([一二三四五]、)', r'## \1', q_part)
                q_sections.append(q_part)
                
                # Format answer heading as ##
                head_match = re.match(r'^([一二三四五]、[^\n]+)', c_clean)
                header_title = head_match.group(1) if head_match else f"第 {len(a_sections)+1} 題"
                # Strip question title in answer and format
                a_formatted = f"## 📝 {header_title}\n\n" + a_part
                a_sections.append(a_formatted)
            else:
                q_sections.append(c_clean)
        
        # Save Question File
        q_output = [
            f"# 113年 特種考試地方政府公務人員考試\n",
            f"**等別**：三等考試  ",
            f"**類科**：資訊處理  ",
            f"**科目**：{sub}  ",
            f"**考試時間**：2 小時  \n",
            f"---\n"
        ]
        q_output.extend(q_sections)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(q_output))
            
        # Save Answer File
        a_output = [
            f"# 113年 特種考試地方政府公務人員考試（三等考試）\n",
            f"**類科**：資訊處理  ",
            f"**科目**：{sub}  \n",
            f"---\n"
        ]
        a_output.extend(a_sections)
        with open(ans_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(a_output))
            
        print(f"Successfully processed 113 {sub}: Question ({len(q_sections)} items), Answer ({len(a_sections)} items).")

def clean_all_general_questions():
    dirs = ['TMP/高考三等', 'TMP/地方特考三等']
    for b in dirs:
        track_name = "公務人員高等考試三級考試" if "高考" in b else "特種考試地方政府公務人員考試"
        for root, _, files in os.walk(b):
            for f in sorted(files):
                if not f.endswith('.md') or '_解答' in f or '重點整理' in f:
                    continue
                
                # Skip 113 if already handled
                m_year = re.match(r'^(\d+)(.+)\.md$', f)
                if not m_year:
                    continue
                year, sub = m_year.groups()
                if "地方特考" in b and year == "113" and sub in ['資料結構', '資料庫應用', '資訊管理', '資通網路與安全']:
                    continue
                
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                
                content = replace_pua(content)
                cleaned = clean_lines(content)
                
                # Normalize headings
                # Turn 一、, 二、, etc. into ## 一、
                cleaned = re.sub(r'(?m)^([一二三四五六七八九十]、)', r'## \1', cleaned)
                # Turn (一), (二), etc. into ### (一)
                cleaned = re.sub(r'(?m)^(\([一二三四五六七八九十]+\))', r'### \1', cleaned)
                
                header = [
                    f"# {year}年 {track_name}\n",
                    f"**等別**：三等考試  ",
                    f"**類科**：資訊處理  ",
                    f"**科目**：{sub}  ",
                    f"**考試時間**：2 小時  \n",
                    f"---\n"
                ]
                
                final_content = '\n'.join(header) + '\n' + cleaned.strip() + '\n'
                with open(path, 'w', encoding='utf-8') as fp:
                    fp.write(final_content)
                # print(f"Cleaned {b}/{sub}/{f}")

if __name__ == '__main__':
    split_and_clean_113_local()
    clean_all_general_questions()
    print("All question formatting and 113 splitting completed!")
