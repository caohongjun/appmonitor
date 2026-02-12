// 主页JavaScript

// 加载统计数据
async function loadStats() {
    try {
        // 获取数据天数
        const dates = await getAvailableDates();
        document.getElementById('total-dates').textContent = dates.length;

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
        const analyzedData = await loadJSON('../data/analyzed_apps.json');
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
