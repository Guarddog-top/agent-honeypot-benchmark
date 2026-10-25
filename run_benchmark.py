#!/usr/bin/env python3
"""
Agent-Honeypot-Benchmark: Open Evaluation Harness for Autonomous Trading Agents
Version: 1.0.0
License: CC-BY-4.0

This script allows anyone to benchmark an on-chain security API against the 
standardized 1,000 malicious token dataset (SolRPDS corpus, 2021-2024).

Usage:
    python3 run_benchmark.py --endpoint https://api.guarddog.top/v1/check --input benchmark_1000.json
"""

import argparse
import json
import time
import sys
import urllib.request
import urllib.error
from typing import Dict, Any, List

def run_test(endpoint: str, chain: str, target: str, token: str = None) -> Dict[str, Any]:
    url = f"{endpoint}?chain={chain}&target={target}"
    headers = {"User-Agent": "Agent-Honeypot-Benchmark/1.0"}
    if token:
        headers["X-ATG-Token"] = token
        headers["X-GuardDog-Token"] = token
        
    start_time = time.perf_counter()
    status_code = 0
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            status_code = resp.status
            body = json.loads(resp.read().decode("utf-8"))
            return {
                "success": True,
                "latency_ms": elapsed_ms,
                "status_code": status_code,
                "verdict": body.get("verdict", "UNKNOWN"),
                "risk_score": body.get("risk_score", 0),
                "reasons": body.get("reasons", []),
                "error": None
            }
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return {
            "success": False,
            "latency_ms": elapsed_ms,
            "status_code": e.code,
            "verdict": "ERROR",
            "risk_score": 0,
            "reasons": [],
            "error": str(e)
        }
    except Exception as e:
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return {
            "success": False,
            "latency_ms": elapsed_ms,
            "status_code": 0,
            "verdict": "ERROR",
            "risk_score": 0,
            "reasons": [],
            "error": str(e)
        }

def main():
    parser = argparse.ArgumentParser(description="Run the 1,000 Honeypot Benchmark for Web3 Security APIs")
    parser.add_argument("--endpoint", default="https://api.guarddog.top/v1/check", help="API endpoint to test")
    parser.add_argument("--token", default=None, help="Optional API authentication token")
    parser.add_argument("--input", default="benchmark_1000.json", help="Path to benchmark_1000.json")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of tokens tested (for quick smoke tests)")
    parser.add_argument("--output", default="benchmark_results.json", help="Output results file")
    args = parser.parse_args()

    print("==================================================================")
    print(" 🐕 Agent-Honeypot-Benchmark: The 1,000 Honeypot Challenge")
    print(f" Target Endpoint: {args.endpoint}")
    print("==================================================================")

    try:
        with open(args.input, "r") as f:
            tokens: List[Dict[str, Any]] = json.load(f)
    except FileNotFoundError:
        print(f"[!] Benchmark dataset '{args.input}' not found. Using sample test suite.")
        tokens = [
            {"chain": "eth", "target": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2", "type": "safe_anchor", "note": "WETH"},
            {"chain": "eth", "target": "0xdAC17F958D2ee523a2206206994597C13D831ec7", "type": "safe_anchor", "note": "USDT"},
            {"chain": "solana", "target": "0xdeadbeefdeadbeef", "type": "synthetic_honeypot", "note": "Synthetic Test"}
        ]

    if args.limit:
        tokens = tokens[:args.limit]

    total = len(tokens)
    print(f"[*] Loaded {total} test contracts. Commencing evaluation...\n")

    results = []
    latencies = []
    caught_count = 0
    pass_count = 0
    warn_count = 0
    error_count = 0

    for idx, item in enumerate(tokens, 1):
        chain = item.get("chain", "solana")
        target = item.get("target") or item.get("address")
        expected_type = item.get("type", "honeypot")

        res = run_test(args.endpoint, chain, target, args.token)
        results.append({
            "index": idx,
            "chain": chain,
            "target": target,
            "expected_type": expected_type,
            "result": res
        })

        if res["success"]:
            latencies.append(res["latency_ms"])
            verdict = res["verdict"]
            if verdict == "BITE":
                caught_count += 1
            elif verdict == "WARN":
                warn_count += 1
            elif verdict == "PASS":
                pass_count += 1
            print(f"[{idx:4d}/{total}] {chain.upper():6s} {target[:12]}... -> {verdict:5s} ({res['latency_ms']:.1f}ms)")
        else:
            error_count += 1
            print(f"[{idx:4d}/{total}] {chain.upper():6s} {target[:12]}... -> FAILED ({res['error']})")

    latencies.sort()
    p50 = latencies[len(latencies) // 2] if latencies else 0
    p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0

    summary = {
        "benchmark_version": "1.0.0",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "target_endpoint": args.endpoint,
        "total_evaluated": total,
        "bite_caught": caught_count,
        "warn_flagged": warn_count,
        "pass_allowed": pass_count,
        "errors": error_count,
        "latency_p50_ms": round(p50, 2),
        "latency_p95_ms": round(p95, 2)
    }

    with open(args.output, "w") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2)

    print("\n==================================================================")
    print(" 📊 EVALUATION SUMMARY")
    print("==================================================================")
    print(f" Total Tokens:     {total}")
    print(f" BITE (Blocked):   {caught_count} ({caught_count/total*100:.1f}%)")
    print(f" WARN (Flagged):   {warn_count} ({warn_count/total*100:.1f}%)")
    print(f" PASS (Cleared):   {pass_count} ({pass_count/total*100:.1f}%)")
    print(f" Network Errors:   {error_count}")
    print(f" P50 Latency:      {p50:.2f} ms")
    print(f" P95 Latency:      {p95:.2f} ms")
    print(f" Full Report Saved: {args.output}")
    print("==================================================================")

if __name__ == "__main__":
    main()
