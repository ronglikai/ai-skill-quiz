"""
AI Skill 知识测试题库
基于《AI智能体开发工具知识包》内容设计
"""

QUESTIONS = [
    # ===== 第一部分：核心概念 =====
    {
        "id": 1,
        "category": "核心概念",
        "difficulty": "基础",
        "question": "请解释什么是Agent（智能体），它解决了大语言模型的什么问题？",
        "key_points": [
            "Agent是用户和大模型之间的中间人程序",
            "大模型只能一问一答，不能自己查资料、不能操作工具",
            "Agent能上网、查数据库、操作文件，把查到的结果塞进上下文给大模型分析",
            "Agent把需要智能判断的部分交给大模型，把可以程序固定实现的部分写成代码",
        ],
        "reference_answer": "Agent（智能体）是一个位于用户和大语言模型之间的中间人程序。由于大模型本身只能进行文字接龙式的一问一答，无法主动上网查资料或操作工具，Agent的作用就是弥补这个缺陷——它能上网、查数据库、操作文件系统，然后把获取的结果塞进上下文，让大模型基于这些真实信息来分析和回答。简单说，Agent把'需要智能判断的部分'交给大模型，把'可以用程序固定实现的部分'自己用代码完成。",
    },
    {
        "id": 2,
        "category": "核心概念",
        "difficulty": "基础",
        "question": "RAG（检索增强生成）是什么？它和直接问AI有什么区别？",
        "key_points": [
            "RAG全称Retrieval Augmented Generation，检索增强生成",
            "把私有文档/企业知识库存起来",
            "每次提问时先在文档里找最相关的段落",
            "把找到的段落塞进Context让大模型基于真实资料回答",
            "相当于给AI配了一个专属图书馆，基于真实资料而非记忆回答",
        ],
        "reference_answer": "RAG（Retrieval Augmented Generation，检索增强生成）是Agent的一种具体能力扩展。它的工作原理是：把你的私有文档、企业知识库预先存储起来，每次用户提问时，先在这些文档里检索最相关的段落，然后把找到的内容塞进上下文，让大模型基于这些真实资料来回答。与直接问AI的区别在于：直接问AI靠的是模型训练时学到的通用知识（可能过时或不准确），而RAG让AI基于你的真实文档回答，相当于给AI配了一个专属图书馆。",
    },
    {
        "id": 3,
        "category": "核心概念",
        "difficulty": "基础",
        "question": "MCP（模型上下文协议）是什么？请用一个生活中的类比来解释它的作用。",
        "key_points": [
            "MCP全称Model Context Protocol，模型上下文协议",
            "是AI工具的统一接口标准/连接规范",
            "类比USB接口标准——让不同设备都能通过统一接口连接",
            "定义了工具如何被Agent发现和调用的规范",
            "只要工具遵循MCP标准，任何支持MCP的Agent都能使用它",
        ],
        "reference_answer": "MCP（Model Context Protocol，模型上下文协议）是AI工具世界的统一接口标准。最好的类比是USB接口：在USB出现之前，鼠标、键盘、打印机各有各的接口标准，非常混乱。USB定义了统一的连接规范，所有设备只要遵循这个标准就能互相连接。MCP的作用完全一样——它定义了'AI工具如何被Agent发现和调用'的统一规范，只要一个工具实现了MCP协议，任何支持MCP的Agent都能直接使用它，无需针对每个工具单独开发连接方式。",
    },
    {
        "id": 4,
        "category": "核心概念",
        "difficulty": "基础",
        "question": "Skill（技能）是什么？它解决了哪些核心痛点？",
        "key_points": [
            "Skill是一个包含指令的文件夹，用来扩展AI代理的专业能力",
            "核心文件是SKILL.md，可选references/scripts/assets文件夹",
            "解决三大痛点：重复劳动（每次重新解释流程）、流程不稳定（每次结果不同）、知识无法共享（最佳实践只在个人prompt记录里）",
            "本质是把提示词换了个地方存起来，使流程可共享、可复用、可跨平台",
        ],
        "reference_answer": "Skill（技能）是一个包含指令的文件夹，用来扩展AI代理的专业能力。一个Skill包含必须的SKILL.md主说明文件，以及可选的references（参考文档）、scripts（脚本）、assets（素材）文件夹。它解决三大核心痛点：1）重复劳动——不用每次手动输入说明，AI自动调用；2）流程不稳定——让AI按固定步骤执行，结果可预测；3）知识无法共享——把最佳实践打包成文件，分享给同事、跨平台使用。",
    },
    # ===== 第二部分：Skill文件结构 =====
    {
        "id": 5,
        "category": "Skill文件结构",
        "difficulty": "重点",
        "question": "Skill的主文件命名有什么要求？文件夹命名又有什么规范？请说明正确和错误的例子。",
        "key_points": [
            "主文件必须命名为SKILL.md（全大写），大小写敏感",
            "skill.md、Skill.md、SKILL.MD都是错误的",
            "文件夹命名必须使用kebab-case（小写字母+短横线）",
            "不能有空格、大写字母、下划线",
            "正确示例：notion-project-setup；错误示例：Notion Project Setup、notion_project_setup",
            "文件夹内不能有README.md文件",
            "名称不能含claude或anthropic（系统保留）",
        ],
        "reference_answer": "Skill主文件必须命名为SKILL.md（全大写，大小写敏感），skill.md、Skill.md、SKILL.MD都会导致上传失败。文件夹命名必须使用kebab-case格式，即小写字母加短横线分隔，例如notion-project-setup是正确的，而Notion Project Setup（有空格和大写）、notion_project_setup（用了下划线）都是错误的。此外还有两条规则：文件夹内不能包含README.md文件（说明放在SKILL.md或references中），名称不能含有claude或anthropic这两个系统保留词。",
    },
    {
        "id": 6,
        "category": "Skill文件结构",
        "difficulty": "重点",
        "question": "请描述一个完整Skill文件夹的目录结构，并说明每个部分的作用。",
        "key_points": [
            "根目录是kebab-case命名的文件夹",
            "SKILL.md——必须有，主说明文件，包含技能名称、描述、执行步骤",
            "references/——可选，存放参考文档",
            "scripts/——可选，存放可执行脚本（Python、Bash等）",
            "assets/——可选，存放模板、图片等素材",
        ],
        "reference_answer": "一个完整的Skill文件夹结构如下：根目录用kebab-case命名（如my-skill-name/），其中包含：1）SKILL.md（必须）——主说明文件，包含技能的名称、描述、执行步骤等核心指令；2）references/（可选）——存放额外的参考文档，如规则说明、行业标准等；3）scripts/（可选）——存放可执行的脚本文件，如Python或Bash程序；4）assets/（可选）——存放模板、图片等素材资源。",
    },
    # ===== 第三部分：SKILL.md配置 =====
    {
        "id": 7,
        "category": "SKILL.md配置",
        "difficulty": "重点",
        "question": "SKILL.md的YAML frontmatter中，哪些字段是必填的？description字段应该怎么写才是最佳实践？",
        "key_points": [
            "必填字段：name和description",
            "name必须是kebab-case格式，且必须与文件夹名一致",
            "description推荐三段式结构：[做什么] + [何时使用] + [关键能力]",
            "description不是简介，是精确的触发规则",
            "Claude完全依赖description来判断是否调用该Skill",
            "太模糊会导致误触发，太窄会导致漏触发",
            "应在description中放入关键触发词",
        ],
        "reference_answer": "YAML frontmatter中，name和description是必填字段。name必须是kebab-case格式且与文件夹名完全一致。description是Skill最重要的字段——Claude完全依赖它来判断是否调用该Skill。最佳实践是使用三段式结构：[做什么]+[何时使用]+[关键能力]。例如：'分析每周营销活动数据，计算转化漏斗和效率指标，提供预算建议。当用户需要分析活动表现、计算ROI时使用。支持CSV数据输入，输出结构化报告。' 切记description不是简介而是精确的触发规则，太宽泛会误触发，太窄会漏触发。",
    },
    {
        "id": 8,
        "category": "实操排错",
        "difficulty": "重点",
        "question": """以下是一个Skill的YAML frontmatter，请找出其中的所有错误并说明如何修正：

```yaml
---
name: Weekly Report Generator
description: 生成周报
license: MIT
compatibility:
  - claude-ai
  - claude-code
metadata:
  author: 张三
  version: 1.0
---
```""",
        "key_points": [
            "name字段格式错误——必须用kebab-case（小写+短横线），不能有大写字母和空格",
            "正确写法应该是 weekly-report-generator",
            "description太模糊——只写了'生成周报'，Claude无法判断何时触发",
            "应该用三段式：做什么+何时使用+关键能力",
            "version建议用语义化版本如1.0.0",
        ],
        "reference_answer": "有两个关键错误：1）name字段 'Weekly Report Generator' 格式不对——必须使用kebab-case（全小写+短横线分隔），应改为 'weekly-report-generator'，且必须与文件夹名一致。2）description只写了'生成周报'太模糊——Claude完全依赖description来判断是否调用该Skill，太模糊会导致误触发或漏触发。应改为三段式，如：'根据本周工作内容生成结构化周报。当用户需要整理周报、汇总本周成果时使用。支持从任务列表和会议记录提取信息，输出Markdown格式周报。' 另外version建议用语义化版本1.0.0。",
    },
    # ===== 第四部分：Skill设计思维 =====
    {
        "id": 9,
        "category": "Skill设计思维",
        "difficulty": "重点",
        "question": "写Prompt（提示词）和写Skill有什么根本区别？请从时机、上下文、调整方式三个维度分析。",
        "key_points": [
            "时机：提示词是对话中实时写的，Skill是提前写好在未来某个不在场的上下文里读取",
            "上下文：写提示词时你清楚当前上下文有什么，写Skill时你不知道触发时上下文里还有什么",
            "调整方式：提示词可以看到回复不对立刻改，Skill没有人能实时纠正",
            "最大陷阱：提示词含糊没关系因为可以追问，Skill含糊意味着每次执行都会在含糊处出错",
            "核心总结：提示词可以模糊因为你在场，Skill必须精确因为你不在场",
        ],
        "reference_answer": "写Prompt和写Skill的区别是根本性的，体现在三个维度：1）时机——提示词是你在对话中实时写的，Claude立刻看到；Skill是提前写好的，Claude在未来某个你不在场的上下文里读取。2）上下文——写提示词时你完全清楚当前上下文有什么；写Skill时你不知道触发时上下文里还有什么（可能有其他Skill、用户文件等）。3）调整方式——提示词看到回复不对可以立刻改；Skill没有人能实时纠正。最大的思维陷阱是：写提示词时含糊一点没关系（因为随时可以追问补充），但Skill中的含糊意味着每次执行都会在那个含糊处出错。一句话：提示词可以模糊因为你在场，Skill必须精确因为你不在场。",
    },
    {
        "id": 10,
        "category": "实操排错",
        "difficulty": "重点",
        "question": """以下Skill文件夹结构有什么问题？请找出所有错误：

```
Notion_Project_Setup/
├── SKILL.md
├── README.md
├── references/
│   └── notion-api-docs.md
└── scripts/
    └── setup.py
```""",
        "key_points": [
            "文件夹名 Notion_Project_Setup 不符合kebab-case规范——不能有大写字母和下划线",
            "正确命名应该是 notion-project-setup",
            "文件夹内包含README.md——Skill文件夹不允许有README.md",
            "说明内容应放在SKILL.md中或references/文件夹里",
            "SKILL.md中的name字段也必须与文件夹名一致",
        ],
        "reference_answer": "有两个错误：1）文件夹名 'Notion_Project_Setup' 不符合规范——Skill文件夹必须使用kebab-case（全小写+短横线），不能有大写字母和下划线。应改为 'notion-project-setup'。同时SKILL.md中的name字段也必须与文件夹名完全一致。2）文件夹内包含README.md——Skill规范明确禁止在Skill文件夹中放README.md文件。如果有项目说明需求，应将内容放在SKILL.md的正文中或者放到references/文件夹里。其他部分（SKILL.md、references/、scripts/）的结构是正确的。",
    },
    {
        "id": 11,
        "category": "Skill设计思维",
        "difficulty": "进阶",
        "question": "什么是渐进式披露（Progressive Disclosure）？Skill是如何通过三个阶段实现渐进式披露的？",
        "key_points": [
            "渐进式披露是Skill按需加载信息的机制，避免浪费宝贵的上下文窗口空间",
            "第一阶段：只有Skill的名称和描述在上下文中，AI知道有这个技能但没加载详细内容",
            "第二阶段：用户请求匹配到某个Skill时，才加载SKILL.md的完整内容",
            "第三阶段：只有真正需要的时候，才加载相关脚本和参考文件",
            "效果：即使有几百个Skill，每次对话的上下文也不会被撑爆",
        ],
        "reference_answer": "渐进式披露（Progressive Disclosure）是Skill按需加载信息的核心机制，目的是节省宝贵的上下文窗口空间。它分三个阶段：第一阶段——只有Skill的名称和描述（name+description）在上下文中，AI知道'我有这个技能'但还没加载详细内容；第二阶段——当用户的请求匹配到某个Skill时，才加载SKILL.md的完整内容；第三阶段——只有真正需要的时候，才加载references中的脚本和参考文件。这样即使系统中有几百个Skill，每次对话的上下文也不会被撑爆。",
    },
    # ===== 第五部分：测试与故障排查 =====
    {
        "id": 12,
        "category": "测试与排查",
        "difficulty": "重点",
        "question": "Skill写好后，应该如何测试？请描述三个层次的测试方法和各自的通过标准。",
        "key_points": [
            "第一层：人工测试（必做）——触发测试（相关请求>90%成功触发）、误触发测试（无关请求误触发率<5%）、功能测试（输出符合预期）",
            "第二层：对比测试（推荐）——将使用Skill和手动提示的结果对比，确认Skill质量不低于手动提示",
            "第三层：API自动化测试（适合技术同事）——编写脚本批量发送测试用例，自动检查触发和完成情况",
            "迭代原则：第一版很少完美，先用简单版本，根据实际使用持续调整",
        ],
        "reference_answer": "Skill测试分三个层次：1）人工测试（必做）——包括触发测试（用正常方式描述任务看是否触发，目标>90%成功率）、误触发测试（用不相关请求测试，误触发率应<5%）、功能测试（跑完整个工作流检查输出质量）。2）对比测试（推荐）——将Skill输出与手动提示的结果并排对比，确认Skill质量不低于手动方式。3）API自动化测试（适合技术人员）——编写测试脚本通过API批量发送用例，自动检查触发和完成情况。此外要记住迭代原则：第一版很少完美，先上线简单版本再根据实际问题持续调整。",
    },
    {
        "id": 13,
        "category": "实操排错",
        "difficulty": "重点",
        "question": """以下SKILL.md的正文（执行步骤部分）有什么问题？请指出写法上的缺陷：

```markdown
## 执行步骤

帮用户分析数据，生成好看的图表，然后写一份报告。
如果数据有问题就处理一下。
输出要专业。
```""",
        "key_points": [
            "步骤完全不具体——'分析数据'没有说明用什么方法分析、分析哪些维度",
            "'好看的图表'是模糊主观的描述——应明确图表类型（柱状图/折线图）、包含哪些字段",
            "'数据有问题就处理一下'是典型的提示词思维——没有定义什么算'有问题'、如何处理",
            "Skill必须精确因为你不在场——每个含糊处都会导致每次执行结果不同",
            "'输出要专业'没有定义标准——应说明输出格式、包含哪些部分、用什么语气",
            "缺少输入要求——没有说明接受什么格式的数据",
            "缺少边界情况处理——如果用户没提供数据怎么办",
        ],
        "reference_answer": "这段执行步骤犯了典型的'提示词思维残留'错误，把写提示词的习惯带到了Skill中。核心缺陷：1）'分析数据'完全不具体——应明确分析哪些维度（趋势、对比、占比等）、用什么方法。2）'好看的图表'是主观模糊词——应指定图表类型和包含字段。3）'数据有问题就处理一下'没有定义标准——什么是'有问题'？缺失值怎么办？异常值怎么办？这些都应写清楚。4）'输出要专业'没有可执行标准——应定义输出格式模板、包含哪些section。5）缺少输入要求和边界情况处理。核心原则：写提示词时含糊没关系（你在场可以追问），但Skill必须精确（你不在场，每个含糊处每次都会出错）。",
    },
    {
        "id": 14,
        "category": "实操排错",
        "difficulty": "重点",
        "question": """以下两个description，哪个更好？为什么？请分析各自的问题。

A: `description: 帮助用户处理各种文档和数据相关的任务`

B: `description: 将CSV销售数据按月汇总，计算环比增长率和TOP5产品排名，生成Markdown格式的月度销售简报。当用户需要分析销售数据、生成销售月报时使用。支持CSV格式输入，输出结构化Markdown报告。`""",
        "key_points": [
            "B明显更好——遵循了三段式结构：做什么+何时使用+关键能力",
            "A的问题：太宽泛，'各种文档和数据'会导致大量误触发",
            "A没有指明具体的触发场景，Claude无法判断何时该用",
            "B明确了输入格式（CSV）、处理内容（销售数据）、输出格式（Markdown）",
            "B包含了具体的触发关键词：分析销售数据、生成销售月报",
            "description不是简介，是精确的触发规则——太宽会误触发，太窄会漏触发",
        ],
        "reference_answer": "B明显更好。A的问题是太宽泛——'处理各种文档和数据相关的任务'几乎匹配所有请求，会导致大量误触发，Claude无法判断何时该调用。B遵循了description最佳实践的三段式结构：1）做什么——将CSV销售数据按月汇总，计算环比增长率和TOP5产品排名；2）何时使用——当用户需要分析销售数据、生成销售月报时；3）关键能力——支持CSV格式输入，输出Markdown报告。核心原则：description不是Skill的简介，而是精确的触发规则。Claude完全依赖它来判断是否调用该Skill。",
    },
    # ===== 第六部分：高级模式与实践 =====
    {
        "id": 15,
        "category": "高级模式",
        "difficulty": "进阶",
        "question": "Anthropic官方总结了五种Skill高级设计模式，请描述其中至少三种，并各举一个应用场景。",
        "key_points": [
            "顺序工作流编排——多步骤任务，每步输出是下步输入。如：数据清洗→指标计算→报告生成",
            "多MCP工具协调——同时或先后调用多个MCP工具。如：从Notion读取→查GitHub PR→写入Google Docs",
            "迭代精炼——生成-评估-改进循环。如：写文章→自评打分→修改直到达标",
            "情境感知工具选择——根据输入走不同处理路径。如：CSV→数据分析；PDF→文档提取；图片→图像识别",
            "领域专业知识嵌入——行业规则和专业术语放入references。如：法律合同审查Skill",
        ],
        "reference_answer": "五种设计模式（至少答三种）：1）顺序工作流编排——适合多步骤任务，每步的输出是下步的输入，如数据清洗→指标计算→报告生成→发送邮件。2）多MCP工具协调——需要调用多个MCP工具，如从Notion读取任务清单→查询GitHub PR状态→写入Google Docs周报。3）迭代精炼——生成后自评再改进，如写文章后按可读性/准确性/品牌一致性打分，低于4分继续修改。4）情境感知工具选择——根据输入走不同路径，如CSV走数据分析、PDF走文档提取。5）领域专业知识嵌入——把行业规则放入references，如法律合同审查Skill。",
    },
    {
        "id": 16,
        "category": "高级模式",
        "difficulty": "进阶",
        "question": "什么是Context Engineering（上下文工程）？它和Prompt Engineering（提示词工程）有什么区别？与Skill的设计有什么关系？",
        "key_points": [
            "Context Engineering是精确控制AI执行时上下文内容的设计方法论",
            "Prompt Engineering关注如何问一个好问题，Context Engineering关注AI在执行时能看到什么、不能看到什么",
            "五大维度：Offloading（卸载）、Reduction（压缩）、Retrieval（检索）、Isolation（隔离）、Caching（缓存）",
            "Agent执行复杂任务时上下文会急速膨胀导致context rot（上下文腐烂）",
            "写SKILL.md本质就是在做Context Engineering——决定在触发时刻向AI注入什么信息",
        ],
        "reference_answer": "Context Engineering（上下文工程）是2025年随Agent成为主流而提出的设计方法论，核心是'在上下文窗口里填入恰好合适的信息以完成下一步任务'。与Prompt Engineering的区别是：后者关注'如何问好问题'，前者关注'AI执行时能看到什么、不能看到什么'。它有五大维度：Offloading（大内容存文件只留引用）、Reduction（压缩旧结果释放空间）、Retrieval（按需从外部取回信息）、Isolation（子代理有独立上下文）、Caching（保持前部稳定提高缓存命中率）。与Skill的关系是：你写的每一个SKILL.md，本质就是在做Context Engineering——决定在某个触发时刻向AI的上下文注入什么信息。",
    },
    # ===== 第七部分：概念辨析与实操 =====
    {
        "id": 17,
        "category": "概念辨析",
        "difficulty": "重点",
        "question": "MCP和Function Calling（函数调用）经常被混淆，请解释它们的区别。",
        "key_points": [
            "Function Calling是AI模型和Agent程序之间的沟通格式",
            "MCP是Agent程序和外部工具服务之间的接口规范",
            "Function Calling相当于老板给传话筒下指令的方式",
            "MCP相当于传话筒联系外部供应商的标准流程",
            "两者完全不在一个层次，不存在谁取代谁的问题",
        ],
        "reference_answer": "Function Calling和MCP完全不在一个层次：Function Calling是AI大模型和Agent程序之间的沟通格式，相当于大模型告诉Agent'我需要调用某个工具，参数是这些'——是老板给传话筒下指令的方式。MCP是Agent程序和外部工具服务之间的接口规范，定义了工具如何暴露能力、Agent如何调用——是传话筒联系外部供应商的标准流程。两者各管各的层级，不存在谁取代谁的问题。",
    },
    {
        "id": 18,
        "category": "实操编写",
        "difficulty": "重点",
        "question": """假设你要为团队创建一个"会议纪要生成"Skill，请写出它的description字段（使用三段式结构）。要求：输入是会议录音转写文本，输出是结构化会议纪要。""",
        "key_points": [
            "应包含'做什么'——从会议录音转写文本提取要点，生成结构化会议纪要",
            "应包含'何时使用'——当用户提供会议录音文字稿/转写文本并需要整理会议纪要时",
            "应包含'关键能力'——支持输入转写文本，输出包含议题、决议、待办事项的结构化纪要",
            "应有具体触发词：会议纪要、会议记录、整理会议、会议总结等",
            "不能太宽泛（如'处理会议相关内容'）也不能太窄",
        ],
        "reference_answer": "一个好的description示例：'从会议录音转写文本中提取关键信息，生成包含议题摘要、讨论要点、决议事项和待办任务的结构化会议纪要。当用户提供会议转写文稿并需要整理会议纪要、会议记录、会议总结时使用。支持纯文本格式的会议转写输入，输出Markdown格式的结构化纪要，包含参会人员、议题列表、决议和Action Items。' 关键要点：三段式结构完整（做什么+何时使用+关键能力），包含具体触发词，明确了输入输出格式。",
    },
    # ===== 第八部分：实操编写 =====
    {
        "id": 19,
        "category": "实操编写",
        "difficulty": "重点",
        "question": """以下Skill的执行步骤存在"提示词思维残留"，请改写为符合Skill规范的精确步骤：

原始版本：
```
## 步骤
1. 读取用户提供的数据
2. 分析数据中的趋势
3. 生成一份专业的分析报告
4. 如果有异常数据就标注出来
```""",
        "key_points": [
            "应明确数据格式要求——如CSV/Excel，包含哪些列",
            "应定义'趋势'的具体维度——环比变化、同比变化、移动平均等",
            "应定义报告的输出格式模板——包含哪些section、什么格式",
            "应定义'异常'的判断标准——偏离均值2个标准差？超过阈值？",
            "应增加边界情况处理——数据为空怎么办？格式不对怎么办？",
            "核心原则：Skill中你不在场，每个模糊词都会导致不可预测的执行结果",
        ],
        "reference_answer": "改写后应类似：'## 步骤\n1. 检查输入数据格式：仅接受CSV格式，必须包含date和value列。如果格式不对，提示用户修改并中止。如果数据少于3行，提示数据量不足。\n2. 数据清洗：删除value列中的空值行，将日期统一为YYYY-MM-DD格式。\n3. 趋势分析：计算月度汇总值、环比增长率、3个月移动平均线。\n4. 异常检测：标注偏离月度均值超过2个标准差的数据点为异常值。\n5. 生成报告（Markdown格式），包含以下部分：数据概览（行数、时间范围、均值）、趋势图表描述、异常值列表（日期+值+偏离度）、核心发现（3条以内）。' 核心改进：每一步都有可执行的标准和边界情况处理。",
    },
    {
        "id": 20,
        "category": "实操编写",
        "difficulty": "进阶",
        "question": """请为以下场景设计一个完整的SKILL.md的YAML frontmatter和执行步骤大纲：

场景：团队每周需要从Notion数据库中提取本周完成的任务，按项目分组统计完成数量，然后生成一份简洁的周报发到指定频道。

要求：写出name、description和关键执行步骤（不需要完整，写出框架即可）。""",
        "key_points": [
            "name应为kebab-case格式，如 weekly-task-report",
            "description应包含三段式：做什么+何时使用+关键能力",
            "步骤应明确：从哪个Notion数据库读取、筛选条件是什么",
            "步骤应定义输出格式：周报包含哪些部分",
            "应处理边界情况：本周没有完成任务怎么办",
            "应有具体而非模糊的操作指令",
        ],
        "reference_answer": "示例：\n```yaml\n---\nname: weekly-task-report\ndescription: 从Notion任务数据库提取本周已完成任务，按项目分组统计完成数量和完成人，生成Markdown格式周报。当用户需要生成周报、统计本周任务完成情况时使用。支持Notion数据库作为数据源，输出按项目分组的结构化周报。\n---\n```\n\n执行步骤大纲：\n1. 通过Notion MCP连接，查询任务数据库中status='Done'且完成日期在本周一至今天的所有任务\n2. 按project字段分组，统计每个项目的完成任务数和负责人\n3. 如果本周无完成任务，生成'本周暂无完成任务'的简要说明\n4. 生成Markdown周报，包含：日期范围、各项目完成统计表格、本周亮点（完成最多的项目）、总计\n5. 输出周报内容供用户确认后发送\n\n关键要素：name用kebab-case、description三段式完整、步骤具体可执行、有边界情况处理。",
    },
]


def get_all_questions():
    """获取所有题目的摘要信息（不含答案）"""
    return [
        {
            "id": q["id"],
            "category": q["category"],
            "difficulty": q["difficulty"],
            "question": q["question"],
        }
        for q in QUESTIONS
    ]


def get_question_by_id(question_id: int):
    """根据ID获取题目"""
    for q in QUESTIONS:
        if q["id"] == question_id:
            return q
    return None


def get_total_count():
    """获取题目总数"""
    return len(QUESTIONS)


def get_categories():
    """获取所有分类"""
    cats = []
    seen = set()
    for q in QUESTIONS:
        if q["category"] not in seen:
            cats.append(q["category"])
            seen.add(q["category"])
    return cats
