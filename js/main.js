document.addEventListener('DOMContentLoaded', function() {
    initScale();
    initDateTime();
    initMap();
    initAnnouncements();
    initFundFlow();
    initCharts();
});

// 0. 全屏填充缩放
function initScale() {
    const app = document.getElementById('app');

    function resize() {
        const scaleX = window.innerWidth / 1920;
        const scaleY = window.innerHeight / 1080;
        app.style.transform = `scale(${scaleX}, ${scaleY})`;
    }

    resize();
    window.addEventListener('resize', resize);
}

// 1. 日期时间显示
function initDateTime() {
    const dateTimeEl = document.getElementById('dateTime');
    function update() {
        const now = new Date();
        dateTimeEl.textContent = now.toLocaleString('zh-CN', { hour12: false });
    }
    update();
    setInterval(update, 1000);
}

// 2. 地图初始化 (Leaflet + GeoJSON)
function initMap() {
    // 修复 Leaflet 默认图标路径
    delete L.Icon.Default.prototype._getIconUrl;
    L.Icon.Default.mergeOptions({
        iconRetinaUrl: 'lib/images/marker-icon-2x.png',
        iconUrl: 'lib/images/marker-icon.png',
        shadowUrl: 'lib/images/marker-shadow.png',
    });

    // 巴马县中心坐标
    const center = [24.116, 107.203];
    const map = L.map('map', {
        center: center,
        zoom: 11,
        zoomControl: false,
        attributionControl: false,
        dragging: false,          // 禁止拖拽
        scrollWheelZoom: false,   // 禁止滚轮缩放
        doubleClickZoom: false,   // 禁止双击缩放
        touchZoom: false,         // 禁止触摸缩放
        boxZoom: false,           // 禁止框选缩放
        keyboard: false           // 禁止键盘操作
    });

    // 加载暗色瓦片底图（离线）
    L.tileLayer('assets/tiles/{z}/{x}/{y}.png', {
        maxZoom: 13,
        minZoom: 10,
        errorTileUrl: ''
    }).addTo(map);

    // 叠加巴马县 GeoJSON 边界（发光效果）
    fetch('data/bama.json')
        .then(response => response.json())
        .then(data => {
            // 绘制广西地图边界 - 科技感样式
            L.geoJSON(data, {
                style: function(feature) {
                    return {
                        color: '#00d2ff',       // 边框青色
                        weight: 1.5,
                        opacity: 0.8,
                        fillColor: '#0a192f',   // 填充深蓝
                        fillOpacity: 0.15       // 低透明度让瓦片透出
                    };
                },
                onEachFeature: function(feature, layer) {
                    // 鼠标悬停高亮效果
                    layer.on({
                        mouseover: function(e) {
                            e.target.setStyle({
                                weight: 2,
                                color: '#ffd700', // 高亮金色
                                fillOpacity: 0.3,
                                fillColor: '#112240'
                            });
                        },
                        mouseout: function(e) {
                            e.target.setStyle({
                                color: '#00d2ff',
                                weight: 1.5,
                                fillOpacity: 0.15,
                                fillColor: '#0a192f'
                            });
                        }
                    });
                }
            }).addTo(map);

            // 添加虚拟村庄标记
            addVillageMarkers(map);
        })
        .catch(error => {
            console.error('Error loading GeoJSON:', error);
            addVillageMarkers(map);
        });
}

function addVillageMarkers(map) {
    // 自定义脉冲图标
    const villageIcon = L.divIcon({
        className: 'custom-village-icon',
        html: `
            <div style="position:relative;width:14px;height:14px;">
                <div style="position:absolute;width:100%;height:100%;background:#ffd700;border-radius:50%;box-shadow:0 0 10px #ffd700;"></div>
                <div style="position:absolute;top:-50%;left:-50%;width:200%;height:200%;border:1px solid #ffd700;border-radius:50%;opacity:0;animation:pulse 2s infinite;"></div>
            </div>
            <style>
                @keyframes pulse {
                    0% { transform: scale(0.5); opacity: 1; }
                    100% { transform: scale(1.5); opacity: 0; }
                }
            </style>
        `,
        iconSize: [14, 14],
        iconAnchor: [7, 7]
    });

    // 虚拟村庄坐标（分布在巴马县域内）
    const villageMarkers = [
        { name: "甲县", lat: 24.14, lng: 107.26, assets: 12345, income: 890, type: 'county' },
        { name: "A村", lat: 24.28, lng: 107.10, assets: 5000, income: 200 },
        { name: "B村", lat: 24.05, lng: 107.40, assets: 4500, income: 180 },
        { name: "C村", lat: 23.92, lng: 107.18, assets: 6000, income: 250 },
        { name: "D村", lat: 24.22, lng: 107.45, assets: 3000, income: 120 },
        { name: "E村", lat: 24.35, lng: 107.30, assets: 5500, income: 220 },
        { name: "F村", lat: 23.98, lng: 107.05, assets: 4200, income: 160 },
        { name: "G村", lat: 24.18, lng: 107.00, assets: 3800, income: 140 }
    ];

    villageMarkers.forEach(village => {
        const marker = L.marker([village.lat, village.lng], { icon: villageIcon }).addTo(map);

        // 自定义科技感弹窗内容
        const popupContent = `
            <div class="popup-header">
                <span class="popup-title">${village.name}</span>
                <span class="popup-status">正常</span>
            </div>
            <div class="popup-body">
                <div class="popup-row">
                    <span class="popup-label">总资产</span>
                    <span class="popup-value highlight">${village.assets.toLocaleString()} <span style="font-size:10px">万元</span></span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">集体收入</span>
                    <span class="popup-value">${village.income.toLocaleString()} <span style="font-size:10px">万元</span></span>
                </div>
                <div class="popup-row">
                    <span class="popup-label">数据更新</span>
                    <span class="popup-value">2023-12-31</span>
                </div>
            </div>
        `;
        
        marker.bindPopup(popupContent, {
            className: 'custom-popup',
            closeButton: false,
            minWidth: 200
        });

        // 永久显示名称标签
        const labelClass = village.type === 'county' ? 'village-label county-label' : 'village-label';
        marker.bindTooltip(village.name, {
            permanent: true,
            direction: 'top',
            offset: [0, -10],
            className: labelClass
        });
    });
}

