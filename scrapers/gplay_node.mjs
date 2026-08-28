// Google Play 榜单爬取 Node 脚本
// 通过 facundoolano/google-play-scraper 的 list() 获取分类榜单 Top N
//
// 调用方式：
//   echo '{"category":"TOOLS","collection":"TOP_FREE","num":100,"country":"us","lang":"en"}' | node scrapers/gplay_node.js
//
// 输出：stdout 输出一个 JSON 数组（应用列表），stderr 输出日志。
// 成功退出码 0；失败退出码非 0，错误信息写到 stderr。

import gplay from 'google-play-scraper';

async function readStdin() {
  return new Promise((resolve, reject) => {
    let data = '';
    process.stdin.setEncoding('utf8');
    process.stdin.on('data', (chunk) => { data += chunk; });
    process.stdin.on('end', () => resolve(data));
    process.stdin.on('error', reject);
  });
}

async function main() {
  const raw = await readStdin();
  if (!raw.trim()) {
    console.error('错误：未收到 stdin 输入参数');
    process.exit(2);
  }

  let opts;
  try {
    opts = JSON.parse(raw);
  } catch (e) {
    console.error('错误：参数 JSON 解析失败:', e.message);
    process.exit(2);
  }

  const {
    category,      // 例 "TOOLS"，对应 gplay.category 常量
    collection,    // 例 "TOP_FREE"
    num = 100,
    country = 'us',
    lang = 'en'
  } = opts;

  if (!category) {
    console.error('错误：缺少 category 参数');
    process.exit(2);
  }

  console.error(`[gplay_node] 爬取 category=${category} collection=${collection} num=${num} country=${country}`);
  const startTime = Date.now();

  const listOpts = {
    category,
    num,
    country,
    lang,
    fullDetail: true  // 对每个 app 单独请求详情，拿到 released/ratings/genre 等字段
  };
  if (collection) {
    listOpts.collection = collection;
  }

  let apps;
  try {
    apps = await gplay.list(listOpts);
  } catch (e) {
    console.error('错误：gplay.list 调用失败:', e.message);
    process.exit(1);
  }

  console.error(`[gplay_node] 爬取完成，共 ${apps.length} 个，耗时 ${((Date.now() - startTime) / 1000).toFixed(1)}s`);

  // 输出 JSON 到 stdout（紧凑模式，避免日志干扰）
  process.stdout.write(JSON.stringify(apps));
  process.stdout.write('\n');
}

main().catch((e) => {
  console.error('错误：未捕获异常:', e);
  process.exit(1);
});
