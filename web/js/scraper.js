// 榜单数据页面JavaScript

let currentDate = getQueryParam('date') || getTodayString();
let currentPlatform = 'app_store';
let currentCategory = 'health_fitness'; // 当前选中的分类
let currentSort = { column: null, order: 'asc' }; // 当前排序状态
let currentApps = []; // 当前显示的应用数据

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

// 初始化页面
async function init() {
    // 加载日期列表
    const dates = await getAvailableDates();
    
    // 检查当前日期是否有数据
    const isToday = currentDate === getTodayString();
    const hasData = dates.includes(currentDate);
    
    if (!hasData && isToday) {
        // 今天没有数据，显示爬取中状态
        showScrapingStatus();
        // 开始轮询检查数据
        pollForData();
    } else if (!hasData) {
        // 历史日期没有数据，切换到最新的可用日期
        currentDate = dates[0];
        console.log(`当前日期 ${currentDate} 没有数据，切换到 ${currentDate}`);
    }
    
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

    // 只有在有数据时才加载数据
    if (hasData) {
        loadData();
    }
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

// 渲染日期列表
function renderDateList(dates) {
    const dateList = document.getElementById('dateList');
    dateList.innerHTML = dates.map(date => `
        <li class="date-item ${date === currentDate ? 'active' : ''}"
            onclick="changeDate('${date}')">
            ${formatDate(date)}
        </li>
    `).join('');
}

// 切换日期
function changeDate(date) {
    const url = new URL(window.location);
    url.searchParams.set('date', date);
    window.location.href = url.toString();
}

// 加载数据 - 只加载当前选中的分类
async function loadData() {
    const content = document.getElementById('dataContent');
    content.innerHTML = '<p>加载中...</p>';

    try {
        const categoryName = categories[currentPlatform][currentCategory];
        const data = await loadJSON(`../data/raw/${currentDate}/${currentPlatform}/${currentCategory}.json`);

        if (data && data.apps) {
            currentApps = data.apps;
            currentSort = { column: null, order: 'asc' }; // 重置排序
            renderTable(categoryName);
        } else {
            content.innerHTML = `
                <div class="data-table">
                    <h4>${categoryName}</h4>
                    <p style="padding: 20px; color: #6b7280;">暂无数据</p>
                </div>
            `;
        }
    } catch (error) {
        content.innerHTML = '<p style="color: red;">加载失败，请检查数据文件</p>';
        console.error('加载数据失败:', error);
    }
}

// 渲染表格
function renderTable(categoryName) {
    const content = document.getElementById('dataContent');
    const sortIndicator = (col) => {
        if (currentSort.column === col) {
            return currentSort.order === 'asc' ? ' ↑' : ' ↓';
        }
        return '';
    };

    const html = `
        <div class="data-table">
            <h4>${categoryName} (${currentApps.length}个应用)</h4>
            <table>
                <thead>
                    <tr>
                        <th>排名</th>
                        <th>图标</th>
                        <th>应用名称</th>
                        <th>开发者</th>
                        <th class="sortable" onclick="sortTable('release_date')">上架时间${sortIndicator('release_date')}</th>
                        <th>评分</th>
                        <th>评价数</th>
                        <th>链接</th>
                    </tr>
                </thead>
                <tbody>
                    ${currentApps.map(app => `
                        <tr>
                            <td><strong>#${app.rank}</strong></td>
                            <td><img src="${app.icon_url}" alt="${app.name}" class="app-icon" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22><rect width=%2240%22 height=%2240%22 fill=%22%23ddd%22/></svg>'"></td>
                            <td>
                                <div class="app-name">${app.name}</div>
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
            <p style="text-align: center; padding: 15px; color: #6b7280;">共 ${currentApps.length} 个应用</p>
        </div>
    `;
    content.innerHTML = html;
}

// 表格排序
function sortTable(column) {
    // 切换排序方向
    if (currentSort.column === column) {
        currentSort.order = currentSort.order === 'asc' ? 'desc' : 'asc';
    } else {
        currentSort.column = column;
        currentSort.order = 'desc'; // 默认倒序（新到旧）
    }

    // 排序数据
    currentApps.sort((a, b) => {
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
    const categoryName = categories[currentPlatform][currentCategory];
    renderTable(categoryName);
}

// 显示爬取中状态
function showScrapingStatus() {
    const content = document.getElementById('dataContent');
    const categoryName = categories[currentPlatform][currentCategory];
    
    content.innerHTML = `
        <div class="data-table">
            <h4>${categoryName}</h4>
            <div style="padding: 40px; text-align: center;">
                <div class="loading-spinner"></div>
                <p style="color: #6b7280; margin-top: 20px; font-size: 18px; font-weight: bold;">
                    🚀 正在爬取 ${formatDate(currentDate)} 的榜单数据
                </p>
                <p style="color: #9ca3af; font-size: 14px; margin-top: 10px;">预计需要 5-10 分钟，请稍候...</p>
                <p style="color: #9ca3af; font-size: 14px;">页面将在爬取完成后自动刷新</p>
            </div>
        </div>
    `;
}

// 轮询检查数据是否生成
function pollForData() {
    const maxAttempts = 60; // 最多检查60次（10分钟）
    let attempts = 0;
    
    const poll = async () => {
        attempts++;
        console.log(`检查数据 (${attempts}/${maxAttempts})...`);
        
        try {
            const categoryName = categories[currentPlatform][currentCategory];
            const data = await loadJSON(`../data/raw/${currentDate}/${currentPlatform}/${currentCategory}.json`);
            
            if (data && data.apps) {
                console.log('数据爬取完成!');
                showToast('数据爬取完成!', 'success');
                
                // 重新加载数据
                currentApps = data.apps;
                currentSort = { column: null, order: 'asc' };
                renderTable(categoryName);
                
                // 刷新日期列表
                refreshDateList();
                return;
            }
        } catch (error) {
            // 数据还不存在，继续轮询
        }
        
        if (attempts >= maxAttempts) {
            console.log('轮询超时');
            showToast('爬取超时，请稍后手动刷新页面', 'error');
            return;
        }
        
        // 10秒后再次检查
        setTimeout(poll, 10000);
    };
    
    poll();
}

// 刷新日期列表
async function refreshDateList() {
    try {
        const dates = await getAvailableDates();
        renderDateList(dates);
    } catch (error) {
        console.error('刷新日期列表失败:', error);
    }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', init);
