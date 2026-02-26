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
        "category": "SKILL.md配置",
        "difficulty": "进阶",
        "question": "SKILL.md中有哪些可选的YAML字段？分别有什么作用？请至少说出4个。",
        "key_points": [
            "license——开源协议，说明使用权限",
            "compatibility——指定支持的平台列表（claude-ai, claude-code, api）",
            "metadata.author——创建者名称或组织",
            "metadata.version——版本号，建议用语义化版本",
            "metadata.category——分类标签",
            "metadata.tags——关键词列表，便于搜索",
            "allowed-tools——允许Skill使用的工具白名单",
        ],
        "reference_answer": "SKILL.md的可选YAML字段包括：1）license——开源协议，如MIT、Apache-2.0，用于说明使用权限；2）compatibility——支持平台列表，如[claude-ai, claude-code, api]；3）metadata.author——创建者名称；4）metadata.version——版本号，建议用语义化版本如1.0.0；5）metadata.category——分类标签；6）metadata.tags——关键词列表便于搜索；7）allowed-tools——允许Skill使用的工具白名单，不填则使用代理默认工具集。",
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
        "category": "Skill设计思维",
        "difficulty": "重点",
        "question": "在写SKILL.md之前，应该先问自己哪三个正确的问题？请分别解释每个问题的重要性。",
        "key_points": [
            "问题一：这个Skill在什么情况下应该被触发？什么情况下不该触发？——触发边界是Skill失败最常见的原因",
            "问题二：用户的输入可能是什么形状？边界情况怎么处理？——Skill不能等用户澄清，必须在正文里写清楚处理方式",
            "问题三：这个Skill运行时，Claude的上下文里可能还有什么？——好的Skill不假设自己是唯一被加载的Skill",
        ],
        "reference_answer": "写SKILL.md前应问三个问题：1）这个Skill什么时候该触发、什么时候不该触发？——触发边界是Skill失败最常见的原因，description太宽泛会误触发、太窄会漏触发。2）用户输入可能是什么形状？边界情况怎么处理？——不同于提示词可以等下一条消息澄清，Skill必须在正文中预先写明：如果缺少X就先询问，如果是Y格式就执行步骤A。3）Skill运行时上下文里可能还有什么？——设计良好的Skill不假设自己是唯一被加载的Skill，需要能在旁边还有其他Skill的情况下正常工作。",
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
        "category": "测试与排查",
        "difficulty": "重点",
        "question": "如果你的Skill上传失败了，可能是哪些原因？请列举至少3种常见原因及其解决方法。",
        "key_points": [
            "主文件命名不对——必须是SKILL.md（全大写），不能是skill.md或Skill.md",
            "文件夹命名不规范——必须是kebab-case，不能有空格或大写字母",
            "包含README.md——删除Skill文件夹内的README.md",
            "name字段含claude或anthropic——这是系统保留词",
            "YAML语法错误——检查frontmatter的缩进",
        ],
        "reference_answer": "Skill上传失败的常见原因：1）主文件命名错误——文件名必须是SKILL.md（全大写），skill.md、Skill.md、SKILL.MD都会失败，需修改为正确命名。2）文件夹命名不规范——必须使用kebab-case（小写+短横线），不能有空格、大写字母或下划线。3）文件夹内包含README.md——需删除README.md，将说明内容移到SKILL.md或references/文件夹中。4）name字段包含claude或anthropic——这是系统保留词，需更换名称。5）YAML语法错误——YAML对缩进敏感，检查frontmatter格式是否正确。",
    },
    {
        "id": 14,
        "category": "测试与排查",
        "difficulty": "进阶",
        "question": "如果Skill不触发（该用的时候没被调用），或者被错误触发（不该用的时候被调用了），分别应该怎么排查和修复？",
        "key_points": [
            "不触发的原因：description太模糊/太窄，缺少具体触发场景和关键词",
            "不触发的修复：在description中加入具体触发场景和关键词",
            "不触发也可能是YAML语法错误导致Skill未被正确解析",
            "错误触发的原因：description过于宽泛",
            "错误触发的修复：缩小description范围，加入'仅当...'等限制语",
        ],
        "reference_answer": "Skill不触发时：最可能是description太模糊或太窄——需要在description中加入具体的触发场景和关键词，比如'当用户说分析数据、生成报告时触发'。也可能是YAML语法错误导致Skill未被正确解析，需检查frontmatter缩进。Skill被错误触发时：原因通常是description过于宽泛，解决方法是缩小description范围，加入限制语如'仅当用户需要分析营销数据时使用，不适用于财务数据分析'，让Claude能准确区分该Skill的适用边界。",
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
    # ===== 第七部分：概念辨析 =====
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
        "category": "概念辨析",
        "difficulty": "重点",
        "question": "Skill和CLAUDE.md有什么区别？分别适合存放什么类型的内容？",
        "key_points": [
            "CLAUDE.md是项目级的常驻说明，每次Claude Code启动时都会读取",
            "Skill是按需加载的专项技能，只在用户请求匹配时才读取",
            "CLAUDE.md适合放项目架构、编码规范、技术栈说明、运行命令等",
            "Skill适合封装特定的工作流程，如数据分析流水线、报告生成等",
        ],
        "reference_answer": "CLAUDE.md是项目级的常驻说明，每次Claude Code启动时都会自动读取，适合放项目架构概述、技术栈说明、编码规范、运行命令、注意事项等需要Claude始终了解的信息。Skill是按需加载的专项技能，只在用户请求匹配时才被读取和执行，适合封装特定的工作流程，如营销数据分析流水线、报告生成模板、代码审查流程等可复用的任务。简单说：CLAUDE.md是背景知识（始终在场），Skill是专业技能（按需调用）。",
    },
    # ===== 第八部分：实操应用 =====
    {
        "id": 19,
        "category": "实操应用",
        "difficulty": "重点",
        "question": "创建Skill的推荐步骤是什么？为什么建议最后才写description？",
        "key_points": [
            "第一步：识别值得做成Skill的任务（每周至少做一次、有固定输入输出、每次都要解释同样背景）",
            "第二步：手动做一次，像法庭书记员一样记录每个决策点",
            "第三步：起草SKILL.md——先写步骤→再写输入要求→再写输出格式→最后写description",
            "第四步：检查是否有提示词思维残留（模糊词、隐性假设、未处理的边界情况）",
            "第五步：从最小可用版本开始迭代",
            "最后写description是因为：在步骤写完之前，你往往不清楚Skill的真正边界，应让步骤来塑造描述",
        ],
        "reference_answer": "推荐的创建步骤：1）识别值得做Skill的任务——每周至少做一次、有固定输入输出格式、每次要解释同样背景。2）手动做一遍并详细记录每个操作、判断依据和边界情况处理。3）起草SKILL.md，按此顺序：先写步骤（核心）→再写输入要求→再写输出格式→最后写description。4）自检是否有提示词思维残留，把模糊词替换为具体标准。5）从最小可用版本开始迭代。之所以最后写description，是因为在步骤写完之前你往往不清楚Skill的真正边界，应该让步骤来塑造描述而不是反过来。",
    },
    {
        "id": 20,
        "category": "实操应用",
        "difficulty": "重点",
        "question": "Skill的三大设计原则是什么？请分别解释每个原则的含义。",
        "key_points": [
            "渐进式披露（Progressive Disclosure）——三级加载机制，按需消耗上下文",
            "可组合性（Composability）——Skill能与其他Skill协同工作，不能假设自己是唯一技能",
            "可移植性（Portability）——Skill在Claude.ai、Claude Code和API三个环境中行为一致，一次制作全平台通用",
        ],
        "reference_answer": "Skill的三大设计原则：1）渐进式披露（Progressive Disclosure）——采用三级加载机制，只在需要时才加载详细内容，避免浪费上下文空间。2）可组合性（Composability）——Claude可以同时加载多个Skill，你的Skill应该能与其他Skill协同工作，不能假设自己是唯一被加载的技能。3）可移植性（Portability）——Skill在Claude.ai、Claude Code和API三个环境中行为完全一致，一次制作即可全平台通用。这三个原则来自Anthropic官方文档，是Skill设计的基石。",
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
