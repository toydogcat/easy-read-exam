import os
import re
import shutil
import fitz

def clean_pdf_text(doc):
    full_text = []
    for page_idx, page in enumerate(doc):
        text = page.get_text()
        lines = text.split('\n')
        cleaned_lines = []
        for l in lines:
            line_str = l.strip()
            # Remove repeated page markers
            if re.match(r'^代號：\d+(-\d+)?\s+頁次：\d+－\d+', line_str):
                continue
            cleaned_lines.append(l)
        full_text.append('\n'.join(cleaned_lines))
    return '\n\n'.join(full_text)

def parse_choice_answers(doc):
    answers = []
    for page in doc:
        tabs = page.find_tables()
        if tabs.tables:
            for t in tabs.tables:
                df = t.extract()
                for row_idx in range(0, len(df)-1, 2):
                    header_row = df[row_idx]
                    ans_row = df[row_idx+1]
                    for q, a in zip(header_row, ans_row):
                        q_str = str(q).strip() if q else ''
                        a_str = str(a).strip() if a else ''
                        if q_str.startswith('第') and '題' in q_str and a_str:
                            m = re.search(r'第(\d+)題', q_str)
                            if m:
                                answers.append((int(m.group(1)), a_str))
    answers.sort(key=lambda x: x[0])
    # deduplicate by question number
    seen = set()
    dedup = []
    for q, a in answers:
        if q not in seen:
            seen.add(q)
            dedup.append((q, a))
    return dedup

def format_answers_md(exam_title, answers):
    md = [f"# {exam_title} 參考解答\n\n---\n\n## 📋 測驗式試題標準答案\n"]
    md.append("| 題號 | 答案 | 題號 | 答案 | 題號 | 答案 | 題號 | 答案 | 題號 | 答案 |")
    md.append("| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |")
    
    rows = []
    curr = []
    for q_num, ans in answers:
        curr.append(f"**第 {q_num} 題** | `{ans}`")
        if len(curr) == 5:
            rows.append("| " + " | ".join(curr) + " |")
            curr = []
    if curr:
        while len(curr) < 5:
            curr.append(" - | - ")
        rows.append("| " + " | ".join(curr) + " |")
    md.extend(rows)
    md.append("\n")
    return '\n'.join(md)

def process_senior_3():
    base = 'TMP/三等考試/三等考試'
    target_base = 'TMP/高考三等'
    os.makedirs(target_base, exist_ok=True)
    
    years = sorted(os.listdir(base))
    for y in years:
        ypath = os.path.join(base, y)
        if not os.path.isdir(ypath): continue
        
        # Keep track of answer pdfs
        ans_files = {}
        q_files = {}
        
        for f in sorted(os.listdir(ypath)):
            if not f.endswith('.pdf'): continue
            is_ans = '答案' in f
            sub = None
            if '國文' in f: sub = '國文'
            elif '英文' in f: sub = '法學知識與英文'
            elif '資料庫' in f: sub = '資料庫應用'
            elif '資料結構' in f: sub = '資料結構'
            elif '資訊管理' in f or ('資訊網路與安全' in f and int(y) <= 110): sub = '資訊管理'
            elif '資通網路' in f or ('資訊網路與安全' in f and int(y) >= 111): sub = '資通網路與安全'
            
            if not sub: continue
            
            if is_ans:
                ans_files[sub] = os.path.join(ypath, f)
            else:
                q_files[sub] = os.path.join(ypath, f)
        
        for sub, q_pdf in q_files.items():
            sub_dir = os.path.join(target_base, sub)
            os.makedirs(sub_dir, exist_ok=True)
            
            # Destination file names
            dest_pdf = os.path.join(sub_dir, f"{y}{sub}.pdf")
            dest_md = os.path.join(sub_dir, f"{y}{sub}.md")
            dest_ans = os.path.join(sub_dir, f"{y}{sub}_解答.md")
            
            shutil.copy2(q_pdf, dest_pdf)
            
            # Extract question text
            doc = fitz.open(q_pdf)
            q_text = clean_pdf_text(doc)
            with open(dest_md, 'w', encoding='utf-8') as f_out:
                f_out.write(q_text)
            
            # If there's an official answer file, extract choice answers
            if sub in ans_files:
                ans_doc = fitz.open(ans_files[sub])
                answers = parse_choice_answers(ans_doc)
                if answers:
                    exam_title = f"{y}年公務人員高等考試三級考試 - {sub}"
                    ans_md = format_answers_md(exam_title, answers)
                    with open(dest_ans, 'w', encoding='utf-8') as f_out:
                        f_out.write(ans_md)
                    print(f"  [高考三等] {y} {sub}: extracted {len(answers)} choice answers")

def process_local_3():
    base = 'TMP/三等考試/地方特考'
    target_base = 'TMP/地方特考三等'
    os.makedirs(target_base, exist_ok=True)
    
    years = sorted(os.listdir(base))
    for y in years:
        ypath = os.path.join(base, y)
        if not os.path.isdir(ypath): continue
        
        for f in sorted(os.listdir(ypath)):
            if not f.endswith('.pdf'): continue
            sub = None
            if '國文' in f: sub = '國文'
            elif '法學知識' in f: sub = '法學知識與英文'
            elif '資料庫' in f: sub = '資料庫應用'
            elif '資料結構' in f: sub = '資料結構'
            elif '資訊管理' in f or '資通管理' in f: sub = '資訊管理'
            elif '資通網路' in f: sub = '資通網路與安全'
            
            if not sub: continue
            
            sub_dir = os.path.join(target_base, sub)
            os.makedirs(sub_dir, exist_ok=True)
            
            dest_pdf = os.path.join(sub_dir, f"{y}{sub}.pdf")
            dest_md = os.path.join(sub_dir, f"{y}{sub}.md")
            
            shutil.copy2(os.path.join(ypath, f), dest_pdf)
            
            doc = fitz.open(os.path.join(ypath, f))
            q_text = clean_pdf_text(doc)
            with open(dest_md, 'w', encoding='utf-8') as f_out:
                f_out.write(q_text)

process_senior_3()
process_local_3()
print("Batch conversion completed successfully!")
