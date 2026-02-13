// AI智能分析页面JavaScript

let currentPlatform = 'all';
let currentStatus = 'all';
let analysisQueue = [];

const platformNames = {
    'app_store': 'App Store',
    'google_play': 'Google Play'
};

const statusNames = {
    'pending': '待分析',
    'analyzing': '分析中',
    'completed': '已完成'
};

const statusColors = {
    'pending': '#f59e0b',
    'analyzing': '#3b82f6',
    'completed': '#10b981'
};

// 初始化页面
function init() {
    // 加载分析队列
    loadAnalysisQueue();

    // 平台Tab切换
    document.querySelectorAll('.tabs .tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tabs .tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentPlatform = tab.dataset.platform;
            renderTable();
        });
    });

    // 渲染表格
    renderTable();
}

// 加载分析队列
function loadAnalysisQueue() {
    const queueData = localStorage.getItem('analysisQueue');
    analysisQueue = queueData ? JSON.parse(queueData) : [];

    // 更新统计信息
    updateStats();
}

// 更新统计信息
function updateStats() {
    const pending = analysisQueue.filter(app => app.status === 'pending').length;
    const analyzing = analysisQueue.filter(app => app.status === 'analyzing').length;
    const completed = analysisQueue.filter(app => app.status === 'completed').length;

    document.getElementById('pendingCount').textContent = pending;
    document.getElementById('analyzingCount').textContent = analyzing;
    document.getElementById('completedCount').textContent = completed;
}

// 按状态筛选
function filterByStatus(status) {
    currentStatus = status;

    // 更新侧边栏激活状态
    document.querySelectorAll('.sidebar .date-item').forEach((item, index) => {
        item.classList.remove('active');
        const statuses = ['all', 'pending', 'analyzing', 'completed'];
        if (statuses[index] === status) {
            item.classList.add('active');
        }
    });

    renderTable();
}

// 渲染表格
function renderTable() {
    const content = document.getElementById('dataContent');

    // 筛选数据
    let filteredApps = analysisQueue;

    // 按平台筛选
    if (currentPlatform !== 'all') {
        const platformName = platformNames[currentPlatform];
        filteredApps = filteredApps.filter(app => app.platform === platformName);
    }

    // 按状态筛选
    if (currentStatus !== 'all') {
        filteredApps = filteredApps.filter(app => app.status === currentStatus);
    }

    if (filteredApps.length === 0) {
        content.innerHTML = `
            <div class="data-table">
                <p style="padding: 40px; text-align: center; color: #6b7280;">
                    暂无应用
                </p>
            </div>
        `;
        return;
    }

    const html = `
        <div class="data-table">
            <h4>应用列表 (${filteredApps.length}个应用)</h4>
            <table>
                <thead>
                    <tr>
                        <th>图标</th>
                        <th>应用名称</th>
                        <th>平台</th>
                        <th>分类</th>
                        <th>开发者</th>
                        <th>添加时间</th>
                        <th>状态</th>
                        <th>操作</th>
                    </tr>
                </thead>
                <tbody>
                    ${filteredApps.map((app, index) => `
                        <tr>
                            <td><img src="${app.icon_url}" alt="${app.name}" class="app-icon" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22><rect width=%2240%22 height=%2240%22 fill=%22%23ddd%22/></svg>'"></td>
                            <td>
                                <div class="app-name">${app.name}</div>
                            </td>
                            <td>${app.platform}</td>
                            <td>${app.category}</td>
                            <td><div class="app-developer">${app.developer}</div></td>
                            <td>${formatDateTime(app.added_time)}</td>
                            <td><span class="status-badge" style="background-color: ${statusColors[app.status]}">${statusNames[app.status]}</span></td>
                            <td>
                                ${app.status === 'pending' ? `<button class="btn-small btn-primary" onclick="startAnalysis('${app.app_id}', '${app.platform}')">开始分析</button>` : ''}
                                ${app.status === 'analyzing' ? `<button class="btn-small btn-info" onclick="viewAnalysis('${app.app_id}', '${app.platform}')">查看进度</button>` : ''}
                                ${app.status === 'completed' ? `<button class="btn-small" onclick="viewAnalysis('${app.app_id}', '${app.platform}')">查看结果</button>` : ''}
                                <button class="btn-small btn-danger" onclick="removeFromQueue('${app.app_id}', '${app.platform}')">移除</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <p style="text-align: center; padding: 15px; color: #6b7280;">共 ${filteredApps.length} 个应用</p>
        </div>
    `;

    content.innerHTML = html;
}

// 格式化日期时间
function formatDateTime(isoString) {
    if (!isoString) return '-';
    const date = new Date(isoString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}/${month}/${day} ${hours}:${minutes}`;
}

