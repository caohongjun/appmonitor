// 主页JavaScript - 本地版本

// 检查今天的数据并跳转到榜单页面
async function checkAndGoToScraper() {
    const today = getTodayString();
    const testUrl = `../data/raw/${today}/app_store/health_fitness.json`;
    
    try {
        const response = await fetch(testUrl);
        if (response.ok) {
            window.location.href = 'scraper.html';
        } else {
            showToast('今天的数据还未爬取，请稍后再试', 'info');
        }
    } catch (error) {
        showToast('检查数据失败: ' + error.message, 'error');
    }
}

// 检查并运行检测模块
async function checkAndRunDetector() {
    const today = getTodayString();
    const testUrl = `../data/new_apps/${today}.json`;
    
    try {
        const response = await fetch(testUrl);
        if (response.ok) {
            window.location.href = 'detector.html';
        } else {
            showToast('今天还没有检测数据，请稍后再试', 'info');
        }
    } catch (error) {
        showToast('检查数据失败: ' + error.message, 'error');
    }
}

// 加载统计数据
async function loadStats() {
    try {
        // 获取数据天数
        const dates = await getAvailableDates();
        document.getElementById('total-dates').textContent = dates.length;

        // 加载模块1日期（最新爬取日期）
        if (dates.length > 0) {
            const latestScrapeDate = dates[0];
            document.getElementById('module1-date').textContent = formatDate(latestScrapeDate);
        } else {
            document.getElementById('module1-date').textContent = '暂无数据';
        }

        // 加载模块2日期（最新新上榜产品分析日期）
        const newAppsDates = [];
        const today = getTodayString();
        try {
            const response = await fetch(`../data/new_apps/${today}.json`);
            if (response.ok) {
                newAppsDates.push(today);
            }
        } catch (e) {}
        
        if (newAppsDates.length > 0) {
            document.getElementById('module2-date').textContent = formatDate(newAppsDates[0]);
        } else {
            document.getElementById('module2-date').textContent = '暂无';
        }

        // 加载模块3日期（最新AI分析日期）
        const analyzedData = await loadJSON(`../data/analyzed_apps.json`);
        if (analyzedData && analyzedData.latest_date) {
            document.getElementById('module3-date').textContent = formatDate(analyzedData.latest_date);
        } else {
            document.getElementById('module3-date').textContent = '暂无';
        }

        // 获取最新一天的应用总数
        if (dates.length > 0) {
            const latestDate = dates[0];
            let totalApps = 0;

            // App Store
            const appStoreCategories = ['health_fitness', 'social', 'lifestyle', 'games'];
            for (const category of appStoreCategories) {
                const data = await loadJSON(`../data/raw/${latestDate}/app_store/${category}.json`);
                if (data && data.apps) {
                    totalApps += data.apps.length;
                }
            }

            // Google Play
            const googlePlayCategories = ['health_fitness', 'social', 'lifestyle', 'games', 'dating', 'tools'];
            for (const category of googlePlayCategories) {
                const data = await loadJSON(`../data/raw/${latestDate}/google_play/${category}.json`);
                if (data && data.apps) {
                    totalApps += data.apps.length;
                }
            }

            document.getElementById('total-apps').textContent = totalApps;
        }

        // 获取新上榜产品数
        const newAppsData = await loadJSON(`../data/new_apps/${getTodayString()}.json`);
        if (newAppsData) {
            document.getElementById('new-apps').textContent = newAppsData.total_count || 0;
        }

        // 获取已分析产品数
        if (analyzedData) {
            document.getElementById('analyzed-apps').textContent = analyzedData.total_count || 0;
        }

    } catch (error) {
        console.error('加载统计数据失败:', error);
    }
}

// 获取可用的日期列表
async function getAvailableDates() {
    try {
        const response = await fetch('../data/raw');
        const text = await response.text();
        
        // 解析目录列表
        const dates = [];
        const regex = /href="([0-9]{4}-[0-9]{2}-[0-9]{2})"/g;
        let match;
        while ((match = regex.exec(text)) !== null) {
            dates.push(match[1]);
        }
        
        return dates.sort().reverse();
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
    loadStats();
});