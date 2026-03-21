export default function ResourcesPage() {
  return (
    <div className="space-y-8">
      <h1 className="text-2xl font-bold text-white">📎 Ücretsiz Kaynaklar</h1>
      <p className="text-gray-400 text-sm">Tüm kaynaklar %100 ücretsiz. Müfredatın her aşamasında kullanılacak en iyi kaynaklar.</p>

      <ResourceCategory
        title="Tam Eğitim Platformları"
        icon="🎓"
        resources={[
          { name: 'The Odin Project', url: 'https://www.theodinproject.com', desc: 'Full stack web development - baştan sona ücretsiz müfredat' },
          { name: 'freeCodeCamp', url: 'https://www.freecodecamp.org', desc: 'Sertifikalı interaktif eğitim platformu' },
          { name: 'Full Stack Open', url: 'https://fullstackopen.com', desc: 'Helsinki Üniversitesi - modern full stack geliştirme' },
          { name: 'CS50 (Harvard)', url: 'https://cs50.harvard.edu', desc: 'Bilgisayar bilimleri temelleri - dünyaca ünlü kurs' },
          { name: 'roadmap.sh', url: 'https://roadmap.sh', desc: 'İnteraktif kariyer yol haritaları' },
        ]}
      />

      <ResourceCategory
        title="AI & Machine Learning"
        icon="🤖"
        resources={[
          { name: 'fast.ai', url: 'https://www.fast.ai', desc: 'Pratik deep learning - yukarıdan aşağıya yaklaşım' },
          { name: 'DeepLearning.AI', url: 'https://www.deeplearning.ai', desc: 'Kısa kurslar ve uzmanlaşma programları' },
          { name: 'Hugging Face Learn', url: 'https://huggingface.co/learn', desc: 'NLP ve Transformers eğitimleri' },
          { name: 'Kaggle', url: 'https://www.kaggle.com', desc: 'Yarışmalar + ücretsiz GPU + veri setleri' },
          { name: 'Andrew Ng ML (Coursera)', url: 'https://www.coursera.org/learn/machine-learning', desc: 'Makine öğrenmesi temelleri - audit modunda ücretsiz' },
          { name: '3Blue1Brown', url: 'https://www.3blue1brown.com', desc: 'Matematik ve neural network görselleştirmeleri' },
          { name: 'Andrej Karpathy', url: 'https://karpathy.ai', desc: 'Neural network eğitimleri (YouTube)' },
        ]}
      />

      <ResourceCategory
        title="Pratik & Mülakat Hazırlığı"
        icon="💪"
        resources={[
          { name: 'NeetCode', url: 'https://neetcode.io', desc: 'NeetCode 150, Blind 75, Grind 75 - ücretsiz problem çözme' },
          { name: 'LeetCode', url: 'https://leetcode.com', desc: 'Algoritma ve veri yapıları problemleri' },
          { name: 'HackerRank', url: 'https://www.hackerrank.com', desc: 'Kodlama challengeları ve sertifikalar' },
          { name: 'Exercism', url: 'https://exercism.org', desc: '70+ dilde mentor destekli pratik' },
          { name: 'Pramp', url: 'https://www.pramp.com', desc: 'Ücretsiz canlı mock interview platformu' },
          { name: 'Tech Interview Handbook', url: 'https://www.techinterviewhandbook.org', desc: 'Kapsamlı mülakat hazırlık rehberi' },
          { name: 'System Design Primer', url: 'https://github.com/donnemartin/system-design-primer', desc: 'Sistem tasarımı mülakat hazırlığı' },
          { name: 'ByteByteGo (YouTube)', url: 'https://www.youtube.com/@ByteByteGo', desc: 'Sistem tasarımı videoları' },
        ]}
      />

      <ResourceCategory
        title="Cloud & DevOps"
        icon="☁️"
        resources={[
          { name: 'AWS Free Tier', url: 'https://aws.amazon.com/free', desc: '12 aylık ücretsiz katman + 750 saat EC2' },
          { name: 'Google Cloud $300', url: 'https://cloud.google.com/free', desc: '$300 deneme kredisi + her zaman ücretsiz ürünler' },
          { name: 'Azure Free', url: 'https://azure.microsoft.com/free', desc: '25+ her zaman ücretsiz servis + $200 kredi' },
          { name: 'Docker Docs', url: 'https://docs.docker.com/get-started', desc: 'Resmi Docker öğrenme yolu' },
          { name: 'KubeAcademy', url: 'https://kube.academy', desc: 'VMware Kubernetes eğitimi' },
        ]}
      />

      <ResourceCategory
        title="Teknik İngilizce"
        icon="🌐"
        resources={[
          { name: 'freeCodeCamp English', url: 'https://www.freecodecamp.org/news/learn-english-for-developers', desc: 'A2 & B1 Developer İngilizcesi' },
          { name: 'English4IT', url: 'https://english4it.com', desc: 'IT profesyonelleri için İngilizce' },
          { name: 'GrokEnglish.dev', url: 'https://grokenglish.dev', desc: 'Yazılımcılar için İngilizce + sözlük' },
          { name: 'Anki', url: 'https://apps.ankiweb.net', desc: 'Spaced repetition ile kelime öğrenme' },
          { name: 'Grammarly', url: 'https://www.grammarly.com', desc: 'Ücretsiz yazım ve dilbilgisi kontrolü' },
        ]}
      />

      <ResourceCategory
        title="Dokümantasyon & Referans"
        icon="📖"
        resources={[
          { name: 'MDN Web Docs', url: 'https://developer.mozilla.org', desc: 'Web teknolojileri referansı - HTML, CSS, JS' },
          { name: 'DevDocs', url: 'https://devdocs.io', desc: 'Birleştirilmiş API dokümantasyonu' },
          { name: 'Can I Use', url: 'https://caniuse.com', desc: 'Tarayıcı uyumluluk tabloları' },
          { name: 'web.dev', url: 'https://web.dev', desc: 'Google - modern web best practices' },
        ]}
      />

      <ResourceCategory
        title="Open Source Katkı"
        icon="🤝"
        resources={[
          { name: 'First Timers Only', url: 'https://www.firsttimersonly.com', desc: 'İlk kez katkı yapanlar için rehber' },
          { name: 'Good First Issues', url: 'https://goodfirstissues.com', desc: 'Başlangıç seviyesi open source issue\'ları' },
          { name: 'Up For Grabs', url: 'https://up-for-grabs.net', desc: 'Katkıda bulunulabilecek projeler' },
          { name: 'CodeTriage', url: 'https://www.codetriage.com', desc: 'Open source projelerine yardım et' },
        ]}
      />
    </div>
  );
}

function ResourceCategory({ title, icon, resources }: {
  title: string; icon: string; resources: { name: string; url: string; desc: string }[];
}) {
  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <div className="px-5 py-3 border-b border-gray-800">
        <h2 className="text-lg font-semibold text-white">{icon} {title}</h2>
      </div>
      <div className="divide-y divide-gray-800/50">
        {resources.map((res) => (
          <a
            key={res.name}
            href={res.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-between px-5 py-3 hover:bg-gray-800/50 transition-colors"
          >
            <div>
              <h3 className="text-sm font-medium text-blue-400">{res.name}</h3>
              <p className="text-xs text-gray-400 mt-0.5">{res.desc}</p>
            </div>
            <span className="text-gray-600 text-sm shrink-0 ml-3">↗</span>
          </a>
        ))}
      </div>
    </div>
  );
}
