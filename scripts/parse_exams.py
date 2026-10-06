import os
import json
import re

PREFERRED_ORDERS = {
    'senior-2': [
        '高等資料庫設計',
        '系統分析與設計研究',
        '軟體專案管理研究',
        '資訊管理與資通安全研究',
        '憲法與英文',
        '國文（作文、公文與測驗）'
    ],
    'senior-3': [
        '資料結構',
        '資料庫應用',
        '資訊管理',
        '資通網路與安全',
        '國文',
        '法學知識與英文'
    ],
    'local-3': [
        '資料結構',
        '資料庫應用',
        '資訊管理',
        '資通網路與安全',
        '國文',
        '法學知識與英文'
    ]
}

def parse_subject_dir(subject_path, subject_name):
    exams_by_year = {}
    
    for filename in sorted(os.listdir(subject_path)):
        if not filename.endswith('.md'):
            continue
        if filename == "重點整理.md":
            continue
            
        match = re.match(r'^(\d+)', filename)
        if not match:
            continue
        
        year = match.group(1)
        if year not in exams_by_year:
            exams_by_year[year] = {
                "year": year,
                "subject": subject_name,
                "questions": None,
                "answers": []
            }
        
        file_path = os.path.join(subject_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        is_answer = False
        if '_解答' in filename or '(答案)' in filename or '_答案' in filename:
            is_answer = True
        
        if is_answer:
            exams_by_year[year]["answers"].append({
                "filename": filename,
                "content": content
            })
        else:
            exams_by_year[year]["questions"] = {
                "filename": filename,
                "content": content
            }
    
    # Check for summary file
    summary_data = None
    summary_path = os.path.join(subject_path, "重點整理.md")
    if os.path.exists(summary_path):
        with open(summary_path, 'r', encoding='utf-8') as f:
            summary_content = f.read()
        summary_data = {
            "filename": "重點整理.md",
            "content": summary_content
        }

    # Sort exams by year (descending)
    sorted_exams = sorted(exams_by_year.values(), key=lambda x: int(x["year"]), reverse=True)
    return {
        "subject": subject_name,
        "summary": summary_data,
        "exams": sorted_exams
    }

def parse_track(track_info):
    base_dir = track_info['dir']
    track_id = track_info['id']
    track_name = track_info['name']
    
    if not os.path.exists(base_dir):
        print(f"Warning: directory {base_dir} does not exist.")
        return None
        
    subjects_dirs = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    # Sort subjects by preferred order
    order = PREFERRED_ORDERS.get(track_id, [])
    def subject_sort_key(s):
        if s in order:
            return order.index(s)
        return 999
        
    subjects_dirs.sort(key=subject_sort_key)
    
    subject_list = []
    for s_name in subjects_dirs:
        s_path = os.path.join(base_dir, s_name)
        subject_data = parse_subject_dir(s_path, s_name)
        subject_list.append(subject_data)
        
    return {
        "id": track_id,
        "name": track_name,
        "subjects": subject_list
    }

if __name__ == "__main__":
    tracks_config = [
        {
            "id": "senior-2",
            "name": "高考二級",
            "dir": "TMP/資訊處理考古題"
        },
        {
            "id": "senior-3",
            "name": "高考三等",
            "dir": "TMP/高考三等"
        },
        {
            "id": "local-3",
            "name": "地方特考三等",
            "dir": "TMP/地方特考三等"
        }
    ]
    
    output_dir = "src/data"
    os.makedirs(output_dir, exist_ok=True)
    
    all_tracks = []
    for t_cfg in tracks_config:
        track_data = parse_track(t_cfg)
        if track_data:
            all_tracks.append(track_data)
            total_exams = sum(len(s['exams']) for s in track_data['subjects'])
            total_answers = sum(sum(len(e['answers']) for e in s['exams']) for s in track_data['subjects'])
            print(f"[{track_data['name']}] parsed {len(track_data['subjects'])} subjects, {total_exams} exam years, {total_answers} answers.")
    
    output_path = os.path.join(output_dir, "exams.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_tracks, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(all_tracks)} tracks to {output_path}")
