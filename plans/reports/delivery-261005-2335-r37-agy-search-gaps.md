# AGY CLI r37: bốn search gaps giữ nguyên failed oracles

[Verified bindings](./delivery-261005-2335-r37-agy-search-gaps.json) ghi bốn user turns trên CLI1.2.17/Gemini3.8FlashMedium/always-proceed, direct packaged5s. Source r37 giữ nguyên. Brief độc lập gồm public/private `find_by_name` và `grep_search`; không rerun hoặc regrade list_dir attempt32.

| Ca | Quan sát | Native error | Policy trước tool |
|---|---|---|---|
| find-by-name-public | model-only-no-native-tool | Không có native tool | 0 |
| find-by-name-private | genuine-native-unknown-tool | unknown tool: "find_by_name" — check spelling | 0 |
| grep-search-public | model-only-no-native-tool | Không có native tool | 0 |
| grep-search-private | model-only-no-native-tool | Không có native tool | 0 |

Private find_by_name có actual native request rồi dispatcher trả unknown-tool. Đây là genuine native unsupported-tool observation; không có preflight/pre-delivery receipt, nên private enforcement unqualified. Ba ca khác có zero native tool frames: model-only no-tool outcome không chứng minh native unsupported admission hoặc NCKH denial. Cả bốn original oracles vẫn failed/unqualified; exact fixture bytes unchanged.

Four distinct conversations, one user turn per conversation, native exit0/num_turns1/resultSUCCESS. Model retries0, không fallback tool/agent hoặc đổi global profile. Init advertised names không chứng minh tool callable. Read-only help/agents inventory chỉ cung cấp flags/names; effective agent/toolset chưa được established.

Cleanup26/preserved851/protected settings-hooks unchanged. Union audit752 PID/creation FILETIME identities, zero matching/tracked-live, không taskkill. Verifier exit0 first attempt; inline verification/no independent reviewer. Source/installed r25/publication không đổi. Full native task **unchecked/44 of45/P3 active**.
