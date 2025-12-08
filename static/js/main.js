// 切換側邊欄顯示/隱藏
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('hidden');
}

// Parse markdown content in a container
function parseMarkdown(container) {
    // Find all markdown script tags
    const markdownScripts = container.querySelectorAll('script[type="text/markdown"]');

    // Explicit mapping: script ID -> card content ID
    const contentMapping = {
        'markdown-data': 'card-dataset',
        'markdown-downsampling-page': 'card-downsampling',
        'markdown-reference': 'card-reference'
    };

    markdownScripts.forEach((script) => {
        const scriptId = script.id;
        const contentId = contentMapping[scriptId];

        if (contentId) {
            const contentDiv = container.querySelector(`#${contentId}`);
            if (contentDiv && script.textContent) {
                contentDiv.innerHTML = marked.parse(script.textContent);
            }
        }
    });
}

async function loadPage(pageName, event = null) {
    // 隱藏所有頁面
    document.querySelectorAll('.page-content').forEach(page => {
        page.classList.add('hidden');
    });

    // 取得或創建目標頁面容器
    let targetPage = document.getElementById(pageName + '-page');

    if (!targetPage) {
        const mainContent = document.getElementById('main-content');
        targetPage = document.createElement('div');
        targetPage.id = pageName + '-page';
        targetPage.className = 'page-content';
        mainContent.appendChild(targetPage);
    }

    // 如果頁面內容為空，載入外部 HTML
    if (!targetPage.hasAttribute('data-loaded')) {
        try {
            const response = await fetch(`pages/${pageName}.html`);
            if (response.ok) {
                const html = await response.text();
                targetPage.innerHTML = html;
                targetPage.setAttribute('data-loaded', 'true');

                // Execute scripts in loaded HTML
                const scripts = targetPage.querySelectorAll('script');
                scripts.forEach(script => {
                    if (script.type === 'text/markdown') {
                        // Skip markdown content scripts
                        return;
                    }
                    const newScript = document.createElement('script');
                    if (script.src) {
                        newScript.src = script.src;
                    } else {
                        newScript.textContent = script.textContent;
                    }
                    document.body.appendChild(newScript);
                });

                // Parse markdown if marked library is available
                if (typeof marked !== 'undefined') {
                    parseMarkdown(targetPage);
                }
            } else {
                targetPage.innerHTML = '<div class="bg-red-50 border border-red-200 rounded-lg p-4"><p class="text-red-800">頁面載入失敗</p></div>';
            }
        } catch (error) {
            console.error('Loading Failed:', error);
            targetPage.innerHTML = '<div class="bg-red-50 border border-red-200 rounded-lg p-4"><p class="text-red-800">頁面載入錯誤</p></div>';
        }
    }

    // 顯示頁面
    targetPage.classList.remove('hidden');

    // 更新導航按鈕樣式
    document.querySelectorAll('.nav-btn').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white');
        btn.classList.add('text-gray-300');
    });

    // Highlight active button (if event exists, from click; otherwise find by page name)
    if (event && event.target) {
        const clickedBtn = event.target.closest('.nav-btn');
        if (clickedBtn) {
            clickedBtn.classList.add('bg-blue-600', 'text-white');
            clickedBtn.classList.remove('text-gray-300');
        }
    } else {
        // Find button by onclick attribute matching pageName
        const buttons = document.querySelectorAll('.nav-btn');
        buttons.forEach(btn => {
            if (btn.getAttribute('onclick') && btn.getAttribute('onclick').includes(`'${pageName}'`)) {
                btn.classList.add('bg-blue-600', 'text-white');
                btn.classList.remove('text-gray-300');
            }
        });
    }

    // 更新頁面標題
    const titles = {
        'home': 'Overview',
        'downsampling': 'Dimensionality Reduction Analysis'
    };
    document.getElementById('page-title').textContent = titles[pageName] || pageName;
}
async function apiRequest(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json'
        }
    };
    
    if (data) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

// 載入資料集列表
async function loadDatasets() {
    try {
        const datasets = await apiRequest('/api/datasets');
        return datasets;
    } catch (error) {
        console.error('Failed to load datasets:', error);
        return null;
    }
}

// 執行分析
async function runAnalysis(analysisType, params) {
    try {
        const result = await apiRequest('/api/analyze', 'POST', {
            type: analysisType,
            params: params
        });
        return result;
    } catch (error) {
        console.error('Analysis failed:', error);
        throw error;
    }
}

// 顯示載入中狀態
function showLoading(elementId, message = '處理中...') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="flex items-center justify-center p-8">
                <svg class="animate-spin h-8 w-8 text-blue-500 mr-3" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span class="text-gray-600">${message}</span>
            </div>
        `;
    }
}

// 顯示錯誤訊息
function showError(elementId, message) {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = `
            <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                <div class="flex items-center">
                    <svg class="w-5 h-5 text-red-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <span class="text-red-800">${message}</span>
                </div>
            </div>
        `;
    }
}

// 初始化
window.addEventListener('DOMContentLoaded', () => {
    // 選中首頁按鈕
    document.querySelector('.nav-btn').classList.add('bg-blue-600', 'text-white');

    // 載入首頁
    loadPage('home');

    // 載入資料集列表 (optional - only works with Flask backend)
    loadDatasets().then(datasets => {
        if (datasets) {
            console.log('Datasets loaded:', datasets);
        }
    }).catch(err => {
        console.log('API not available (Flask server not running):', err.message);
    });
});
