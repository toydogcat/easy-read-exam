import { useState, useEffect } from 'react';
import PasswordGate from './components/PasswordGate';
import ExamViewer from './components/ExamViewer';
import examData from './data/exams.json';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const auth = localStorage.getItem('exam_auth');
    if (auth === 'true') {
      setIsAuthenticated(true);
    }
  }, []);

  if (!isAuthenticated) {
    return <PasswordGate onSuccess={() => setIsAuthenticated(true)} />;
  }

  return <ExamViewer data={examData} />;
}

export default App;
