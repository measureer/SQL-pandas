// WebDAV 同步：配置管理 + 上传 / 下载 / 测试连接（纯 fetch，无依赖）

const CFG_KEY = 'sql-pandas-lab:webdav';

const DEFAULT_CFG = {
  url: '',
  username: '',
  password: '',
  filename: 'sql-pandas-progress.json',
  autoUpload: false,
};

export function getConfig() {
  try {
    const raw = localStorage.getItem(CFG_KEY);
    if (!raw) return { ...DEFAULT_CFG };
    return { ...DEFAULT_CFG, ...JSON.parse(raw) };
  } catch {
    return { ...DEFAULT_CFG };
  }
}

export function saveConfig(cfg) {
  localStorage.setItem(CFG_KEY, JSON.stringify({ ...DEFAULT_CFG, ...cfg }));
}

export function isConfigured(cfg = getConfig()) {
  return !!cfg.url.trim();
}

function fileUrl(cfg) {
  const base = cfg.url.trim().replace(/\/+$/, '');
  const name = (cfg.filename || DEFAULT_CFG.filename).trim().replace(/^\/+/, '');
  return `${base}/${name}`;
}

function headers(cfg, extra = {}) {
  const h = { ...extra };
  if (cfg.username || cfg.password) {
    h['Authorization'] = 'Basic ' + btoa(unescape(encodeURIComponent(`${cfg.username}:${cfg.password}`)));
  }
  return h;
}

// 统一错误信息：401 凭据问题，网络层失败多半是 CORS / 地址不可达
async function request(cfg, method, { body, extraHeaders, notFoundMsg } = {}) {
  let res;
  try {
    res = await fetch(fileUrl(cfg), {
      method,
      headers: headers(cfg, extraHeaders),
      body,
    });
  } catch {
    throw new Error('无法连接服务器：请检查地址，或该 WebDAV 服务不允许浏览器跨域（CORS）访问');
  }
  if (res.status === 401 || res.status === 403) {
    throw new Error('认证失败：请检查用户名 / 密码');
  }
  if (res.status === 404 && notFoundMsg) {
    throw new Error(notFoundMsg);
  }
  if (!res.ok) {
    throw new Error(`服务器返回 ${res.status} ${res.statusText}`);
  }
  return res;
}

export async function testConnection(cfg) {
  await request(cfg, 'PROPFIND', { extraHeaders: { Depth: '0' } });
}

export async function upload(cfg, jsonText) {
  await request(cfg, 'PUT', {
    body: jsonText,
    extraHeaders: { 'Content-Type': 'application/json; charset=utf-8' },
  });
}

export async function download(cfg) {
  const res = await request(cfg, 'GET', { notFoundMsg: '云端还没有备份文件' });
  return res.text();
}
