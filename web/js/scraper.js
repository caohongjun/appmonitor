// 榜单数据页面JavaScript - GitHub Pages 版本

// GitHub 仓库配置
const GITHUB_REPO = 'caohongjun/appmonitor';
const GITHUB_API_BASE = `https://api.github.com/repos/${GITHUB_REPO}/contents/data`;
const GITHUB_RAW_BASE = `https://raw.githubusercontent.com/${GITHUB_REPO}/master/data`;

let currentDate = getQueryParam('date') || getTodayString();
let currentPlatform = 'app_store';
let currentCategory = 'health_fitness';
let currentSort = { column: null, order: 'asc' };
let currentApps = [];

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
    const hasData = dates.includes(currentDate);
    
    if (!hasData) {
        // 切换到最新的可用日期
        currentDate = dates[0] || getTodayString();
    }
    
    renderDateList(dates);

    // 平台Tab切换
    document.querySelectorAll('.tabs:not(.category-tabs) .tab').forEach(tab => {
        tab.addEventListener('click', () => {
            switchPlatform(tab.dataset.platform);
        });
    });

    // 分类Tab切换
    document.querySelectorAll('.category-tabs .tab').forEach(tab => {
        tab.addEventListener('click', () => {
            switchCategory(tab.dataset.category);
        });
    });

    // 加载数据
    await loadData();
}

// 加载数据
async function loadData() {
    try {
        const url = `${GITHUB_RAW_BASE}/raw/${currentDate}/${currentPlatform}/${currentCategory}.json`;
        const data = await loadJSON(url);
        
        if (data && data.apps) {
            currentApps = data.apps;
            renderApps();
        } else {
            showToast('加载数据失败', 'error');
        }
    } catch (error) {
        console.error('加载数据失败:', error);
        showToast('加载数据失败: ' + error.message, 'error');
    }
}

// 切换平台
function switchPlatform(platform) {
    currentPlatform = platform;
    currentCategory = Object.keys(categories[platform])[0];
    updatePlatformTabs();
    updateCategoryTabs();
    loadData();
}

// 切换分类
function switchCategory(category) {
    currentCategory = category;
    updateCategoryTabs();
    loadData();
}

// 渲染日期列表
function renderDateList(dates) {
    const container = document.getElementById('date-list');
    container.innerHTML = dates.map(date => `
        <div class="date-item ${date === currentDate ? 'active' : ''}" 
             onclick="selectDate('${date}')">
            ${formatDate(date)}
        </div>
    `).join('');
}

// 选择日期
function selectDate(date) {
    currentDate = date;
    renderDateList(await getAvailableDates());
    loadData();
}

// 渲染应用列表
function renderApps() {
    const container = document.getElementById('apps-container');
    
    if (currentApps.length === 0) {
        container.innerHTML = '<div class="no-data">暂无数据</div>';
        return;
    }
    
    container.innerHTML = currentApps.map(app => `
        <div class="app-card">
            <img src="${app.icon_url}" alt="${app.name}" class="app-icon" onerror="this.src='https://via.placeholder.com/64'">
            <div class="app-info">
                <div class="app-name">${app.name}</div>
                <div class="app-category">${app.category || 'N/A'}</div>
                <div class="app-rank">排名: ${app.rank || 'N/A'}</div>
            </div>
        </div>
    `).join('');
}

// 更新平台Tab
function updatePlatformTabs() {
    document.querySelectorAll('.tabs:not(.category-tabs) .tab').forEach(tab => {
        tab.classList.toggle('active', tab.dataset.platform === currentPlatform);
    });
}

// 更新分类Tab
function updateCategoryTabs() {
    const container = document.querySelector('.category-tabs');
    container.innerHTML = Object.entries(categories[currentPlatform]).map(([key, name]) => `
        <div class="tab ${key === currentCategory ? 'active' : ''}" 
             data-category="${key}">
            ${name}
        </div>
    `).join('');
    
    // 重新绑定事件
    container.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            switchCategory(tab.dataset.category);
        });
    });
}

// 获取可用的日期列表
async function getAvailableDates() {
    try {
        const response = await fetch(`${GITHUB_API_BASE}/raw`);
        const data = await response.json();
        
        if (data && data.length > 0) {
            return data
                .filter(item => item.type === 'dir')
                .map(item => item.name)
                .sort()
                .reverse();
        }
        return [];
    } catch (error) {
        console.error('获取日期列表失败:', error);
        return [];
    }
}

// 加载 JSON 数据
async function loadJSON(url) {
    try {
        const response = await fetch(url);
        if (response.ok) {
            return await response.json();
        }
        return null;
    } catch (error) {
        console.error('加载 JSON 失败:', url, error);
        return null;
    }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    init();
});