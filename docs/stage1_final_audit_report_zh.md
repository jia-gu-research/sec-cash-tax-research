# Stage 1 最终审计报告

日期：2026-11-11。总体判断：**CONDITIONAL PASS**。

技术复现及交付检查通过，可作为明确披露限制的 Stage 1 Coding Sample；不能将暂时合格记录称为已全部确认经济可比的最终研究样本。

## 实际完成

已读取原始 152-cell Notebook，并保留其为代码来源；HTML 仅作为保存结果的参考。
已验证原始 March SEC ZIP 可访问，并复核完整 SHA-256。
指定 `notebooks/outputs/march_2026_pilot.zip` 不存在；实际使用当前解压文件夹中的 12 个 CSV 作为有指纹的验证基准，没有静默替换为旧 ZIP。
HTML 包含源 Notebook 未保存的覆盖率/导出单元，这个不一致已在 SOURCE_TRACE.md 单独说明。没有从 HTML 重建源 Notebook。

已建立独立提交副本，包含 52 cells、42 个 code cells。主干抽取、分类和 Strict QA 保留在 Notebook，稳定审计/输出函数置于 src/tax_data_utils.py。
其中 32 个 code cells 映射到原始单元（含必要修改），其余为新建步骤；逐格映射在 evidence/cell_provenance.json。
新增完整导出逻辑、Total eligibility、amendment links、signed CAL QA、字段字典、README 和冻结规则。

## 实际计数桥

| stage | n_filings | reduction_from_previous | definition |
|---|---|---|---|
| 01_ORIGINAL_10K | 2340 | 0 | Original 10-K, not 10-K/A |
| 02_TOTAL_TAG_ANY_PERIOD | 1294 | 1046 | Standard Total tag present in any period/scope |
| 03_NUMERIC_TOTAL_ANY_PERIOD | 1211 | 83 | At least one nonmissing numeric Total |
| 04_CURRENT_ANNUAL_NUMERIC | 1172 | 39 | fp FY, qtrs 4, standardized ddate equals period |
| 05_DIMENSIONLESS_USD_CURRENT | 1159 | 13 | Original 1,159 coverage definition |
| 06_UNIQUE_DUPLICATE_REVIEWED | 1158 | 1 | Unique target fact; duplicate audit; prior precision-source flags cleared |
| 07_SEMANTIC_EXCLUSIONS_APPLIED | 1157 | 1 | Exclude known legacy-row ambiguity; no universal semantic verification |
| 08_ELIGIBLE_PROVISIONAL | 1157 | 0 | Mechanical checks pass; semantic validity provisional |

1,159 的原始定义为：当期年度、USD、无维度且金额非缺失的标准 Total 覆盖。它不是所有有数值 Total 的申报，更不是最终样本。
1,157 仅标记 ELIGIBLE_PROVISIONAL。没有逐份完成全部申报的经济语义核验。

## 互斥资格状态

| eligibility_status | n_filings | n_reported_zero | share_of_original_10k |
|---|---|---|---|
| ELIGIBLE_PROVISIONAL | 1157 | 123 | 0.4944444444444444 |
| EXCLUDED_NO_TOTAL_TAG | 1046 | 0 | 0.447008547008547 |
| EXCLUDED_SEMANTIC_AMBIGUITY | 1 | 1 | 0.0004273504273504 |
| EXCLUDED_TOTAL_VALUE_MISSING | 83 | 0 | 0.0354700854700854 |
| REVIEW_DIMENSIONED_TOTAL_ONLY | 13 | 0 | 0.0055555555555555 |
| REVIEW_NO_CURRENT_ANNUAL_NUMERIC | 39 | 0 | 0.0166666666666666 |
| REVIEW_UNVERIFIED_PRECISION_SOURCE | 1 | 1 | 0.0004273504273504 |

