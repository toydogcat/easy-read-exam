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

import { ChevronRight, ChevronLeft, GraduationCap, Menu, X } from 'lucide-react';

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
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const currentSubject = data[selectedSubjectIdx];
  const currentExam = currentSubject.exams[selectedExamIdx];

  const handleSubjectChange = (idx: number) => {
    setSelectedSubjectIdx(idx);
    setSelectedExamIdx(0);
    setViewMode('question');
    setSelectedAnswerIdx(0);
    setIsSidebarOpen(false); // Close sidebar on mobile
  };

  const handleExamChange = (idx: number) => {
    setSelectedExamIdx(idx);
    setViewMode('question');
    setSelectedAnswerIdx(0);
    setIsSidebarOpen(false); // Close sidebar on mobile
  };

  return (
    <div className="flex h-screen overflow-hidden bg-slate-950 text-slate-100 relative">
      {/* Sidebar Overlay (Mobile Only) */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 bg-black/60 z-40 md:hidden"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 w-72 bg-slate-900 border-r border-slate-800 flex flex-col z-50 transition-transform duration-300 transform
        md:relative md:translate-x-0 md:w-64
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="p-4 border-b border-slate-800 flex items-center justify-between">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <GraduationCap className="text-blue-400" />
            考古題閱覽
          </h1>
          <button 
            className="md:hidden p-2 text-slate-400"
            onClick={() => setIsSidebarOpen(false)}
          >
            <X size={24} />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto p-3 space-y-6">
          <div>
            <p className="px-2 mb-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">考科</p>
            <div className="space-y-1">
              {data.map((item, idx) => (
                <button
                  key={item.subject}
                  onClick={() => handleSubjectChange(idx)}
                  className={`w-full text-left px-3 py-2.5 rounded-lg text-sm transition-colors ${
                    selectedSubjectIdx === idx 
                      ? 'bg-blue-900/40 text-blue-400 font-medium' 
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
                  }`}
                >
                  {item.subject}
                </button>
              ))}
            </div>
          </div>

          <div>
            <p className="px-2 mb-3 text-xs font-semibold text-slate-500 uppercase tracking-wider">年份</p>
            <div className="grid grid-cols-2 gap-1 px-1">
              {currentSubject.exams.map((exam, idx) => (
                <button
                  key={exam.year}
                  onClick={() => handleExamChange(idx)}
                  className={`text-center px-2 py-2.5 rounded-lg text-sm transition-colors ${
                    selectedExamIdx === idx 
                      ? 'bg-slate-800 text-slate-100 font-medium' 
                      : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-transparent'
                  }`}
                >
                  {exam.year}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col min-w-0 bg-slate-950">
        <header className="h-16 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-4 md:px-6 shrink-0 z-30">
          <div className="flex items-center gap-3 min-w-0">
            <button 
              className="md:hidden p-2 -ml-2 text-slate-400 hover:text-slate-200"
              onClick={() => setIsSidebarOpen(true)}
            >
              <Menu size={24} />
            </button>
            <div className="flex items-center gap-1 text-sm text-slate-400 truncate">
              <span className="hidden sm:inline">{currentSubject.subject}</span>
              <ChevronRight size={14} className="hidden sm:inline shrink-0" />
              <span className="font-medium text-slate-200 truncate">{currentExam.year} 年</span>
            </div>
          </div>

          <div className="flex bg-slate-800 p-1 rounded-xl">
            <button
              onClick={() => setViewMode('question')}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                viewMode === 'question' ? 'bg-slate-700 shadow-lg text-blue-400' : 'text-slate-400'
              }`}
            >
              題目
            </button>
            <button
              onClick={() => setViewMode('answer')}
              className={`px-4 py-1.5 rounded-lg text-sm font-medium transition-all ${
                viewMode === 'answer' ? 'bg-slate-700 shadow-lg text-blue-400' : 'text-slate-400'
              }`}
            >
              解答
            </button>
          </div>
        </header>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto p-4 md:p-8">
          <div className="max-w-4xl mx-auto bg-slate-900 shadow-2xl rounded-2xl border border-slate-800 p-5 md:p-10 min-h-full">
            {viewMode === 'question' ? (
              <div className="markdown-body text-base md:text-lg">
                {currentExam.questions ? (
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {currentExam.questions.content}
                  </ReactMarkdown>
                ) : (
                  <p className="text-slate-500 italic text-center py-20">暫無題目內容</p>
                )}
              </div>
            ) : (
              <div className="space-y-6">
                {currentExam.answers.length > 1 && (
                  <div className="flex gap-2 border-b border-slate-800 pb-4 overflow-x-auto no-scrollbar">
                    {currentExam.answers.map((ans, idx) => (
                      <button
                        key={idx}
                        onClick={() => setSelectedAnswerIdx(idx)}
                        className={`px-4 py-2 text-xs font-medium rounded-full whitespace-nowrap transition-colors ${
                          selectedAnswerIdx === idx 
                            ? 'bg-blue-600 text-white shadow-lg shadow-blue-900/40' 
                            : 'bg-slate-800 text-slate-400 hover:bg-slate-700'
                        }`}
                      >
                        {ans.filename.replace('.md', '')}
                      </button>
                    ))}
                  </div>
                )}
                <div className="markdown-body text-base md:text-lg">
                  {currentExam.answers.length > 0 ? (
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                      {currentExam.answers[selectedAnswerIdx].content}
                    </ReactMarkdown>
                  ) : (
                    <p className="text-slate-500 italic text-center py-20">暫無解答內容</p>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Footer Navigation */}
        <footer className="h-16 bg-slate-900 border-t border-slate-800 flex items-center justify-between px-6 shrink-0 text-sm z-30">
          <button
            disabled={selectedExamIdx === currentSubject.exams.length - 1}
            onClick={() => handleExamChange(selectedExamIdx + 1)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-slate-400 hover:text-blue-400 hover:bg-slate-800 active:bg-slate-700 disabled:opacity-10 disabled:cursor-not-allowed transition-all"
          >
            <ChevronLeft size={20} /> <span className="hidden sm:inline">下一年份</span>
          </button>
          <div className="text-slate-600 font-mono font-medium tracking-tighter">
            {selectedExamIdx + 1} / {currentSubject.exams.length}
          </div>
          <button
            disabled={selectedExamIdx === 0}
            onClick={() => handleExamChange(selectedExamIdx - 1)}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg text-slate-400 hover:text-blue-400 hover:bg-slate-800 active:bg-slate-700 disabled:opacity-10 disabled:cursor-not-allowed transition-all"
          >
            <span className="hidden sm:inline">前一年份</span> <ChevronRight size={20} />
          </button>
        </footer>
      </div>
    </div>
  );
};

export default ExamViewer;
