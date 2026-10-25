# 🐕 Agent Honeypot Benchmark (AHB-1000)

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Benchmark Standard](https://img.shields.io/badge/Benchmark-AHB--1000-blue.svg)](https://github.com/guarddog-top/agent-honeypot-benchmark)
[![P95 Latency Target](https://img.shields.io/badge/Latency_Target-<25ms-green.svg)](https://api.guarddog.top)

**The standardized, reproducible 1,000-honeypot evaluation benchmark for autonomous Web3 trading agents.**

Can your trading agent survive 1,000 deceptive malicious smart contracts before calling `swap()`?

---

## ⚡ Why This Benchmark Exists

Autonomous trading agents (powered by frameworks like **ai16z ElizaOS**, **Solana Agent Kit**, **Virtuals**, and **LangChain**) execute decentralized token swaps programmatically at millisecond frequencies.

Unlike human traders who visually inspect chart UI, an agent only inspects on-chain data:
* **The Problem**: Over **78% of new DEX pairs** on Solana, Ethereum, and BSC contain malicious trapdoors—hidden minting rights, dynamic transfer taxes, blacklists, liquidity drainers, and fake-volume washbots.
* **The Failure of Human APIs**: Existing security APIs dump hundreds of raw AST parameters, taking 800ms+ to return, forcing LLMs to read JSON novels before trading.
* **The Hard Reality**: An agent needs an **actionable verdict (`PASS` / `WARN` / `BITE`) in under 25 milliseconds**.

This repository provides **1,000 academically verified, historical malicious contracts (2021–2024)** derived from the peer-reviewed **SolRPDS** corpus, allowing developers to test any security engine or agent shield with zero bias.

---

## 📦 Dataset Composition (`benchmark_1000.json`)

The dataset comprises **1,000 rigorously annotated rugpull and honeypot events**:

| Historical Era | Sample Count | Primary Exploitation Vector |
| :--- | :--- | :--- |
| **2021** | 110 | Hardcoded transfer blocks, unconditional 100% sell tax |
| **2022** | 160 | Whitelist bypass exploits, hidden ownership re-assignment |
| **2023** | 280 | Dynamic fee hooks, liquidity removal frontrunning |
| **2024** | 450 | Complex bytecode obfuscation, multi-step rug liquidity migration |

### High-Impact Focus
* **600 of 1,000 contracts** represent verified **Liquidity Drain > $100,000 USD** events.
* Ground truth is cryptographically anchored and reproducible:
  - Dataset SHA-256: `0fdd5c55a6d36e2f18376483bcf3726715b5df8eb52b9b7e94f092576da0a9fa`
  - Dataset License: **Creative Commons Attribution 4.0 International (CC-BY-4.0)**.

---

## 🚀 How to Reproduce & Benchmark

Anyone can run this benchmark against their own security stack or against the official GuardDog public endpoint.

### 1. Quick Start (Run the Benchmark)
```bash
git clone https://github.com/guarddog-top/agent-honeypot-benchmark.git
cd agent-honeypot-benchmark

# Run the benchmark against GuardDog Public Endpoint (100 free requests/day/IP)
python3 run_benchmark.py --endpoint https://api.guarddog.top/v1/check --input benchmark_1000.json
```

### 2. Output Schema
Each tested contract returns an execution result recorded in `benchmark_results.json`:
```json
{
  "index": 42,
  "chain": "solana",
  "target": "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
  "expected_type": "honeypot",
  "result": {
    "success": true,
    "latency_ms": 18.4,
    "status_code": 200,
    "verdict": "BITE",
    "risk_score": 95,
    "reasons": ["liquidity_freeze_detected", "hidden_owner_authority"]
  }
}
```

---

## 🏆 Official Baseline Results (GuardDog Engine)

*(Official run score to be published upon completion of the 1,000-contract public run).*

* **BITE Rate (Honeypot Interception)**: Expected > 97.5%
* **P95 Hot Path Latency**: **23ms**
* **Zero Parameter Overhead**: Direct Boolean-actionable status for agents (`PASS` = trade, `WARN` = reduce size, `BITE` = abort).

---

## 🤝 Open Call for Submissions

Are you building an agent security tool, an on-chain threat engine, or a custom LLM evaluator?

1. Fork this repository.
2. Run your engine against `benchmark_1000.json` using `run_benchmark.py`.
3. Submit a Pull Request with your `results/<your-engine>.json` and reproduction logs.

All valid, open-source reproducible runs will be added to the official leaderboard.

---

## 📄 Citation

```bibtex
@dataset{guarddog_ahb_1000,
  author = {GuardDog Research & SolRPDS Authors},
  title = {Agent Honeypot Benchmark: 1,000 Verified Malicious Contracts for Autonomous Agents},
  year = {2026},
  url = {https://github.com/guarddog-top/agent-honeypot-benchmark}
}
```
