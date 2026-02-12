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
    const dates = [];
    const today = new Date();

    for (let i = 0; i < 30; i++) {
        const date = new Date(today);
        date.setDate(date.getDate() - i);
        const dateStr = date.toISOString().split('T')[0];

        try {
            const response = await fetch(`../data/new_apps/${dateStr}.json`);
            if (response.ok) {
                dates.push(dateStr);
            }
        } catch (e) {
            // 忽略错误
        }
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

        // 更新头部信息
        document.getElementById('currentDate').textContent = `今天: ${formatDate(data.date)}`;
        document.getElementById('compareDate').textContent = `对比: ${formatDate(data.compare_date)}`;

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
                    ${filteredApps.map(app => `
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

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', init);
