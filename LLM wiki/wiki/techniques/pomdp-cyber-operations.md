---
title: "POMDP in Cyber Operations (網絡攻防中的部分可觀察馬可夫決策過程)"
category: "techniques"
tags: [pomdp, rl, probability, decision-theory, cybersecurity]
---

# POMDP in Cyber Operations (網絡攻防中的部分可觀察馬可夫決策過程)

## 概述
在真實的網路攻防場景中，攻擊者與防禦者皆面臨資訊不對稱的挑戰。攻擊者無法獲悉內部網絡的完整拓撲、伺服器內部配置或安全監控規則。這使得網絡滲透測試無法被簡化為標準的 MDP，而必須建模為**部分可觀察馬可夫決策過程 (POMDP)**。

## 核心數學公式
POMDP 由七元組 $\langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \Omega, \mathcal{O}, \gamma \rangle$ 構成。
因為真實狀態 $s \in \mathcal{S}$ 不可直觀，智慧體必須維護**信念狀態（Belief State）** $b \in \Delta(\mathcal{S})$，代表當前處於各個可能狀態的機率分佈：

$$b'(s') = \eta \cdot \mathcal{O}(o \mid s', a) \sum_{s \in \mathcal{S}} \mathcal{T}(s' \mid s, a) b(s)$$

其中 $\eta$ 為正規化常數。

## 應用突破
在 [[Schwartz2019-POMDPPenTest.md]] 與 [[Pham2024-Raiju.md]] 中，研究人員將信念狀態與類神經網絡結合，使 AI 能夠在不確定、動態變化的網絡拓撲中，以高達 84% 以上的成功率精確完成提權。

## 關聯詞條
- [[Schwartz2019-POMDPPenTest.md]]
- [[Pham2024-Raiju.md]]
- [[Microsoft2021-CyberBattleSim.md]]