// 开始分析
async function startAnalysis(appId, platform) {
    // 查找应用
    const app = analysisQueue.find(item =>
        item.app_id === appId && item.platform === platform
    );

    if (!app) {
        alert('应用不存在');
        return;
    }

    // 确认
    const confirmed = confirm(`确定要开始分析 "${app.name}" 吗？\n\n这将调用AI进行深度分析，可能需要1-2分钟。`);
    if (!confirmed) {
        return;
    }

    // 更新状态为"分析中"
    app.status = 'analyzing';
    localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));

    // 刷新页面
    loadAnalysisQueue();
    renderTable();

    try {
        // 调用API触发分析
        const response = await fetch('http://localhost:8000/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                app_id: appId,
                platform: platform
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast(`✓ 分析任务已启动: ${app.name}`, 'success');

            // 开始轮询检查结果
            pollAnalysisResult(appId, platform, app.name);
        } else {
            throw new Error(data.error || '启动分析失败');
        }
    } catch (error) {
        console.error('启动分析失败:', error);
        showToast(`✗ 启动分析失败: ${error.message}`, 'error');

        // 恢复状态为pending
        app.status = 'pending';
        localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));
        loadAnalysisQueue();
        renderTable();
    }
}

// 轮询检查分析结果
async function pollAnalysisResult(appId, platform, appName) {
    const maxAttempts = 60; // 最多检查60次（约10分钟）
    let attempts = 0;

    const checkInterval = setInterval(async () => {
        attempts++;

        try {
            const today = getTodayString();
            const response = await fetch(`http://localhost:8000/api/analysis/${appId}?platform=${encodeURIComponent(platform)}&date=${today}`);

            if (response.ok) {
                // 分析完成
                clearInterval(checkInterval);

                // 更新状态为completed
                const app = analysisQueue.find(item =>
                    item.app_id === appId && item.platform === platform
                );

                if (app) {
                    app.status = 'completed';
                    app.analyzed_time = new Date().toISOString();
                    localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));
                    loadAnalysisQueue();
                    renderTable();

                    showToast(`✓ 分析完成: ${appName}`, 'success');
                }
            } else if (attempts >= maxAttempts) {
                // 超时
                clearInterval(checkInterval);
                showToast('分析超时，请稍后刷新查看结果', 'warning');

                // 恢复pending状态
                const app = analysisQueue.find(item =>
                    item.app_id === appId && item.platform === platform
                );
                if (app) {
                    app.status = 'pending';
                    localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));
                    loadAnalysisQueue();
                    renderTable();
                }
            }
        } catch (error) {
            console.error('检查状态失败:', error);
            if (attempts >= maxAttempts) {
                clearInterval(checkInterval);
            }
        }
    }, 10000); // 每10秒检查一次
}

// 显示Toast提示
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' :
                     type === 'error' ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' :
                     type === 'warning' ? 'linear-gradient(135deg, #f59e0b 0%, #d97706 100%)' :
                     'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        font-weight: 600;
        animation: slideInRight 0.3s ease;
    `;
    toast.textContent = message;

    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from { transform: translateX(400px); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        @keyframes slideOutRight {
            from { transform: translateX(0); opacity: 1; }
            to { transform: translateX(400px); opacity: 0; }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// 查看分析结果
function viewAnalysis(appId, platform) {
    const app = analysisQueue.find(item =>
        item.app_id === appId && item.platform === platform
    );

    if (!app) {
        alert('应用不存在');
        return;
    }

    // 跳转到详情页面
    window.location.href = `analysis-detail.html?app_id=${encodeURIComponent(appId)}&platform=${encodeURIComponent(platform)}`;
}

// 从队列中移除
function removeFromQueue(appId, platform) {
    const confirmed = confirm('确定要从分析队列中移除此应用吗？');

    if (confirmed) {
        // 从队列中移除
        analysisQueue = analysisQueue.filter(item =>
            !(item.app_id === appId && item.platform === platform)
        );

        // 保存到 localStorage
        localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));

        // 刷新页面
        loadAnalysisQueue();
        renderTable();

        alert('已移除');
    }
}

// 自动检查分析结果
async function autoCheckAnalysisResults() {
    const today = getTodayString();

    for (const app of analysisQueue) {
        if (app.status === 'pending' || app.status === 'analyzing') {
            // 检查是否有分析结果
            try {
                const response = await fetch(`../data/analysis/${today}/${app.app_id}.json`);
                if (response.ok) {
                    // 分析已完成
                    app.status = 'completed';
                    app.analyzed_time = new Date().toISOString();
                }
            } catch (error) {
                // 文件不存在，继续等待
            }
        }
    }

    // 保存更新后的队列
    localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));
    updateStats();
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    init();

    // 每30秒自动检查一次分析结果
    setInterval(() => {
        autoCheckAnalysisResults().then(() => {
            renderTable(); // 刷新表格显示
        });
    }, 30000);
});
