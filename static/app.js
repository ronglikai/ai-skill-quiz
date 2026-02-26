// AI Skill 知识测试系统 - 通用前端脚本
// 主要逻辑在各模板页面中，此文件放通用工具函数

/**
 * 通用 fetch 包装器
 */
async function apiFetch(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };
    const mergedOptions = { ...defaultOptions, ...options };
    const response = await fetch(url, mergedOptions);
    if (!response.ok) {
        throw new Error(`API请求失败: ${response.status}`);
    }
    return response.json();
}

/**
 * 格式化日期
 */
function formatDate(dateStr) {
    if (!dateStr) return '-';
    const d = new Date(dateStr);
    return d.toLocaleString('zh-CN', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
    });
}