// 3. 公告展示
function initAnnouncements() {
    const listEl = document.getElementById('announcementList');
    announcements.forEach(item => {
        const div = document.createElement('div');
        div.className = 'announcement-item';
        div.innerHTML = `
            <div class="announcement-title">${item.title}</div>
            <div class="announcement-date">${item.date}</div>
        `;
        div.onclick = () => showModal(item.title, item.content);
        listEl.appendChild(div);
    });
}

// 4. 资金去向 (滚动列表)
function initFundFlow() {
    const listEl = document.getElementById('fundList');

    // 填充数据
    fundFlows.forEach(item => {
        const li = document.createElement('li');
        li.className = 'fund-item';
        const amountClass = item.amount.startsWith('+') ? 'fund-amount' : 'fund-amount negative';
        li.innerHTML = `
            <span style="color:#ccc;font-size:12px;">${item.date}</span>
            <span style="flex:1;margin-left:10px;color:#fff;">${item.desc}</span>
            <span class="${amountClass}">${item.amount}</span>
        `;
        listEl.appendChild(li);
    });

    // 复制一份用于无缝滚动
    const clone = listEl.innerHTML;
    listEl.innerHTML += clone;
}

// 5. 图表初始化 (ECharts)
function initCharts() {
    // 资产构成饼图
    const assetChart = echarts.init(document.getElementById('assetChart'));
    const assetOption = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)',
            backgroundColor: 'rgba(10, 20, 40, 0.9)',
            borderColor: '#00d2ff',
            textStyle: { color: '#fff' }
        },
        legend: {
            bottom: '0%',
            left: 'center',
            textStyle: { color: '#ccc', fontSize: 10 },
            itemWidth: 10,
            itemHeight: 10
        },
        color: ['#00d2ff', '#ffd700', '#00ff88'],
        series: [
            {
                name: '资产构成',
                type: 'pie',
                radius: ['40%', '60%'],
                center: ['50%', '40%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 5,
                    borderColor: '#0a192f',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: 14,
                        fontWeight: 'bold',
                        color: '#fff'
                    }
                },
                labelLine: { show: false },
                data: assetData
            }
        ]
    };
    assetChart.setOption(assetOption);

    // 年度收支柱状图
    const incomeChart = echarts.init(document.getElementById('incomeChart'));
    const incomeOption = {
        tooltip: {
            trigger: 'axis',
            axisPointer: { type: 'shadow' },
            backgroundColor: 'rgba(10, 20, 40, 0.9)',
            borderColor: '#00d2ff',
            textStyle: { color: '#fff' }
        },
        legend: {
            top: '0%',
            textStyle: { color: '#ccc', fontSize: 10 },
            itemWidth: 10,
            itemHeight: 10
        },
        color: ['#00d2ff', '#ff4444'],
        grid: {
            left: '3%',
            right: '4%',
            bottom: '5%',
            top: '15%',
            containLabel: true
        },
        xAxis: [{
            type: 'category',
            data: incomeData.years,
            axisLabel: { color: '#ccc', fontSize: 10 },
            axisLine: { lineStyle: { color: '#333' } }
        }],
        yAxis: [{
            type: 'value',
            axisLabel: { color: '#ccc', fontSize: 10 },
            splitLine: { lineStyle: { color: 'rgba(255,255,255,0.05)' } },
            axisLine: { show: false }
        }],
        series: [
            {
                name: '收入',
                type: 'bar',
                barWidth: '20%',
                itemStyle: { borderRadius: [3, 3, 0, 0] },
                data: incomeData.income
            },
            {
                name: '支出',
                type: 'bar',
                barWidth: '20%',
                itemStyle: { borderRadius: [3, 3, 0, 0] },
                data: incomeData.expense
            }
        ]
    };
    incomeChart.setOption(incomeOption);

    // 窗口大小改变时重绘图表
    window.addEventListener('resize', function() {
        assetChart.resize();
        incomeChart.resize();
    });
}

// 模态框控制
function showModal(title, content) {
    const modal = document.getElementById("modal");
    document.getElementById("modalTitle").textContent = title;
    document.getElementById("modalBody").innerHTML = content;
    modal.style.display = "block";
}

document.querySelector('.close').onclick = function() {
    document.getElementById("modal").style.display = "none";
};

window.onclick = function(event) {
    const modal = document.getElementById("modal");
    if (event.target === modal) {
        modal.style.display = "none";
    }
};
