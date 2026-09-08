# 📊 In-Depth Token & Cost Calculation Guide: YT Helper RAG

This document provides a line-by-line, comprehensive mathematical breakdown of token consumption and financial cost for every query processed by the **YT Helper** system.

---

## 📑 Table of Contents
1. [Executive Summary](#1-executive-summary)
2. [Video Ingestion Stage Token Cost](#2-video-ingestion-stage-token-cost)
3. [Vector Search Stage (ChromaDB)](#3-vector-search-stage-chromadb)
4. [Line-by-Line Token Breakdown per Query](#4-line-by-line-token-breakdown-per-query)
5. [Total Token Count per Query](#5-total-token-count-per-query)
6. [Financial Cost Analysis (Groq Cloud API)](#6-financial-cost-analysis-groq-cloud-api)
7. [Groq Free Tier & Rate Limits (TPM / RPM)](#7-groq-free-tier--rate-limits-tpm--rpm)
8. [Token Optimization Techniques](#8-token-optimization-techniques)

---

## 1. Executive Summary

| Metric | Typical Value | Notes |
| :--- | :--- | :--- |
| **Ingestion Token Cost** | **0 API Tokens** ($0.00) | Handled locally via SentenceTransformers |
| **Vector Search Cost** | **0 API Tokens** ($0.00) | Handled locally in ChromaDB |
| **Input Tokens (Prompt + Context)** | **~1,450 – 1,600 tokens** | Top 7 chunks (800 chars each) + prompt |
| **Output Tokens (LLM Response)** | **~200 – 450 tokens** | 1 to 3 paragraphs |
| **Total Tokens Per Query** | **~1,650 – 2,050 tokens** | Combined input and generated output |
| **Average Cost Per Query (Groq)** | **~$0.0011 USD** | Roughly **1/10th of a single US cent** (~₹0.09) |
| **Queries per $1.00 USD** | **~850 to 1,000 queries** | Highly cost-efficient architecture |

---

## 2. Video Ingestion Stage Token Cost

When a user calls `/youtube_url`:
1. **services/chunk_extractor.py**:
   - Fetches the transcript directly from YouTube servers via `youtube_transcript_api`.
   - **Cost: 0 API tokens / $0.00**.
2. **services/embadding.py**:
   - Splits text using `RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)`.
   - Generates embeddings locally using `SentenceTransformer("all-MiniLM-L6-v2")` running directly on your CPU/GPU.
   - Stores vectors directly into local ChromaDB (`./chroma_db`).
   - **Cost: 0 API tokens / $0.00**.

> 💡 **Takeaway:** Ingesting a video of **any length** (5 minutes, 1 hour, or 4 hours) costs **0 API tokens** and does not use any cloud LLM quota.

---

## 3. Vector Search Stage (ChromaDB)

When a query is submitted:
1. `services/query.py` encodes the user question with `SentenceTransformer`.
   - Performed locally.
   - **Cost: 0 API tokens**.
2. ChromaDB queries cosine similarity and retrieves the **top 7 chunks**:
   - Each chunk has a target size of **800 characters** with 150-character overlap.
   - 7 chunks × ~800 characters = **~5,600 characters of raw context**.
   - Joined with `\n\n---\n\n` (6 separators × 7 characters = 42 characters).
   - **Total Context Size: ~5,642 characters**.

---

## 4. Line-by-Line Token Breakdown per Query

In modern tokenizers (such as LLaMA Byte-Pair Encoding), **1 token ≈ 4 characters** (or ~0.75 words) for standard English text.

Here is the exact message payload sent to Groq in `services/groq_connection.py`:

### A. System Message Payload
```python
{
    "role": "system",
    "content": (
        "You are YT Helper, a helpful assistant. You summarize YouTube video content and answer user queries based on video transcript context. "
        "Always respond naturally and directly to the user's question without mentioning transcript chunks, video context, or internal data structures. "
        "Your response must always be written in paragraph form only. Never format answers using tables, charts, or graphs."
    )
}
```
* **Character count:** 427 characters (with spaces).
* **Token estimation:** **~85 tokens**.

---

### B. User Message Payload
```python
{
    "role": "user",
    "content": f"User question: {prompt}\n\nVideo context: {chunk_list}"
}
```
1. **Template framing overhead:**
   - `"User question: "` = 3 tokens.
   - `"\n\nVideo context: "` = 4 tokens.
   - **Subtotal: 7 tokens**.

2. **User Question (`{prompt}`):**
   - Typical question (e.g., *"What were the key takeaways from the discussion on neural networks?"*):
   - Characters: 60 – 120 characters (~15 – 30 words).
   - **Subtotal: ~15 – 35 tokens**.

3. **Retrieved Video Context (`{chunk_list}`):**
   - 7 retrieved chunks from ChromaDB.
   - Total characters: ~5,600 characters.
   - Calculation: `5,600 characters / 4` = **~1,400 tokens**.
   - **Subtotal: ~1,350 – 1,450 tokens**.

4. **Chat Template Overhead (Special Tokens):**
   - Role headers: `<|start_header_id|>system<|end_header_id|>`, `<|start_header_id|>user<|end_header_id|>`, etc.
   - **Subtotal: ~15 tokens**.

---

### C. Output Payload (LLM Response)
Because the system prompt specifies:
> *"Your response must always be written in paragraph form only. Never format answers using tables, charts, or graphs."*

* The model generates between **1 and 3 focused paragraphs**.
* Word count: 150 – 300 words.
* Character count: 800 – 1,600 characters.
* **Output Token Count: ~200 – 400 tokens**.

---

## 5. Total Token Count per Query

| Component | Character Count | Token Count | % of Query Cost |
| :--- | :--- | :--- | :--- |
| **System Prompt** | 427 chars | ~85 tokens | 4.6% |
| **Prompt Template Framing** | 30 chars | ~7 tokens | 0.4% |
| **User Question** | ~80 chars | ~20 tokens | 1.1% |
| **Video Context (7 Chunks)** | ~5,600 chars | ~1,400 tokens | 76.5% |
| **Chat Framing Overhead** | — | ~15 tokens | 0.8% |
| **TOTAL INPUT TOKENS** | **~6,137 chars** | **~1,527 tokens** | **83.4%** |
| **OUTPUT TOKENS (Response)** | ~1,200 chars | **~300 tokens** | **16.6%** |
| **GRAND TOTAL PER QUERY** | — | **~1,827 tokens** | **100%** |

---

## 6. Financial Cost Analysis (Groq Cloud API)

Groq provides extremely competitive pricing on high-end open-source models:

### Example Model Rates (per 1,000,000 tokens):
* **Llama 3.3 70B (Versatile)**:
  * Input: **$0.59** per 1M tokens ($0.00000059 / token)
  * Output: **$0.79** per 1M tokens ($0.00000079 / token)
* **Llama 3.1 8B (Instant)**:
  * Input: **$0.05** per 1M tokens ($0.00000005 / token)
  * Output: **$0.08** per 1M tokens ($0.00000008 / token)

---

### Exact Mathematical Cost Breakdown per Query

#### Scenario A: Using Llama 3.3 70B
* **Input Cost:** 1,527 × $0.00000059 = **$0.0009009**
* **Output Cost:** 300 × $0.00000079 = **$0.0002370**
* **Total Cost per Query:** $0.0009009 + $0.0002370 = **$0.001138 USD**

* **1 Single Query Cost:** ~$0.0011 USD (~0.11 cents).
* **100 Queries:** ~$0.11 USD.
* **1,000 Queries:** ~$1.14 USD.

#### Scenario B: Using Llama 3.1 8B
* **Input Cost:** 1,527 × $0.00000005 = **$0.0000763**
* **Output Cost:** 300 × $0.00000008 = **$0.0000240**
* **Total Cost per Query:** **$0.0001003 USD**

* **10,000 Queries:** Just **$1.00 USD**.

---

## 7. Groq Free Tier & Rate Limits (TPM / RPM)

If you are using Groq's **Free Developer Tier**, your financial cost is **$0.00**, but you must stay within rate limits:

1. **Tokens Per Minute (TPM)**:
   * Typical Free Tier limit: **6,000 to 30,000 TPM** (varies by model).
   * Since each query consumes **~1,527 input tokens**, a single query consumes ~5% to ~25% of your per-minute bucket.
   * Sending more than **4 to 15 rapid queries within 60 seconds** may trigger a `429 RateLimitError`.
2. **Requests Per Minute (RPM)**:
   * Usually 30 RPM on free tier (plenty for human user interaction).
3. **Requests Per Day (RPD)**:
   * Usually 14,400 RPD on free tier.

---

## 8. Token Optimization Techniques

If you want to reduce token usage or prevent TPM rate limit hits, you can tune these settings in the codebase:

1. **Adjust Chunk Count (`n_results` in `services/query.py`)**:
   * Currently set to `n_results=7` (~1,400 tokens).
   * Changing to `n_results=4` reduces input tokens to **~800 tokens** (saving **~40% on token consumption** per query while still providing ~3,200 chars of context).
2. **Adjust Chunk Size (`chunk_size` in `services/embadding.py`)**:
   * Currently set to `chunk_size=800, chunk_overlap=150`.
   * A chunk size of `500` with `overlap=100` allows tighter, more selective retrieval.
3. **Add `max_tokens` Limit in Groq Call**:
   * In `services/groq_connection.py`, you can pass `max_tokens=350` to guarantee the model never generates excessively long paragraphs that inflate output costs.