所有 2,340 份原始 10-K 均有一行状态；1,183 份非合格或待核验记录均有原因。
125 个候选报告零值全部保留；其中 123 个暂时合格，另外两个分别为 BigBear.ai 和 iWallet，均未把零改成 missing 或其他金额。只有它们的 analytical_total_usd 暂不生成。
46 个 fy/calendar label 不同的申报仍暂时合格，没有按该差异一刀切剔除。
81 份 10-K/A 单列：40 份可在月度数据内找到相同 CIK/period 原始申报，41 份原始申报不在本月。链接不证明修改范围；没有自动替换，也没有仅因存在 amendment 而剔除原始申报。

## 184 个 Strict scopes 与七个例外

原始 184 个 scope 的索引、Total/Federal/State-Local/Foreign 金额、component sum、Strict difference 均逐项与原输出完全一致。
仍为 177 个 exact matches、7 个 nonzero differences。完整七例登记表如下。

| company | adsh | strict_difference | other_candidate_amount_usd | other_cal_weight | rounding_status | final_classification |
|---|---|---|---|---|---|---|
| SMITHFIELD FOODS INC | 0000091388-26-000014 | -1000000.0 | 0.0 | nan | ROUNDING_COMPATIBLE | ROUNDING_COMPATIBLE |
| ONE GROUP HOSPITALITY, INC. | 0001104659-26-032065 | 726000.0 | 0.0 | nan | PRECISION_INCOMPATIBLE | GEO_CANDIDATE_REVIEW |
| ZUMIEZ INC | 0001193125-26-104063 | 1287000.0 | 0.0 | nan | PRECISION_INCOMPATIBLE | GEO_CANDIDATE_REVIEW |
| AVEANNA HEALTHCARE HOLDINGS, INC. | 0001193125-26-115851 | 3444000.0 | 3444000.0 | -1.0 | PRECISION_INCOMPATIBLE | OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW |
| AMERICAN SHARED HOSPITAL SERVICES | 0001437749-26-010731 | 679000.0 | 0.0 | nan | PRECISION_INCOMPATIBLE | GEO_CANDIDATE_REVIEW |
| TECNOGLASS INC. | 0001493152-26-008465 | 52000.0 | 52000.0 | -1.0 | PRECISION_INCOMPATIBLE | OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW |
| BIGBEAR.AI HOLDINGS, INC. | 0001836981-26-000018 | 28000.0 | 0.0 | nan | PRECISION_INCOMPATIBLE | TOTAL_SEMANTIC_REVIEW |

Smithfield：Federal 103m、State 19m、Foreign 3m、Total 124m；California 7m 为 State 明细，不再次相加。分类 ROUNDING_COMPATIBLE，rounding_confirmed=False。
其原始 context 为 2024-12-30 至 2025-12-28；标准化 NUM ddate 为 20251231。两者差异不自动排除。

BigBear.ai：原始 XBRL fixed-zero Total 是实际报告零值，State/Local=-28,000。
保留 reported_total_usd=0；semantic_status=LEGACY_ROW_SCOPE_AMBIGUOUS；analysis_eligible=False；没有用 -28,000 代替 Total。

**发现并纠正的重要历史解释问题：** Aveanna 3,444,000 与 Tecnoglass 52,000 的 Other 数值可补齐差额，但实际 CAL negative=1，按 ZIP readme 表示权重 -1。
因此不能继续称为正向 CAL-confirmed addition。当前分类为 OTHER_NUMERIC_MATCH_CAL_SIGN_REVIEW；accepted Other adjustment=0，另存候选金额与假设残差。
原始历史标签保存在 evidence/exception_review.csv，未被覆盖。outputs/cal_arcs_seven_filings.csv 保留七例所有 CAL arcs，便于检查方向、group 与 taxonomy version。

ONE Group、Zumiez、American Shared 的地理明细分别在数值上匹配 726,000、1,287,000、679,000 的 gap，但维度层级、是否已经包含在父类及会计语义仍需核验。没有把数值相等升级为已确认的加总关系。
所有 geo_accepted_sum=0，accounting_relationship_confirmed=False。Extended reconciliation 与 rounding compatibility 明确分开；partial disclosure 单列。

