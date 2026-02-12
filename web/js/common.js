// 公共函数

// 获取所有可用的日期
async function getAvailableDates() {
    try {
        const response = await fetch('../data/raw/');
        // 由于无法列出目录，我们使用一个简单的方法
        // 尝试加载最近30天的数据
        const dates = [];
        const today = new Date();

        for (let i = 0; i < 30; i++) {
            const date = new Date(today);
            date.setDate(date.getDate() - i);
            const dateStr = date.toISOString().split('T')[0];

            // 尝试加载这个日期的数据
            try {
                const testResponse = await fetch(`../data/raw/${dateStr}/app_store/health_fitness.json`);
                if (testResponse.ok) {
                    dates.push(dateStr);
                }
            } catch (e) {
                // 忽略错误
            }
        }

        return dates;
    } catch (error) {
        console.error('获取日期列表失败:', error);
        return [];
    }
}

// 格式化日期显示
function formatDate(dateStr) {
    const date = new Date(dateStr);
    const month = date.getMonth() + 1;
    const day = date.getDate();
    const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
    const weekday = weekdays[date.getDay()];
    return `${month}月${day}日 (${weekday})`;
}

// 加载JSON数据
async function loadJSON(path) {
    try {
        const response = await fetch(path);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return await response.json();
    } catch (error) {
        console.error('加载数据失败:', path, error);
        return null;
    }
}

// 渲染日期导航
function renderDateNav(dates, currentDate, onDateClick) {
    const dateList = document.querySelector('.date-list');
    if (!dateList) return;

    dateList.innerHTML = dates.map(date => `
        <li class="date-item ${date === currentDate ? 'active' : ''}"
            onclick="window.location.href='?date=${date}'">
            ${formatDate(date)}
            ${date === currentDate ? ' ✓' : ''}
        </li>
    `).join('');
}

// 获取URL参数
function getQueryParam(param) {
    const params = new URLSearchParams(window.location.search);
    return params.get(param);
}

// 获取今天的日期字符串
function getTodayString() {
    return new Date().toISOString().split('T')[0];
}
