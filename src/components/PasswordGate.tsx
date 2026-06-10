import React, { useState } from 'react';

interface PasswordGateProps {
  onSuccess: () => void;
}

const PasswordGate: React.FC<PasswordGateProps> = ({ onSuccess }) => {
  const [password, setPassword] = useState('');
  const [error, setError] = useState(false);

  // SHA-256 hash of "12345678987654321"
  const TARGET_HASH = 'f384c0e4f88dc9ea55c92ba016cb43b0d821e76c6676ada2d0de5e392976b30d';

  const hashPassword = async (str: string) => {
    const encoder = new TextEncoder();
    const data = encoder.encode(str);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const hashed = await hashPassword(password);
    if (hashed === TARGET_HASH) {
      onSuccess();
      localStorage.setItem('exam_auth', 'true');
    } else {
      setError(true);
      setPassword('');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 px-4">
      <div className="max-w-md w-full bg-slate-900 border border-slate-800 rounded-xl shadow-2xl p-8">
        <h1 className="text-2xl font-bold text-center mb-6 text-slate-100">請輸入密碼以繼續</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <input
              type="password"
              value={password}
              onChange={(e) => {
                setPassword(e.target.value);
                setError(false);
              }}
              placeholder="密碼"
              className={`w-full px-4 py-2 bg-slate-800 border rounded-lg text-slate-100 focus:outline-none focus:ring-2 ${
                error ? 'border-red-500 focus:ring-red-900/50' : 'border-slate-700 focus:ring-blue-500/50'
              }`}
              autoFocus
            />
            {error && <p className="text-red-400 text-sm mt-1">密碼錯誤，請再試一次。</p>}
          </div>
          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-2 rounded-lg transition-colors shadow-lg shadow-blue-900/20"
          >
            進入閱覽
          </button>
        </form>
      </div>
    </div>
  );
};

export default PasswordGate;
