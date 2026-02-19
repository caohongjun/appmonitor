// 新上榜产品页面JavaScript

let currentDate = getQueryParam('date') || getTodayString();
let currentPlatform = 'app_store';
let currentCategory = 'health_fitness';
let allNewApps = []; // 存储所有新产品数据
let currentSort = { column: null, order: 'asc' }; // 当前排序状态
let filteredApps = []; // 当前筛选后的应用数据

const categories = {
    'app_store': {
        'health_fitness': '健康与健身',
        'social': '社交网络',
        'lifestyle': '生活方式',
        'games': '游戏'
    },
    'google_play': {
        'health_fitness': '健康与健身',
        'social': '社交',
        'lifestyle': '生活方式',
        'games': '游戏',
        'dating': '约会',
        'tools': '工具'
    }
};

const platformNames = {
    'app_store': 'App Store',
    'google_play': 'Google Play'
};

// 初始化页面
async function init() {
    // 加载日期列表
    const dates = await getNewAppsDate();
    renderDateList(dates);

    // 平台Tab切换
    document.querySelectorAll('.tabs:not(.category-tabs) .tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tabs:not(.category-tabs) .tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentPlatform = tab.dataset.platform;

            // 重置为第一个分类
            currentCategory = Object.keys(categories[currentPlatform])[0];

            // 重新渲染分类tabs
            renderCategoryTabs();

            // 加载数据
            loadData();
        });
    });

    // 渲染分类tabs
    renderCategoryTabs();

    // 加载数据
    loadData();
}

// 渲染分类Tabs
function renderCategoryTabs() {
    const categoryTabsContainer = document.getElementById('categoryTabs');
    const categoryKeys = Object.keys(categories[currentPlatform]);

    categoryTabsContainer.innerHTML = categoryKeys.map(key => `
        <div class="tab ${key === currentCategory ? 'active' : ''}" data-category="${key}">
            ${categories[currentPlatform][key]}
        </div>
    `).join('');

    // 添加分类tab点击事件
    categoryTabsContainer.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            categoryTabsContainer.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentCategory = tab.dataset.category;
            loadData();
        });
    });
}

// 获取有新上榜产品数据的日期
async function getNewAppsDate() {
    // 获取所有可用的日期
    const dates = [];
    
    try {
        // 使用 API 获取实际存在的日期
        const response = await fetch('/api/detector/dates');
        if (response.ok) {
            const data = await response.json();
            dates.push(...(data.dates || []));
        }
    } catch (e) {
        // 忽略错误
    }

    return dates;
}

// 渲染日期列表
function renderDateList(dates) {
    const dateList = document.getElementById('dateList');
    if (dates.length === 0) {
        dateList.innerHTML = '<li style="padding: 15px; color: #6b7280;">暂无数据</li>';
        return;
    }

    dateList.innerHTML = dates.map(date => `
        <li class="date-item ${date === currentDate ? 'active' : ''}"
            onclick="changeDate('${date}')">
            ${formatDate(date)}
        </li>
    `).join('');
}

// 切换日期
function changeDate(date) {
    window.location.href = `?date=${date}`;
}

// 加载数据 - 只显示当前选中的平台和分类
async function loadData() {
    const content = document.getElementById('dataContent');
    content.innerHTML = '<p>加载中...</p>';

    try {
        const data = await loadJSON(`../data/new_apps/${currentDate}.json`);

        if (!data) {
            content.innerHTML = '<p style="color: #6b7280;">该日期暂无新上榜产品数据</p>';
            return;
        }

        // 更新头部信息（如果元素存在）
        const currentDateEl = document.getElementById('currentDate');
        const compareDateEl = document.getElementById('compareDate');
        if (currentDateEl) {
            currentDateEl.textContent = `今天: ${formatDate(data.date)}`;
        }
        if (compareDateEl) {
            compareDateEl.textContent = `对比: ${formatDate(data.compare_date)}`;
        }

        // 存储所有新产品
        allNewApps = data.new_apps;

        if (allNewApps.length === 0) {
            content.innerHTML = '<p style="color: #6b7280; padding: 40px; text-align: center;">🎉 该日期无新上榜产品</p>';
            return;
        }

        // 筛选当前平台和分类的新产品
        const platformName = platformNames[currentPlatform];
        const categoryName = categories[currentPlatform][currentCategory];

        filteredApps = allNewApps.filter(app =>
            app.platform === platformName && app.category === categoryName
        );

        currentSort = { column: null, order: 'asc' }; // 重置排序
        renderDetectorTable(platformName, categoryName);
    } catch (error) {
        content.innerHTML = '<p style="color: red;">加载失败，请检查数据文件</p>';
        console.error('加载数据失败:', error);
    }
}

