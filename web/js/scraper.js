// 榜单数据页面JavaScript

let currentDate = getQueryParam('date') || getTodayString();
let currentPlatform = 'app_store';

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
    renderDateList(dates);

    // 显示当前日期
    document.getElementById('currentDate').textContent = formatDate(currentDate);

    // Tab切换
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentPlatform = tab.dataset.platform;
            loadData();
        });
    });

    // 加载数据
    loadData();
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
    window.location.href = `?date=${date}`;
}

// 加载数据
async function loadData() {
    const content = document.getElementById('dataContent');
    content.innerHTML = '<p>加载中...</p>';

    try {
        const categoryKeys = Object.keys(categories[currentPlatform]);
        let html = '';

        for (const key of categoryKeys) {
            const categoryName = categories[currentPlatform][key];
            const data = await loadJSON(`../data/raw/${currentDate}/${currentPlatform}/${key}.json`);

            if (data && data.apps) {
                html += `
                    <div class="data-table">
                        <h4>${categoryName} (${data.apps.length}个应用)</h4>
                        <table>
                            <thead>
                                <tr>
                                    <th>排名</th>
                                    <th>图标</th>
                                    <th>应用名称</th>
                                    <th>开发者</th>
                                    <th>链接</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.apps.map(app => `
                                    <tr>
                                        <td><strong>#${app.rank}</strong></td>
                                        <td><img src="${app.icon_url}" alt="${app.name}" class="app-icon" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%2240%22 height=%2240%22><rect width=%2240%22 height=%2240%22 fill=%22%23ddd%22/></svg>'"></td>
                                        <td>
                                            <div class="app-name">${app.name}</div>
                                        </td>
                                        <td><div class="app-developer">${app.developer}</div></td>
                                        <td><a href="${app.store_url}" target="_blank">查看</a></td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                        <p style="text-align: center; padding: 15px; color: #6b7280;">共 ${data.apps.length} 个应用</p>
                    </div>
                `;
            } else {
                html += `
                    <div class="data-table">
                        <h4>${categoryName}</h4>
                        <p style="padding: 20px; color: #6b7280;">暂无数据</p>
                    </div>
                `;
            }
        }

        content.innerHTML = html;
    } catch (error) {
        content.innerHTML = '<p style="color: red;">加载失败，请检查数据文件</p>';
        console.error('加载数据失败:', error);
    }
}

// 页面加载完成后执行
document.addEventListener('DOMContentLoaded', init);
