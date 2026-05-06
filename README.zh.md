# FinSkills — 金融分析技能集

[English](README.md) | [中文](README.zh.md)

一套面向金融投资分析的 Claude Skills 集合，覆盖美股和 A 股两大市场，提供从价值筛选到组合构建、风险诊断和机构级文档的全流程分析能力。

> 💡 **探索更多技能**：FinSkills 是更广泛的 [OpenSkills](https://github.com/Geeksfino/openskills.git) 生态系统的一部分——一个涵盖多个领域和用例的全面开源 Claude Skills 集合。欢迎访问以了解更多专业化的 AI 能力！

## 概述

FinSkills 提供 30 个专业技能（15 个美股技能，15 个 A 股技能），旨在通过系统化、数据驱动的分析帮助投资者和分析师做出明智决策。每个技能遵循一致的架构，采用渐进式加载设计以优化上下文使用。

技能按三个分析层次及数据工具层组织：

| 层次 | 技能 | 目的 |
|------|------|------|
| **发现与筛选** | 低估值筛选、董监高分析、情绪偏差、小盘成长、量化因子、ESG筛选 | 寻找投资候选 |
| **深度分析** | 高股息策略、科技估值、行业轮动、财务报表分析、事件驱动 | 评估特定机会 |
| **组合与文档** | 收益优化器、组合健康诊断、适当性报告 | 构建、监控和记录 |
| **数据工具** | 金融数据工具包 | 实时市场数据获取和定量计算 |

每个分析技能可以借助**金融数据工具包**——一个提供实时市场数据和定量计算的伴生技能。当分析技能需要真实数据时，它会按名称引用工具包；LLM 在上下文中同时看到两个技能，会自动调用工具包。

## 相关项目

**OpenSkills** — 一个全面的开源 Claude Skills 集合，涵盖多个领域和用例。如果您想探索除金融分析之外的更多技能，请访问 [OpenSkills 仓库](https://github.com/Geeksfino/openskills.git)，了解各种专业化的 AI 能力和工作流程。

## 目录结构

```
finskills/
├── US-market/                          # 美股市场技能（英文）
│   ├── undervalued-stock-screener/     # 价值筛选
│   ├── insider-trading-analyzer/       # 内部交易分析
│   ├── sentiment-reality-gap/          # 逆向分析
│   ├── dividend-aristocrat-calculator/ # 收入投资
│   ├── tech-hype-vs-fundamentals/      # 科技估值
│   ├── sector-rotation-detector/       # 宏观/行业策略
│   ├── small-cap-growth-identifier/    # 小盘发现
│   ├── risk-adjusted-return-optimizer/ # 组合构建
│   ├── portfolio-health-check/         # 组合诊断
│   ├── suitability-report-generator/   # 投资文档
│   ├── financial-statement-analyzer/   # 财务深度分析
│   ├── event-driven-detector/          # 特殊情况
│   ├── quant-factor-screener/          # 多因子筛选
│   ├── esg-screener/                   # ESG分析
│   └── findata-toolkit/               # 📦 数据工具包（脚本 + 配置）
│       ├── SKILL.md                   # 工具包技能定义
│       ├── requirements.txt           # Python 依赖
│       ├── config/data_sources.yaml   # 数据源配置
│       └── scripts/                   # 自包含脚本
│           ├── common/               # 共享工具
│           ├── stock_data.py         # yfinance: 行情、指标、筛选
│           ├── sec_edgar.py          # SEC文件与内部交易
│           ├── financial_calc.py     # 杜邦、Z/M/F评分
│           ├── portfolio_analytics.py # VaR、压力测试、健康评分
│           ├── factor_screener.py    # 多因子打分引擎
│           └── macro_data.py         # FRED宏观指标
├── China-market/                       # A股市场技能（中文）
│   ├── undervalued-stock-screener/
│   ├── insider-trading-analyzer/
│   ├── sentiment-reality-gap/
│   ├── high-dividend-strategy/
│   ├── tech-hype-vs-fundamentals/
│   ├── sector-rotation-detector/
│   ├── small-cap-growth-identifier/
│   ├── risk-adjusted-return-optimizer/
│   ├── portfolio-health-check/         # 组合健康诊断
│   ├── suitability-report-generator/   # 适当性报告
│   ├── financial-statement-analyzer/   # 财务深度分析
│   ├── event-driven-detector/          # 事件驱动
│   ├── quant-factor-screener/          # 量化因子
│   ├── esg-screener/                   # ESG筛选
│   └── findata-toolkit/               # 📦 数据工具包（脚本 + 配置）
│       ├── SKILL.md                   # 工具包技能定义
│       ├── requirements.txt           # Python 依赖
│       ├── config/data_sources.yaml   # 数据源配置
│       └── scripts/                   # 自包含脚本
│           ├── common/               # 共享工具
│           ├── stock_data.py         # AKShare: 行情、指标、筛选
│           └── macro_data.py         # 宏观数据（LPR、PMI、CPI、M2）
├── README.md                           # 英文版本
└── README.zh.md                        # 本文件（中文版本）
```

## 技能一览

### US-market（美股 · 英文）

| # | 技能名称 | 说明 | 目录 |
|---|---------|------|------|
| 1 | **Undervalued Stock Screener** | 使用 P/E、P/B、增长率和 ROIC 等指标筛选基本面强劲但被低估的公司 | [US-market/undervalued-stock-screener/](US-market/undervalued-stock-screener/) |
| 2 | **Insider Trading Analyzer** | 分析内部交易模式（Form 4 文件）以识别管理层信心信号 | [US-market/insider-trading-analyzer/](US-market/insider-trading-analyzer/) |
| 3 | **Sentiment-Reality Gap** | 识别市场情绪与基本面背离的逆向投资机会 | [US-market/sentiment-reality-gap/](US-market/sentiment-reality-gap/) |
| 4 | **Dividend Aristocrat Calculator** | 评估股息贵族（连续 25 年以上增长）的收入可靠性和总回报 | [US-market/dividend-aristocrat-calculator/](US-market/dividend-aristocrat-calculator/) |
| 5 | **Tech Hype vs Fundamentals** | 使用增长-估值框架区分科技股炒作与基本面价值 | [US-market/tech-hype-vs-fundamentals/](US-market/tech-hype-vs-fundamentals/) |
| 6 | **Sector Rotation Detector** | 基于宏观经济指标（利率、通胀、GDP）检测行业轮动信号 | [US-market/sector-rotation-detector/](US-market/sector-rotation-detector/) |
| 7 | **Small-Cap Growth Identifier** | 发现被忽视的小盘成长股（市值 < 20 亿美元） | [US-market/small-cap-growth-identifier/](US-market/small-cap-growth-identifier/) |
| 8 | **Risk-Adjusted Return Optimizer** | 为特定风险偏好、时间跨度和资金规模构建优化投资组合 | [US-market/risk-adjusted-return-optimizer/](US-market/risk-adjusted-return-optimizer/) |
| 9 | **Portfolio Health Check** | 诊断现有组合风险：集中度、相关性聚集、因子偏移、压力测试、流动性 | [US-market/portfolio-health-check/](US-market/portfolio-health-check/) |
| 10 | **Suitability Report Generator** | 生成机构级投资文档：投资理由、风险披露、客户适当性评估 | [US-market/suitability-report-generator/](US-market/suitability-report-generator/) |
| 11 | **Financial Statement Analyzer** | 法证级单公司分析：杜邦分解、盈利质量、Z值、M值、营运资本 | [US-market/financial-statement-analyzer/](US-market/financial-statement-analyzer/) |
| 12 | **Event-Driven Detector** | 公司事件定价偏差：并购套利、分拆、回购、重组、指数调整 | [US-market/event-driven-detector/](US-market/event-driven-detector/) |
| 13 | **Quant Factor Screener** | 系统化多因子筛选（价值、动量、质量、低波、规模、成长），含因子择时和拥挤度分析 | [US-market/quant-factor-screener/](US-market/quant-factor-screener/) |
| 14 | **ESG Screener** | ESG评分、争议筛查、碳分析、治理质量、负责任投资整合 | [US-market/esg-screener/](US-market/esg-screener/) |
| 15 | **FinData Toolkit** 📦 | 美股实时数据：股票指标（yfinance）、SEC文件（EDGAR）、财务计算器、组合分析、因子筛选、宏观指标（FRED）。无需API密钥。 | [US-market/findata-toolkit/](US-market/findata-toolkit/) |

### China-market（A 股 · 中文）

| # | 技能名称 | 说明 | 目录 |
|---|---------|------|------|
| 1 | **低估值股票筛选器** | 扫描A股市场，筛选基本面强劲但被低估的上市公司 | [China-market/undervalued-stock-screener/](China-market/undervalued-stock-screener/) |
| 2 | **董监高增减持分析器** | 分析董监高及重要股东增减持行为，识别管理层信心信号 | [China-market/insider-trading-analyzer/](China-market/insider-trading-analyzer/) |
| 3 | **市场情绪与基本面偏差分析** | 识别被过度看空但基本面稳健的逆向投资机会 | [China-market/sentiment-reality-gap/](China-market/sentiment-reality-gap/) |
| 4 | **高股息策略分析器** | 评估A股高股息股票的分红可持续性与长期回报 | [China-market/high-dividend-strategy/](China-market/high-dividend-strategy/) |
| 5 | **科技股炒作vs基本面分析** | 区分A股科技公司的概念炒作与基本面支撑 | [China-market/tech-hype-vs-fundamentals/](China-market/tech-hype-vs-fundamentals/) |
| 6 | **行业轮动信号探测器** | 通过宏观经济指标识别A股行业轮动机会 | [China-market/sector-rotation-detector/](China-market/sector-rotation-detector/) |
| 7 | **小盘成长股发现器** | 发现被市场忽视的小市值高成长A股公司（20-200 亿元市值） | [China-market/small-cap-growth-identifier/](China-market/small-cap-growth-identifier/) |
| 8 | **风险调整收益优化器** | 为中国投资者构建风险调整后收益最优的投资组合 | [China-market/risk-adjusted-return-optimizer/](China-market/risk-adjusted-return-optimizer/) |
| 9 | **组合健康诊断** | 诊断现有A股组合：集中度、相关性（白酒聚集、新能源产业链共振等）、涨跌停流动性风险、A股特有压力测试 | [China-market/portfolio-health-check/](China-market/portfolio-health-check/) |
| 10 | **投资适当性报告生成器** | 符合证监会/协会适当性管理框架：科创板/北交所适格投资者验证、投资者风险等级匹配 | [China-market/suitability-report-generator/](China-market/suitability-report-generator/) |
| 11 | **财务报表深度分析** | A股法证财务分析：关联交易、政府补助依赖、在建工程不转固、商誉减值风险、中国会计准则特有红灯 | [China-market/financial-statement-analyzer/](China-market/financial-statement-analyzer/) |
| 12 | **事件驱动机会识别器** | A股公司事件分析：资产注入、国企改革、分拆上市、回购增持、指数调整、限售股解禁 | [China-market/event-driven-detector/](China-market/event-driven-detector/) |
| 13 | **量化因子筛选器** | A股多因子筛选，含中国特色因子（换手率、北向资金），基于PMI/社融数据的因子择时 | [China-market/quant-factor-screener/](China-market/quant-factor-screener/) |
| 14 | **ESG筛选器** | 中国特色ESG分析：双碳目标、共同富裕框架、证监会ESG披露要求 | [China-market/esg-screener/](China-market/esg-screener/) |
| 15 | **金融数据工具包** 📦 | A股实时数据：行情指标（AKShare）、董监高增减持、北向资金、宏观数据（LPR、PMI、CPI、M2）。无需API密钥。 | [China-market/findata-toolkit-cn/](China-market/findata-toolkit-cn/) |

## 技能架构

每个技能遵循统一的三层架构：

```
skill-name/
├── SKILL.md                        # 主文件：触发条件、工作流程、核心指引
└── references/
    ├── xxx-methodology.md          # 详细方法论：计算公式、评分标准、行业基准
    └── output-template.md          # 报告模板：结构化输出格式
```

### 工具包技能

工具包技能封装可执行脚本和数据获取工具。它们是**自包含的**——每个工具包包含自己的 `requirements.txt`、配置和脚本：

```
findata-toolkit/
├── SKILL.md                        # 工具描述和使用示例
├── requirements.txt                # Python 依赖（pip install -r）
├── config/data_sources.yaml        # 数据源配置
├── LICENSE.txt
└── scripts/
    ├── common/                    # 共享工具（配置、输出助手）
    ├── stock_data.py              # 股票指标、筛选、行情
    ├── financial_calc.py          # 杜邦、Z/M/F评分、盈利质量
    └── ...                        # 其他领域脚本
```

### 分析技能如何使用工具包

分析技能（如*低估值股票筛选器*）在其 `SKILL.md` 中按名称引用工具包：

> 如需实时市场数据支撑分析，请使用**金融数据工具包**技能（`findata-toolkit-cn`）。

LLM 在系统提示中同时看到两个技能。当分析技能需要实时数据时，LLM 识别工具包引用并自动调用其脚本。无需特殊连线——耦合通过技能描述中的**自然语言**实现。

### 渐进式加载（Progressive Disclosure）

- **始终在上下文中**：仅 `SKILL.md` 的 YAML frontmatter（`name`、`description`），用于判断是否触发
- **触发时加载**：`SKILL.md` 正文 — 工作流程、核心指引
- **按需加载**：`references/` 目录下的详细方法论和模板 — 仅在执行分析时读取

这种设计确保在不需要时节省上下文窗口，在需要时提供完整的分析框架。

## 数据来源

所有主要数据源**免费**，**无需API密钥**：

| 来源 | 市场 | API密钥 | 提供内容 |
|------|------|---------|----------|
| **yfinance** | 美股 | 无需 | 股票报价、财务数据、历史行情、分析师数据 |
| **SEC EDGAR** | 美股 | 无需 | 内部交易（Form 4）、公司文件（10-K, 10-Q） |
| **FRED** | 美股 | 无需 | 宏观指标（利率、CPI、GDP、就业） |
| **AKShare** | A股 | 无需 | A股数据、宏观指标、北向资金 |

## 市场差异化设计

China-market 技能并非简单翻译 US-market 版本，而是针对 A 股市场特性进行了全面重写：

| 维度 | US-market | China-market |
|------|-----------|-------------|
| **语言** | English | 中文 |
| **市场结构** | NYSE/NASDAQ、SEC 监管 | 沪深交易所/北交所、证监会监管 |
| **行业分类** | GICS | 申万行业分类 |
| **内部交易** | SEC Form 4 | 董监高增减持公告 |
| **分红** | 季度分红、Dividend Aristocrats | 年度分红、中证红利指数 |
| **税制** | 资本利得税、分红税 | 无资本利得税、分红税与持有期挂钩 |
| **会计准则** | US GAAP | 企业会计准则（CAS） |
| **估值特点** | 成熟市场估值中枢 | A股溢价、政策溢价、壳价值（下降中） |
| **政策影响** | 联储政策、监管 | 国务院、央行、证监会、产业政策（权重极高） |
| **资金结构** | 机构主导 | 散户交易占比高、北向资金边际影响大 |
| **投资工具** | ETFs、Options、REITs | ETF、可转债、公募 REITs、QDII |
| **交易机制** | T+0、无涨跌停限制 | T+1、10%/20% 涨跌停限制 |
| **ESG框架** | TCFD、SEC气候披露、股东维权 | 双碳目标、共同富裕、证监会ESG披露要求 |
| **适当性监管** | SEC Reg BI、FINRA Rule 2111 | 证监会投资者适当性管理办法、适格投资者门槛 |
| **公司事件** | 并购、分拆、回购 | 资产注入、国企改革、借壳上市（减少中） |
| **因子溢价** | 标准学术因子 | 低波动异象极显著、换手率因子独特有效 |

## 使用示例

### US-market 触发示例（英文）

- *"Screen for undervalued stocks in the technology sector"*
- *"Analyze insider buying patterns in healthcare companies"*
- *"Build me a $100K moderate-risk portfolio for a 10-year horizon"*
- *"Identify tech stocks where hype exceeds fundamentals"*
- *"What sectors should outperform based on current macro indicators?"*
- *"Find small-cap growth stocks under $2B with strong fundamentals"*
- *"Calculate total return for dividend aristocrats with DRIP"*
- *"Identify stocks where sentiment is overly negative but fundamentals are strong"*
- *"Review my portfolio for hidden risks and concentration issues"*
- *"Generate a suitability report for this portfolio recommendation"*
- *"Do a deep dive into Apple's financial statements"*
- *"What merger arbitrage opportunities are available right now?"*
- *"Screen stocks using a multi-factor model with value and quality"*
- *"Find the best ESG-rated companies in the S&P 500"*

### China-market 触发示例（中文）

- *"帮我筛选 A 股低估值股票"*
- *"分析最近有哪些公司董事长在大量增持"*
- *"当前宏观环境下应该超配哪些行业？"*
- *"用 30 万帮我构建一个稳健型投资组合"*
- *"科创板哪些公司估值泡沫最严重？"*
- *"帮我找几只被市场错杀的 A 股"*
- *"A 股有哪些高股息但分红可持续的标的？"*
- *"推荐几只市值小但增长快的专精特新公司"*
- *"帮我诊断一下我的持仓有什么风险"*
- *"为这个投资建议生成一份适当性报告"*
- *"深度分析一下贵州茅台的财务报表"*
- *"最近有哪些A股并购重组机会？"*
- *"用多因子模型帮我筛选A股"*
- *"帮我找ESG评分最高的沪深300成分股"*

## 安装与使用

这些技能专为 Claude（Anthropic 的 AI 助手）设计。使用方法：

1. **安装技能**：将技能目录放置在您的 Claude 技能目录中（通常为 `$CODEX_HOME/skills/` 或类似路径）。每个技能自包含，可以单独安装。
2. **安装工具包依赖**：如需实时数据能力，安装工具包的 Python 依赖：
   ```bash
   # 美股市场工具包
   cd US-market/findata-toolkit && pip install -r requirements.txt

   # A股市场工具包
   cd China-market/findata-toolkit-cn && pip install -r requirements.txt
   ```
3. **自然触发**：使用与技能描述匹配的自然语言查询
4. **遵循工作流程**：每个技能将引导您完成其分析工作流程
5. **查阅参考资料**：详细方法论可在 `references/` 子目录中找到

## 贡献指南

欢迎贡献！添加新技能时请遵循：

1. 遵循三层架构（`SKILL.md` + `references/`）
2. 使用渐进式加载原则
3. 包含全面的方法论文档
4. 提供结构化输出模板
5. 添加适当的免责声明
6. China-market 技能须针对 A 股市场特性全面重写（而非翻译）
7. 保持技能自包含——所有资源必须位于技能目录内

## 免责声明

> **重要提示**：本技能集仅供信息参考和教育目的，不构成任何投资建议、推荐或买卖任何证券的要约。所有分析基于公开数据和模型假设，可能存在错误或遗漏。过往业绩不代表未来表现。投资有风险，入市需谨慎。在做出任何投资决策前，请咨询合格的投资顾问。

## 许可证

Copyright 2025 FinoGeeks Technology Ltd

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