## Duplicate QA 和缺失

八个抽取概念共 11,860 条原始 NUM 行，选择后 10,926 条；四个核心概念仍为 11,851 → 10,917。
独立重算 919 个重复组：894 direct pass、8 preserve annotations、2 preserve joint interval、15 all missing。
组内 coreg/datp/durp/dimn 均一致；所有重复组及 singleton 均恰好一条 iprx=0。
463 个缺失金额保持缺失，未使用外部恢复候选填充，也未填零。

iWallet 的 Total=0、dcml=128 来自原始 NUM；有限整数 128 在数学上可以构造精度区间，不能称为无效或缺失 sentinel。
此前独立审计曾对此标记原始精度属性待核验。本次原申报网页文本可访问，但直接取得原 HTML 返回 HTTP 403，因此未完成 decimals 属性的独立核验，暂时保留 REVIEW_UNVERIFIED_PRECISION_SOURCE。
该限制和来源 URL 保存在 evidence/additional_source_checks.json 及 prior_singleton_anomalies.csv。

## 实际执行与完整性

- 干净内核完整运行：42 个 code cells，跳过 0，错误 0，耗时 26.19 秒。
- 独立提交验收：23 项检查全部通过。
- 25 个输出 CSV，共 191 个唯一变量名、662 个 file-column entries 全部有字典记录。
- 原始输入指纹比对：15 个文件全部未改变，包括开发 Notebook、HTML、原始 ZIP 和 12 个原 Pilot CSV。
- src/validate_submission.py 可独立重做输出验收；运行方法见 README。
- 新提交目录与最终 ZIP 均不含原始 SEC ZIP。

首次执行中修复了输出 helper 的 groupby 列访问问题；signed-CAL 断言随后暴露了上述历史解释问题并已修正。最终运行无错误。
Windows 本地 Jupyter 后端有事件循环/本地 TCP 提示，不影响执行或金额结果；未将其当作测试通过的替代依据。

## 文件与提交检查

提交目录：`[local path omitted]sktop/P1_SEC_Integrated/P1_Stage1_Coding_Sample/`。
完整打包文件：`[local path omitted]sktop/P1_SEC_Integrated/P1_Stage1_Coding_Sample.zip`。

- README.md：动机、来源、环境、从干净内核运行、结果、局限。
- P1_Stage1_SEC_Cash_Tax_Data_Construction.ipynb / .html：实际执行副本及新导出。
- A1_8_March_Pilot_Processing_Rules.md：17 项冻结规则及来源层次。
- data_dictionary.md：全部输出的粒度、列清单与字段定义；机器可读版本在 evidence/output_variable_dictionary.csv。
- outputs/total_eligibility_audit.csv、total_eligibility_summary.csv、total_exclusion_log.csv、total_eligibility_count_bridge.csv。
- outputs/march_pilot_exception_register.csv、cash_tax_reconciliation_184.csv、partial_disclosure_scopes.csv、geographic_relations.csv、coverage_summary.csv。
- src/tax_data_utils.py、src/validate_submission.py、requirements.txt。
- outputs/execution_report.json、acceptance_checks.json、final_validation.json：实测与验收记录。
- SOURCE_TRACE.md 和 evidence/：代码来源、历史基准、来源片段和输入指纹。

## 你需要亲自确认的内容

提交前阅读 README 的项目定位和七例登记表，尤其是两项 CAL-sign review、BigBear.ai 的语义排除和 iWallet 的暂缓资格。不要在申请材料中声称所有七例已解决，或 1,157 已全部完成原文语义验证。
技术上已实测完整运行；若希望验证你本机准备提交的副本，可按 README 的 clean-kernel 命令和独立验收命令重跑。
本次没有进入 Stage 2 回归、Stage 3 地图或新增研究问题。
