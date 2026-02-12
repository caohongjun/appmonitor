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
function startAnalysis(appId, platform) {
    // 查找应用
    const app = analysisQueue.find(item =>
        item.app_id === appId && item.platform === platform
    );

    if (!app) {
        alert('应用不存在');
        return;
    }

    // TODO: 这里将来调用后端API进行分析
    alert(`开始分析 "${app.name}"\n\n此功能将在后续版本中实现。\n当前仅展示队列管理功能。`);

    // 暂时模拟：更新状态为"分析中"
    app.status = 'analyzing';
    localStorage.setItem('analysisQueue', JSON.stringify(analysisQueue));

    // 刷新页面
    loadAnalysisQueue();
    renderTable();
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

    // TODO: 这里将来展示分析结果
    alert(`查看 "${app.name}" 的分析结果\n\n此功能将在后续版本中实现。`);
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

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', init);
