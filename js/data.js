// ====== 公告数据 ======
const announcements = [
    {
        title: "关于加强农村集体三资管理的通知",
        date: "2024-12-15",
        content: `<p><b>各村集体经济组织：</b></p>
        <p>根据《农村集体经济组织财务制度》和上级有关文件精神，为进一步规范农村集体资金、资产、资源（以下简称"三资"）管理，保障农民群众合法权益，现将有关事项通知如下：</p>
        <p><b>一、加强资金管理。</b>严格执行财务收支审批制度，大额资金使用需经村民代表大会或村民会议讨论决定。</p>
        <p><b>二、规范资产处置。</b>集体资产的出租、出借、转让等须经民主议定程序，实行公开竞价。</p>
        <p><b>三、合理利用资源。</b>集体土地、山林、水面等资源的承包经营须签订规范合同，明确双方权利义务。</p>
        <p><b>四、强化公开监督。</b>三资管理情况须定期向全体村民公开，接受群众监督。</p>`
    },
    {
        title: "甲县2025年度集体收益分配方案公示",
        date: "2025-12-10",
        content: `<p><b>分配依据：</b>根据《农村集体经济组织收益分配管理办法》和村民代表大会决议</p>
        <p><b>2025年度集体总收益：</b>1,285,600 元</p>
        <p><b>收益来源构成：</b></p>
        <table style="width:100%;border-collapse:collapse;color:#ccc;">
            <tr style="border-bottom:1px solid #333;"><th style="text-align:left;padding:5px;">收入项目</th><th>金额(元)</th><th>占比</th></tr>
            <tr style="border-bottom:1px solid #222;"><td style="padding:5px;">土地流转租金</td><td style="text-align:center;">450,000</td><td style="text-align:center;">35.0%</td></tr>
            <tr style="border-bottom:1px solid #222;"><td style="padding:5px;">集体产业分红</td><td style="text-align:center;">320,000</td><td style="text-align:center;">24.9%</td></tr>
            <tr style="border-bottom:1px solid #222;"><td style="padding:5px;">上级财政补助</td><td style="text-align:center;">280,000</td><td style="text-align:center;">21.8%</td></tr>
            <tr style="border-bottom:1px solid #222;"><td style="padding:5px;">资产租赁收入</td><td style="text-align:center;">150,000</td><td style="text-align:center;">11.7%</td></tr>
            <tr style="border-bottom:1px solid #222;"><td style="padding:5px;">其他经营收入</td><td style="text-align:center;">85,600</td><td style="text-align:center;">6.6%</td></tr>
            <tr><td style="padding:5px;"><b>合计</b></td><td style="text-align:center;"><b>1,285,600</b></td><td style="text-align:center;"><b>100%</b></td></tr>
        </table>

        <p><b>分配方案：</b></p>
        <ul style="margin-left:20px;color:#ccc;">
            <li><b>公积金提取：</b>20%（257,120元）用于集体经济发展和风险储备</li>
            <li><b>公益金提取：</b>15%（192,840元）用于村内公益事业</li>
            <li><b>村民分红：</b>65%（835,640元）按股权份额分配</li>
        </ul>

        <p><b>分红标准：</b></p>
        <ul style="margin-left:20px;color:#ccc;">
            <li>总股数：4,178.2股</li>
            <li>每股分红金额：200元</li>
            <li>惠及农户：312户，1,245人</li>
        </ul>

        <p><b>发放时间：</b>2025年12月25日前完成</p>
        <p><b>公示期：</b>2025年12月10日至12月17日</p>`
    },
    {
        title: "2025年度财务审计报告公示",
        date: "2025-11-20",
        content: `<p><b>审计范围：</b>甲县所辖A村、B村、C村、D村、E村、F村、G村2025年度集体财务收支</p>
        <p><b>审计结论：</b></p>
        <p>经审计，各村集体经济组织2025年度财务收支基本合规，账目清晰。主要审计结果如下：</p>
        <ul style="margin-left:20px;color:#ccc;">
            <li>集体总收入 89,456 万元，同比增长 8.3%</li>
            <li>集体总支出 76,230 万元，同比增长 5.1%</li>
            <li>年末集体净资产 1,234,567 万元</li>
            <li>各项专项资金使用合规，无重大违纪违规问题</li>
        </ul>`
    },
    {
        title: "关于土地流转收益分配的通知",
        date: "2025-11-05",
        content: `<p>经甲县村民代表大会讨论通过，现将2025年度土地流转收益分配方案公示如下：</p>
        <p><b>流转面积：</b>1,200亩</p>
        <p><b>流转收益：</b>总计96万元</p>
        <p><b>分配方案：</b></p>
        <ul style="margin-left:20px;color:#ccc;">
            <li>村集体留存 30%（28.8万元）用于公共设施维护</li>
            <li>村民分红 70%（67.2万元）按人口均等分配</li>
            <li>惠及村民 1,680 人，人均分红 400 元</li>
        </ul>
        <p><b>发放时间：</b>2025年12月底前完成</p>`
    },
    {
        title: "村集体资产年度清查结果公示",
        date: "2025-10-28",
        content: `<p>根据上级要求，甲县已完成2025年度集体资产清查工作，结果如下：</p>
        <p><b>资产总额：</b>1,234,567 万元</p>
        <p><b>其中：</b></p>
        <ul style="margin-left:20px;color:#ccc;">
            <li>经营性资产：1,048 万元（厂房、设备、门面等）</li>
            <li>非经营性资产：735 万元（学校、卫生所、文化活动中心等）</li>
            <li>资源性资产：580 万元（耕地、林地、水域等）</li>
        </ul>
        <p><b>新增资产：</b>村文化广场1处（投资35万元），道路硬化2公里（投资48万元）</p>`
    },
    {
        title: "B村集体采购公示（路灯工程）",
        date: "2025-10-15",
        content: `<p><b>项目名称：</b>B村主干道太阳能路灯安装工程</p>
        <p><b>项目预算：</b>18.5 万元</p>
        <p><b>采购方式：</b>公开招标</p>
        <p><b>中标单位：</b>XX照明工程有限公司</p>
        <p><b>工程内容：</b>安装太阳能路灯50盏，覆盖主干道全长2.5公里</p>
        <p><b>工期：</b>30天</p>
        <p><b>公示期：</b>2025年10月15日至10月22日</p>`
    }
];

