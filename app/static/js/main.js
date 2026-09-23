// ─────────────────────────────────────────────
// Sistem Penilaian Digital — main.js
// ─────────────────────────────────────────────

document.addEventListener('DOMContentLoaded', () => {

  // ── 1. Auto-dismiss flash messages ───────────
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    // Close button
    const closeBtn = alert.querySelector('.alert-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => dismissAlert(alert));
    }
    // Auto dismiss after 4s
    setTimeout(() => dismissAlert(alert), 4000);
  });

  function dismissAlert(el) {
    el.style.animation = 'slideInRight 0.3s ease reverse forwards';
    setTimeout(() => el.remove(), 300);
  }

  // ── 2. Delete Confirm Modal ───────────────────
  const modal        = document.getElementById('confirm-modal');
  const modalForm    = document.getElementById('confirm-form');
  const modalMessage = document.getElementById('modal-message');

  document.querySelectorAll('[data-delete-url]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const url  = btn.dataset.deleteUrl;
      const name = btn.dataset.deleteName || 'item ini';

      if (modalMessage) modalMessage.textContent = `Apakah Anda yakin ingin menghapus "${name}"? Tindakan ini tidak dapat dibatalkan.`;
      if (modalForm)    modalForm.action = url;
      if (modal)        modal.classList.add('open');
    });
  });

  document.getElementById('modal-cancel')?.addEventListener('click', () => {
    modal?.classList.remove('open');
  });

  modal?.addEventListener('click', (e) => {
    if (e.target === modal) modal.classList.remove('open');
  });

  // ── 3. Drag & Drop Upload Zone ────────────────
  const uploadZone  = document.getElementById('upload-zone');
  const fileInput   = document.getElementById('file-input');
  const previewGrid = document.getElementById('preview-grid');

  if (uploadZone && fileInput) {

    uploadZone.addEventListener('dragover',  (e) => {
      e.preventDefault();
      uploadZone.classList.add('drag-over');
    });

    uploadZone.addEventListener('dragleave', () => {
      uploadZone.classList.remove('drag-over');
    });

    uploadZone.addEventListener('drop', (e) => {
      e.preventDefault();
      uploadZone.classList.remove('drag-over');
      const files = Array.from(e.dataTransfer.files).filter(f => isAllowedImage(f));
      addFilesToInput(files);
      showPreviews(files);
    });

    fileInput.addEventListener('change', () => {
      const files = Array.from(fileInput.files);
      showPreviews(files);
    });
  }

  function isAllowedImage(file) {
    return ['image/jpeg', 'image/jpg', 'image/png'].includes(file.type);
  }

  let allFiles = [];

  function addFilesToInput(newFiles) {
    allFiles = [...allFiles, ...newFiles];
    const dt = new DataTransfer();
    allFiles.forEach(f => dt.items.add(f));
    if (fileInput) fileInput.files = dt.files;
  }

  function showPreviews(files) {
    if (!previewGrid) return;
    files.forEach(file => {
      if (!isAllowedImage(file)) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        const item = document.createElement('div');
        item.className = 'preview-item';
        item.innerHTML = `
          <img src="${e.target.result}" alt="${file.name}" />
          <button type="button" class="preview-remove" title="Hapus">×</button>
          <div style="position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,0.7);font-size:9px;padding:3px 6px;color:#fff;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${file.name}</div>
        `;
        item.querySelector('.preview-remove').addEventListener('click', () => {
          allFiles = allFiles.filter(f => f !== file);
          const dt = new DataTransfer();
          allFiles.forEach(f => dt.items.add(f));
          if (fileInput) fileInput.files = dt.files;
          item.remove();
        });
        previewGrid.appendChild(item);
      };
      reader.readAsDataURL(file);
    });
  }

  // ── 4. Active Nav Item ────────────────────────
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-item').forEach(item => {
    const href = item.getAttribute('href') || '';
    if (href && href !== '/' && currentPath.startsWith(href)) {
      item.classList.add('active');
    } else if (href === '/' && currentPath === '/') {
      item.classList.add('active');
    } else if (currentPath === '/dashboard' && href === '/dashboard') {
      item.classList.add('active');
    }
  });

  // ── 5. Sidebar Mobile Toggle ──────────────────
  const menuToggle = document.getElementById('menu-toggle');
  const sidebar    = document.querySelector('.sidebar');

  menuToggle?.addEventListener('click', () => {
    sidebar?.classList.toggle('open');
  });

  // ── 6. Mapel filter auto-submit ───────────────
  const mapelFilter = document.getElementById('mapel-filter');
  mapelFilter?.addEventListener('change', () => {
    mapelFilter.closest('form')?.submit();
  });

  const kelasFilter = document.getElementById('kelas-filter');
  kelasFilter?.addEventListener('change', () => {
    kelasFilter.closest('form')?.submit();
  });

  // ── 7. Chart.js — Dashboard ───────────────────
  const chartCanvas = document.getElementById('activity-chart');
  if (chartCanvas && window.Chart) {
    const labels = JSON.parse(chartCanvas.dataset.labels || '[]');
    const values = JSON.parse(chartCanvas.dataset.values || '[]');

    new Chart(chartCanvas, {
      type: 'bar',
      data: {
        labels,
        datasets: [{
          label: 'Lembar Dinilai',
          data: values,
          backgroundColor: 'rgba(108, 99, 255, 0.3)',
          borderColor: 'rgba(108, 99, 255, 0.9)',
          borderWidth: 2,
          borderRadius: 6,
          borderSkipped: false,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: {
            backgroundColor: '#1e1e3a',
            borderColor: 'rgba(108,99,255,0.3)',
            borderWidth: 1,
            titleColor: '#e8e8f0',
            bodyColor: '#9898b8',
            padding: 12,
          }
        },
        scales: {
          x: {
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: { color: '#9898b8', font: { size: 11 } }
          },
          y: {
            grid: { color: 'rgba(255,255,255,0.04)' },
            ticks: { color: '#9898b8', font: { size: 11 }, stepSize: 1 },
            beginAtZero: true
          }
        }
      }
    });
  }

});
