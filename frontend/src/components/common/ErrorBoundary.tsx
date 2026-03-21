import { Component, ReactNode } from 'react';

interface Props { children: ReactNode; fallback?: ReactNode; }
interface State { hasError: boolean; error: Error | null; }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="min-h-screen bg-gray-900 flex items-center justify-center p-4">
          <div className="bg-gray-800 rounded-lg p-8 max-w-lg text-center">
            <h2 className="text-xl font-bold text-white mb-4">Bir hata olustu</h2>
            <p className="text-gray-400 mb-6">{this.state.error?.message}</p>
            <button onClick={() => window.location.reload()} className="px-4 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700">
              Sayfayi Yenile
            </button>
          </div>
        </div>
      );
    }
    return this.props.children;
  }
}
