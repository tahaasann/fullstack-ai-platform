import { useState, useEffect } from 'react';
import { HiOutlinePlus, HiOutlinePencil, HiOutlineTrash, HiOutlineDownload, HiOutlineX } from 'react-icons/hi';

const STORAGE_KEY = 'devmaster_job_tracker';

interface JobApplication {
  id: string;
  company: string;
  position: string;
  status: 'research' | 'applied' | 'interview' | 'offer' | 'rejected';
  dateApplied: string;
  cvVersion: string;
  notes: string;
  followUpDate: string;
  link: string;
  createdAt: string;
}

const COLUMNS: { key: JobApplication['status']; label: string; color: string }[] = [
  { key: 'research', label: 'Araştırma', color: 'border-gray-500/30' },
  { key: 'applied', label: 'Başvuruldu', color: 'border-blue-500/30' },
  { key: 'interview', label: 'Mülakat', color: 'border-yellow-500/30' },
  { key: 'offer', label: 'Teklif', color: 'border-green-500/30' },
  { key: 'rejected', label: 'Red', color: 'border-red-500/30' },
];

function loadJobs(): JobApplication[] {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
  } catch { return []; }
}

function saveJobs(jobs: JobApplication[]) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(jobs));
}

export default function JobTrackerPage() {
  const [jobs, setJobs] = useState<JobApplication[]>(loadJobs);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingJob, setEditingJob] = useState<JobApplication | null>(null);

  useEffect(() => { saveJobs(jobs); }, [jobs]);

  const addJob = (job: Omit<JobApplication, 'id' | 'createdAt'>) => {
    setJobs([...jobs, { ...job, id: crypto.randomUUID(), createdAt: new Date().toISOString() }]);
  };

  const updateJob = (id: string, data: Partial<JobApplication>) => {
    setJobs(jobs.map((j) => (j.id === id ? { ...j, ...data } : j)));
  };

  const deleteJob = (id: string) => {
    setJobs(jobs.filter((j) => j.id !== id));
  };

  const exportJSON = () => {
    const blob = new Blob([JSON.stringify(jobs, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'job-applications.json';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Stats
  const total = jobs.length;
  const applied = jobs.filter((j) => j.status !== 'research').length;
  const interviews = jobs.filter((j) => j.status === 'interview').length;
  const offers = jobs.filter((j) => j.status === 'offer').length;
  const responseRate = applied > 0 ? Math.round(((interviews + offers) / applied) * 100) : 0;

  return (
    <div className="max-w-full mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">İş Başvuru Takibi</h1>
          <p className="text-gray-400 text-sm mt-1">Başvurularını takip et, süreci yönet</p>
        </div>
        <div className="flex items-center gap-2">
          <button
            onClick={exportJSON}
            className="flex items-center gap-1 px-3 py-2 bg-gray-800 hover:bg-gray-700 text-gray-300 rounded-lg text-sm transition-colors"
          >
            <HiOutlineDownload className="w-4 h-4" /> JSON İndir
          </button>
          <button
            onClick={() => { setEditingJob(null); setModalOpen(true); }}
            className="flex items-center gap-1 px-3 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm transition-colors"
          >
            <HiOutlinePlus className="w-4 h-4" /> Yeni Başvuru
          </button>
        </div>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        <StatBox label="Toplam" value={total} color="text-white" />
        <StatBox label="Başvuruldu" value={applied} color="text-blue-400" />
        <StatBox label="Mülakat" value={interviews} color="text-yellow-400" />
        <StatBox label="Yanıt Oranı" value={`%${responseRate}`} color="text-green-400" />
      </div>

      {/* Kanban */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
        {COLUMNS.map((col) => {
          const colJobs = jobs.filter((j) => j.status === col.key);
          return (
            <div key={col.key} className={`bg-gray-900/50 border ${col.color} rounded-xl p-3 min-h-[200px]`}>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-sm font-semibold text-gray-400">{col.label}</h3>
                <span className="text-xs text-gray-600">{colJobs.length}</span>
              </div>
              <div className="space-y-2">
                {colJobs.map((job) => (
                  <div key={job.id} className="bg-gray-900 border border-gray-800 rounded-lg p-3 group">
                    <div className="flex items-start justify-between">
                      <div className="min-w-0 flex-1">
                        <p className="text-sm font-medium text-white truncate">{job.company}</p>
                        <p className="text-xs text-gray-400 truncate">{job.position}</p>
                      </div>
                      <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onClick={() => { setEditingJob(job); setModalOpen(true); }} className="text-gray-400 hover:text-white p-0.5">
                          <HiOutlinePencil className="w-3.5 h-3.5" />
                        </button>
                        <button onClick={() => deleteJob(job.id)} className="text-gray-400 hover:text-red-400 p-0.5">
                          <HiOutlineTrash className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                    {job.dateApplied && <p className="text-xs text-gray-600 mt-1">{job.dateApplied}</p>}
                    {job.notes && <p className="text-xs text-gray-400 mt-1 line-clamp-2">{job.notes}</p>}
                    {/* Status change dropdown */}
                    <select
                      value={job.status}
                      onChange={(e) => updateJob(job.id, { status: e.target.value as JobApplication['status'] })}
                      className="mt-2 w-full text-xs bg-gray-800 border border-gray-700 rounded px-1.5 py-1 text-gray-400"
                    >
                      {COLUMNS.map((c) => (
                        <option key={c.key} value={c.key}>{c.label}</option>
                      ))}
                    </select>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      {/* Modal */}
      {modalOpen && (
        <JobFormModal
          job={editingJob}
          onSave={(data) => {
            if (editingJob) {
              updateJob(editingJob.id, data);
            } else {
              addJob(data as Omit<JobApplication, 'id' | 'createdAt'>);
            }
            setModalOpen(false);
          }}
          onClose={() => setModalOpen(false)}
        />
      )}
    </div>
  );
}

function StatBox({ label, value, color }: { label: string; value: number | string; color: string }) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
      <div className="text-xs text-gray-400 uppercase">{label}</div>
      <div className={`text-2xl font-bold ${color} mt-1`}>{value}</div>
    </div>
  );
}

function JobFormModal({ job, onSave, onClose }: {
  job: JobApplication | null;
  onSave: (data: Partial<JobApplication>) => void;
  onClose: () => void;
}) {
  const [form, setForm] = useState({
    company: job?.company || '',
    position: job?.position || '',
    status: job?.status || 'research' as JobApplication['status'],
    dateApplied: job?.dateApplied || new Date().toISOString().split('T')[0],
    cvVersion: job?.cvVersion || '',
    notes: job?.notes || '',
    followUpDate: job?.followUpDate || '',
    link: job?.link || '',
  });

  const set = (key: string, value: string) => setForm({ ...form, [key]: value });

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center" onClick={onClose}>
      <div className="fixed inset-0 bg-black/60" />
      <div className="relative bg-gray-900 border border-gray-700 rounded-xl w-full max-w-md p-6 space-y-4" onClick={(e) => e.stopPropagation()}>
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white">{job ? 'Başvuru Düzenle' : 'Yeni Başvuru'}</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white"><HiOutlineX className="w-5 h-5" /></button>
        </div>

        <Field label="Şirket" value={form.company} onChange={(v) => set('company', v)} required />
        <Field label="Pozisyon" value={form.position} onChange={(v) => set('position', v)} required />
        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-gray-400 mb-1">Durum</label>
            <select
              value={form.status}
              onChange={(e) => set('status', e.target.value)}
              className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white"
            >
              {COLUMNS.map((c) => <option key={c.key} value={c.key}>{c.label}</option>)}
            </select>
          </div>
          <Field label="Başvuru Tarihi" value={form.dateApplied} onChange={(v) => set('dateApplied', v)} type="date" />
        </div>
        <Field label="CV Versiyonu" value={form.cvVersion} onChange={(v) => set('cvVersion', v)} placeholder="Full Stack v2" />
        <Field label="İlan Linki" value={form.link} onChange={(v) => set('link', v)} placeholder="https://..." />
        <Field label="Follow-up Tarihi" value={form.followUpDate} onChange={(v) => set('followUpDate', v)} type="date" />
        <div>
          <label className="block text-xs text-gray-400 mb-1">Notlar</label>
          <textarea
            value={form.notes}
            onChange={(e) => set('notes', e.target.value)}
            rows={3}
            className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white resize-none"
          />
        </div>

        <button
          onClick={() => { if (form.company && form.position) onSave(form); }}
          className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-medium transition-colors"
        >
          {job ? 'Güncelle' : 'Ekle'}
        </button>
      </div>
    </div>
  );
}

function Field({ label, value, onChange, type = 'text', placeholder, required }: {
  label: string; value: string; onChange: (v: string) => void; type?: string; placeholder?: string; required?: boolean;
}) {
  return (
    <div>
      <label className="block text-xs text-gray-400 mb-1">{label}{required && ' *'}</label>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white"
      />
    </div>
  );
}
