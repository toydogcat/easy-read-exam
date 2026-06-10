import React, { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ChevronRight, ChevronLeft, GraduationCap } from 'lucide-react';

interface Exam {
  year: string;
  subject: string;
  questions: { filename: string; content: string } | null;
  answers: { filename: string; content: string }[];
}

interface SubjectData {
  subject: string;
  exams: Exam[];
}

interface ExamViewerProps {
  data: SubjectData[];
}

const ExamViewer: React.FC<ExamViewerProps> = ({ data }) => {
  const [selectedSubjectIdx, setSelectedSubjectIdx] = useState(0);
  const [selectedExamIdx, setSelectedExamIdx] = useState(0);
  const [viewMode, setViewMode] = useState<'question' | 'answer'>('question');
  const [selectedAnswerIdx, setSelectedAnswerIdx] = useState(0);

  const currentSubject = data[selectedSubjectIdx];
  const currentExam = currentSubject.exams[selectedExamIdx];

  const handleSubjectChange = (idx: number) => {
    setSelectedSubjectIdx(idx);
    setSelectedExamIdx(0);
    setViewMode('question');
    setSelectedAnswerIdx(0);
  };

  const handleExamChange = (idx: number) => {
    setSelectedExamIdx(idx);
    setViewMode('question');
    setSelectedAnswerIdx(0);
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-50">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r border-slate-200 flex flex-col shrink-0">
        <div className="p-4 border-b border-slate-200">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <GraduationCap className="text-blue-600" />
            考古題閱覽
          </h1>
        </div>
        
        <div className="flex-1 overflow-y-auto p-2 space-y-4">
          <div>
            <p className="px-2 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">考科</p>
            <div className="space-y-1">
              {data.map((item, idx) => (
                <button
                  key={item.subject}
                  onClick={() => handleSubjectChange(idx)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                    selectedSubjectIdx === idx 
                      ? 'bg-blue-50 text-blue-700 font-medium' 
                      : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  {item.subject}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="px-2 mb-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">年份</p>
            <div className="space-y-1">
              {currentSubject.exams.map((exam, idx) => (
                <button
                  key={exam.year}
                  onClick={() => handleExamChange(idx)}
                  className={`w-full text-left px-3 py-2 rounded-md text-sm transition-colors ${
                    selectedExamIdx === idx 
                      ? 'bg-slate-200 text-slate-900 font-medium' 
                      : 'text-slate-600 hover:bg-slate-100'
                  }`}
                >
                  {exam.year} 年
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="h-14 bg-white border-b border-slate-200 flex items-center justify-between px-6 shrink-0">
          <div className="flex items-center gap-2 text-sm text-slate-600">
            <span>{currentSubject.subject}</span>
            <ChevronRight size={16} />
            <span className="font-medium text-slate-900">{currentExam.year} 年</span>
          </div>

          <div className="flex bg-slate-100 p-1 rounded-lg">
            <button
              onClick={() => setViewMode('question')}
              className={`px-4 py-1 rounded-md text-sm font-medium transition-all ${
                viewMode === 'question' ? 'bg-white shadow-sm text-blue-600' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              題目
            </button>
            <button
              onClick={() => setViewMode('answer')}
              className={`px-4 py-1 rounded-md text-sm font-medium transition-all ${
                viewMode === 'answer' ? 'bg-white shadow-sm text-blue-600' : 'text-slate-600 hover:text-slate-900'
              }`}
            >
              解答
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-8">
          <div className="max-w-4xl mx-auto bg-white shadow-sm rounded-xl border border-slate-200 p-8 min-h-full">
            {viewMode === 'question' ? (
              <div className="markdown-body">
                {currentExam.questions ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {currentExam.questions.content}
                  </ReactMarkdown>
                ) : (
                  <p className="text-slate-500 italic">暫無題目內容</p>
                )}
              </div>
            ) : (
              <div className="space-y-8">
                {currentExam.answers.length > 1 && (
                  <div className="flex gap-2 border-b border-slate-100 pb-4 overflow-x-auto">
                    {currentExam.answers.map((ans, idx) => (
                      <button
                        key={idx}
                        onClick={() => setSelectedAnswerIdx(idx)}
                        className={`px-3 py-1 text-xs rounded-full whitespace-nowrap ${
                          selectedAnswerIdx === idx 
                            ? 'bg-blue-600 text-white' 
                            : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                        }`}
                      >
                        {ans.filename.replace('.md', '')}
                      </button>
                    ))}
                  </div>
                )}
                <div className="markdown-body">
                  {currentExam.answers.length > 0 ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {currentExam.answers[selectedAnswerIdx].content}
                    </ReactMarkdown>
                  ) : (
                    <p className="text-slate-500 italic">暫無解答內容</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer Navigation */}
        <footer className="h-12 bg-white border-t border-slate-200 flex items-center justify-between px-6 shrink-0 text-sm">
          <button
            disabled={selectedExamIdx === currentSubject.exams.length - 1}
            onClick={() => handleExamChange(selectedExamIdx + 1)}
            className="flex items-center gap-1 text-slate-600 hover:text-blue-600 disabled:opacity-30 disabled:hover:text-slate-600"
          >
            <ChevronLeft size={16} /> 下一年份
          </button>
          <div className="text-slate-400">
            {selectedExamIdx + 1} / {currentSubject.exams.length}
          </div>
          <button
            disabled={selectedExamIdx === 0}
            onClick={() => handleExamChange(selectedExamIdx - 1)}
            className="flex items-center gap-1 text-slate-600 hover:text-blue-600 disabled:opacity-30 disabled:hover:text-slate-600"
          >
            前一年份 <ChevronRight size={16} />
          </button>
        </footer>
      </div>
    </div>
  );
};

export default ExamViewer;
