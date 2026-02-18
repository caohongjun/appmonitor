// 主页JavaScript

// 检查今天的数据并跳转到榜单页面
async function checkAndGoToScraper() {
    const today = getTodayString();
    const testUrl = `../data/raw/${today}/app_store/health_fitness.json`;
    
    try {
        const response = await fetch(testUrl);
        if (response.ok) {
            window.location.href = 'scraper.html';
        } else {
            await startScrapingAndRedirect();
        }
    } catch (error) {
        await startScrapingAndRedirect();
    }
}

// 开始爬取并跳转
async function startScrapingAndRedirect() {
    const today = getTodayString();
    
    try {
        showToast('今天的数据不存在，正在开始爬取...', 'info');
        
        const response = await fetch('/api/scrape', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                date: today
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showToast('爬取任务已启动，正在跳转...', 'success');
            setTimeout(() => {
                window.location.href = 'scraper.html';
            }, 1000);
        } else {
            showToast('启动爬取失败: ' + (result.error || '未知错误'), 'error');
        }
    } catch (error) {
        console.error('启动爬取失败:', error);
        showToast('启动爬取失败: ' + error.message, 'error');
    }
}

// 检查并运行检测模块
async function checkAndRunDetector() {
    const today = getTodayString();
    const testUrl = `../data/new_apps/${today}.json`;
    
    try {
        // 检查当天是否已有检测数据
        const response = await fetch(testUrl);
        if (response.ok) {
            // 已有数据，直接跳转
            window.location.href = 'detector.html';
            return;
        }
        
        // 没有数据，需要重新检测
        showToast('今天还没有检测数据，正在开始检测...', 'info');
        
        const detectResponse = await fetch('/api/detect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ force: true })  // 使用 force 确保能检测到新数据
        });
        
        const result = await detectResponse.json();
        
        if (result.success) {
            showToast('检测任务已启动，正在跳转...', 'success');
            setTimeout(() => {
                window.location.href = 'detector.html';
            }, 1000);
        } else {
            showToast('启动检测失败: ' + (result.error || '未知错误'), 'error');
        }
    } catch (error) {
        console.error('启动检测失败:', error);
        showToast('启动检测失败: ' + error.message, 'error');
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
        // 直接检查当天
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
        const analyzedData = await loadJSON('../data/analyzed_apps.json');
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

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
});
