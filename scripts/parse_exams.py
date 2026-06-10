import os
import json
import re

def parse_exams(base_dir):
    data = []
    
    # Get subjects (subdirectories)
    subjects = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]
    
    for subject_name in subjects:
        subject_path = os.path.join(base_dir, subject_name)
        exams_by_year = {}
        
        for filename in os.listdir(subject_path):
            if not filename.endswith('.md'):
                continue
                
            # Extract year - usually at the beginning
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
                # Assuming the one without "answer" indicators is the question file
                # If there are multiple, the last one wins (could be refined)
                exams_by_year[year]["questions"] = {
                    "filename": filename,
                    "content": content
                }
        
        # Sort exams by year
        sorted_exams = sorted(exams_by_year.values(), key=lambda x: int(x["year"]), reverse=True)
        
        data.append({
            "subject": subject_name,
            "exams": sorted_exams
        })
        
    return data

if __name__ == "__main__":
    base_dir = "TMP/資訊處理考古題"
    output_dir = "src/data"
    os.makedirs(output_dir, exist_ok=True)
    
    exam_data = parse_exams(base_dir)
    
    with open(os.path.join(output_dir, "exams.json"), "w", encoding="utf-8") as f:
        json.dump(exam_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully parsed {len(exam_data)} subjects and saved to {output_dir}/exams.json")