// ====== 资金去向数据 ======
const fundFlows = [
    { type: "收入", desc: "土地租金收入", amount: "+50,000", date: "12-01" },
    { type: "支出", desc: "道路维修工程款", amount: "-20,000", date: "12-03" },
    { type: "收入", desc: "上级补助资金", amount: "+100,000", date: "12-05" },
    { type: "支出", desc: "办公用品采购", amount: "-5,000", date: "12-08" },
    { type: "支出", desc: "环境整治人工费", amount: "-8,000", date: "12-10" },
    { type: "收入", desc: "利息收入", amount: "+1,200", date: "12-12" },
    { type: "支出", desc: "水电费缴纳", amount: "-3,000", date: "12-15" },
    { type: "收入", desc: "资产租赁收入", amount: "+15,000", date: "12-18" },
    { type: "支出", desc: "太阳能路灯工程", amount: "-185,000", date: "12-20" },
    { type: "收入", desc: "产业分红收入", amount: "+32,000", date: "12-22" },
    { type: "支出", desc: "扶贫慰问支出", amount: "-12,000", date: "12-25" },
    { type: "收入", desc: "集体鱼塘承包费", amount: "+28,000", date: "12-28" }
];

// ====== 资产构成数据 ======
const expenseData = [
    { value: 285, name: '基础设施' },      // 道路、水利、公共设施
    { value: 192, name: '公益事业' },      // 教育、文化、卫生
    { value: 153, name: '管理费用' },      // 办公、人员、差旅
    { value: 98, name: '生产投入' },       // 农业生产、产业扶持
    { value: 62, name: '社会保障' }        // 扶贫、慰问、补贴
];

// ====== 收支对比数据 ======
const incomeData = {
    years: ['2021', '2022', '2023', '2024', '2025'],
    income: [120, 132, 101, 134, 90],
    expense: [98, 102, 91, 114, 76]
};