// 渲染新产品表格
function renderDetectorTable(platformName, categoryName) {
    const content = document.getElementById('dataContent');

    if (filteredApps.length === 0) {
        content.innerHTML = `
            <div class="data-table">
                <p style="padding: 40px; text-align: center; color: #6b7280;">
                    🎉 ${platformName} - ${categoryName} 暂无新上榜产品
                </p>
            </div>
        `;
        return;
    }

    const sortIndicator = (col) => {
        if (currentSort.column === col) {
            return currentSort.order === 'asc' ? ' ↑' : ' ↓';
        }
        return '';
    };

    const html = `
        <div class="data-table">
            <h4>${platformName} - ${categoryName} (${filteredApps.length}个新产品)</h4>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>图标</th>
                        <th>应用名称</th>
                        <th>开发者</th>
                        <th class="sortable" onclick="sortDetectorTable('release_date')">上架时间${sortIndicator('release_date')}</th>
                        <th>评分</th>
                        <th>评价数</th>
                        <th>链接</th>
                    </tr>
                </thead>
                <tbody>
                    ${filteredApps.map((app, index) => `
                        <tr>
                            <td><strong>#${app.rank}</strong></td>
                            <td><img src="${app.icon_url}" alt="${app.name}" class="app-icon" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22><rect width=%2240%22 height=%2240%22 fill=%22%23ddd%22/></svg>'"></td>
                            <td>
                                <div class="app-name clickable" onclick="requestAnalysis(${index})">${app.name}</div>
                            </td>
                            <td><div class="app-developer">${app.developer}</div></td>
                            <td>${app.release_date || '-'}</td>
                            <td>${app.rating ? app.rating.toFixed(1) + ' ⭐' : '-'}</td>
                            <td>${app.rating_count ? app.rating_count.toLocaleString() : '-'}</td>
                            <td><a href="${app.store_url}" target="_blank">查看</a></td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
            <p style="text-align: center; padding: 15px; color: #6b7280;">共 ${filteredApps.length} 个新产品</p>
        </div>
    `;

    content.innerHTML = html;
}

// 表格排序
function sortDetectorTable(column) {
    // 切换排序方向
    if (currentSort.column === column) {
        currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.order = 'desc'; // 默认倒序（新到旧）
    }

    // 排序数据
    filteredApps.sort((a, b) => {
        let valueA = a[column] || '';
        let valueB = b[column] || '';

        // 日期比较
        if (column === 'release_date') {
            // 将 YYYY/MM/DD 转换为时间戳进行比较
            const dateA = valueA ? new Date(valueA.replace(/\//g, '-')).getTime() : 0;
            const dateB = valueB ? new Date(valueB.replace(/\//g, '-')).getTime() : 0;
            return currentSort.order === 'asc' ? dateA - dateB : dateB - dateA;
        }

        // 默认字符串比较
        if (currentSort.order === 'asc') {
            return valueA > valueB ? 1 : -1;
        } else {
            return valueA < valueB ? 1 : -1;
        }
    });

    // 重新渲染表格
    const platformName = platformNames[currentPlatform];
    const categoryName = categories[currentPlatform][currentCategory];
    renderDetectorTable(platformName, categoryName);
}

// 当前选中的应用
let selectedApp = null;

// 请求分析应用
function requestAnalysis(index) {
    if (!filteredApps || !filteredApps[index]) {
        return;
    }
    
    selectedApp = filteredApps[index];
    showAnalysisModal(selectedApp);
}

// 显示分析弹窗
function showAnalysisModal(app) {
    const modal = document.getElementById('analysisModal');

    // 保存应用信息到全局变量
    selectedApp = app;

    // 填充应用信息
    document.getElementById('modalAppIcon').src = app.icon_url;
    document.getElementById('modalAppIcon').alt = app.name;
    document.getElementById('modalAppName').textContent = app.name;
    document.getElementById('modalAppPlatform').textContent = app.platform;
    document.getElementById('modalAppCategory').textContent = app.category;
    document.getElementById('modalAppDeveloper').textContent = app.developer;

    // 显示弹窗
    modal.classList.add('show');

    // 点击遮罩层关闭弹窗
    modal.onclick = function(e) {
        if (e.target === modal) {
            closeAnalysisModal();
        }
    };
}

// 关闭分析弹窗
function closeAnalysisModal() {
    const modal = document.getElementById('analysisModal');
    modal.classList.remove('show');
    selectedApp = null;
}

// 加入待分析队列并开始分析
async function addToQueue() {
    if (!selectedApp) {
        return;
    }

    // 添加到队列
    addToAnalysisQueue(selectedApp, 'analyzing');

    // 先保存 app 名称，因为关闭弹窗后 selectedApp 会变为 null
    const appName = selectedApp.name;
    const appId = selectedApp.app_id;
    const platform = selectedApp.platform;

    // 关闭弹窗
    closeAnalysisModal();

    // 显示loading
    showToast(`⚡ 正在启动分析 "${appName}"...`, 'info');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                app_id: appId,
                platform: platform
            })
        });

        const result = await response.json();

        if (result.success) {
            showToast(`✅ "${appName}" 已加入队列并开始分析！`, 'success');
            setTimeout(() => {
                window.location.href = 'analyzer.html';
            }, 1000);
        } else {
            showToast(`❌ 启动分析失败: ${result.error || '未知错误'}`, 'error');
        }
    } catch (error) {
        console.error('启动分析失败:', error);
        showToast(`❌ 启动分析失败: ${error.message}`, 'error');
    }
}

// 立即分析
async function analyzeNow() {
    if (!selectedApp) {
        return;
    }

    // 先添加到分析队列
    addToAnalysisQueue(selectedApp, 'analyzing');

    // 先保存 app 名称，因为关闭弹窗后 selectedApp 会变为 null
    const appName = selectedApp.name;
    const appId = selectedApp.app_id;
    const platform = selectedApp.platform;

    // 先关闭弹窗
    closeAnalysisModal();

    // 显示loading
    showToast(`⚡ 正在启动分析 "${appName}"...`, 'info');

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                app_id: appId,
                platform: platform
            })
        });

        const result = await response.json();

        if (result.success) {
            showToast(`✅ "${appName}" 分析已启动！`, 'success');
            // 等待一下然后跳转
            setTimeout(() => {
                window.location.href = 'analyzer.html';
            }, 1000);
        } else {
            showToast(`❌ 启动分析失败: ${result.error || '未知错误'}`, 'error');
        }
    } catch (error) {
        console.error('启动分析失败:', error);
        showToast(`❌ 启动分析失败: ${error.message}`, 'error');
    }
}

// 显示提示消息
function showToast(message, type = 'info') {
    // 创建toast元素
    const toast = document.createElement('div');
    toast.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'linear-gradient(135deg, #10b981 0%, #059669 100%)' :
                     type === 'info' ? 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)' :
                     'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'};
        color: white;
        padding: 16px 24px;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        font-weight: 600;
        animation: slideInRight 0.3s ease;
    `;
    toast.textContent = message;

    // 添加动画
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

    document.body.appendChild(toast);

    // 3秒后自动消失
    setTimeout(() => {
        toast.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// 添加到分析队列
function addToAnalysisQueue(app, status = 'pending') {
    // 从 localStorage 读取现有队列
    let queue = JSON.parse(localStorage.getItem('analysisQueue') || '[]');

    // 检查是否已存在（根据 app_id 和 platform 判断）
    const existingIndex = queue.findIndex(item =>
        item.app_id === app.app_id && item.platform === app.platform
    );

    if (existingIndex === -1) {
        // 不存在，添加新记录
        app.added_time = new Date().toISOString();
        app.status = status; // pending, analyzing, completed
        queue.push(app);

        // 保存到 localStorage
        localStorage.setItem('analysisQueue', JSON.stringify(queue));

        console.log('已添加到分析队列:', app.name);
    } else {
        // 已存在，更新状态
        queue[existingIndex].status = status;
        localStorage.setItem('analysisQueue', JSON.stringify(queue));
        console.log('已更新应用状态:', app.name, status);
    }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    // 只在detector.html页面中执行初始化
    if (window.location.pathname.endsWith('detector.html') || window.location.pathname.includes('detector')) {
        init();
    }
});
