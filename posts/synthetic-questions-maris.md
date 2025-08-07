---
title: Building Better RAG Evaluations
summary: Systematic Approach to Synthetic Question Generation for Marine Radioactivity Research
date: August 7, 2025
tags:
  - RAG
  - LLM Evals
  - Radioactivity
---

## The Challenge: Why Generic Test Cases Fall Short for Domain-Specific RAG Systems
When building a RAG system for the [IAEA's marine radioactivity knowledge base](https://marise-dev-app.pla.sh), we faced a common but underappreciated problem: **how do you systematically test a system that serves radically different users with vastly different needs?**

Most RAG evaluations rely on generic test cases or simple question templates. You might see evaluations with questions like "What is the definition of X?" or "Summarize document Y." While these capture basic functionality, they miss the nuanced complexity of real-world domain applications.

Consider our marine radioactivity system. A nuclear safety regulator asking *"How do current Cs-137 levels in Pacific fish compare to pre-Fukushima baseline measurements for food safety assessment?"* has completely different expectations than a concerned parent asking *"Is it safe to eat fish from the Pacific Ocean after Fukushima?"* Both are legitimate users, but they need different levels of technical detail, different terminology, and different types of evidence.

**The gold standard, of course, is real user data.** Nothing beats actual queries from your users in production. But when you're building a new system—or expanding to serve new audiences—you need a way to anticipate diverse usage patterns before you have enough real data to work with. This synthetic approach isn't a one-time exercise either; it's something you iterate on as you learn more about your users and discover new failure modes.

Without systematic test generation that captures this diversity, you're essentially flying blind—optimizing for average performance while missing critical edge cases that could undermine user trust or, worse, lead to misinterpretation of safety-critical information.

*Note: The structured approach I'll describe was inspired by the excellent evaluation methodology taught in [Parlance Labs' course on LLM evaluations](https://maven.com/parlance-labs/evals).*

## Our Solution: Structured Synthetic Question Generation

Rather than randomly generating questions or relying on generic templates, we turned to a systematic approach borrowed from qualitative research methodology. The key insight is to identify the fundamental **dimensions** along which your users and their queries vary, then systematically sample across those dimensions.

A dimension represents one axis of variation in how users interact with your system. For our marine radioactivity RAG, we identified three critical dimensions after analyzing our target audiences and use cases:

**1. Query Type/Purpose**
- Scientific/Technical (analytical methods, specific measurements, research findings)
- Regulatory/Safety (food safety assessments, contamination levels, risk evaluation)  
- Educational/General Public (layman explanations of mechanisms, basic concepts)
- Metadata/Discovery (listing studies, regions, dates, most cited papers)

**2. Audience Expertise Level**
- Domain Expert (scientists, researchers familiar with radioactivity terminology)
- Professional (regulators, policymakers who need accurate info but may need context)
- General Public (requires simplified explanations, analogies, avoiding jargon)

**3. Query Specificity/Complexity**
- Direct Factual (specific measurements, dates, locations)
- Analytical/Comparative (trends, correlations, multi-parameter analysis)
- Conceptual/Explanatory (mechanisms, processes, "how" and "why" questions)

This dimensional approach offers several key advantages over ad-hoc question generation:

**Systematic Coverage:** By sampling across all dimensional combinations, we ensure we don't accidentally cluster around common use cases while missing edge cases.

**Diversity by Design:** The framework forces us to generate questions spanning different expertise levels, query types, and complexity—preventing the kind of homogeneous test sets that miss critical failure modes.

**Anchoring Prevention:** Having explicit dimensions helps avoid the tendency to generate questions that are too similar to each other or biased toward what feels 'typical' to the question writer.

The magic happens when you create **tuples**—specific combinations of values from each dimension. Each tuple represents a distinct use case that your system needs to handle well.

## The Process: From Dimensions to Diverse Questions

Once we had our dimensions defined, we created **tuples**—specific combinations that represent distinct use cases. For example:

- (Scientific/Technical, Domain Expert, Direct Factual)
- (Educational/General Public, General Public, Conceptual/Explanatory)  
- (Regulatory/Safety, Professional, Analytical/Comparative)

We needed 20 diverse tuples to ensure good coverage across all dimensions. While you *can* create these manually, you can also generate them programmatically by sampling combinations, or even ask an LLM to create diverse tuples for you. The key is ensuring you get good coverage across your dimensional space rather than clustering around common combinations.

Then, for each tuple, we generated realistic questions that matched that specific combination of characteristics.

Here are some examples showing how different tuples produce very different questions:

**Tuple: (Scientific/Technical, Domain Expert, Direct Factual)**

*"What are the specific gamma spectrometry detection limits for Cs-137 in seawater samples from the Mediterranean studies?"*

**Tuple: (Educational/General Public, General Public, Conceptual/Explanatory)**

*"How does radioactive material from nuclear accidents end up in the fish we eat?"*

**Tuple: (Regulatory/Safety, Professional, Analytical/Comparative)**

*"How do current Cs-137 levels in Pacific fish compare to pre-Fukushima baseline measurements for food safety assessment?"*

**Tuple: (Metadata/Discovery, General Public, Direct Factual)**

*"Which countries have studied radioactivity in their coastal waters?"*

Notice how each question naturally reflects its tuple's characteristics—the technical complexity, audience expectations, and type of information needed all align perfectly with the dimensional values.

## Validation: Expert Approval with Minimal Edits

The real test of our systematic approach came when we shared our 100 generated questions with the lead domain expert on marine radioactivity at IAEA. Would our dimensional framework actually produce realistic, relevant questions that reflected genuine user needs?

The results exceeded our expectations. The expert's feedback was enthusiastic: 
> "These questions are great! Would very much like to learn more about how they were generated. I made some changes but really very minor as they mostly made sense and have relevance."

This validation was crucial for several reasons:

**Minimal editing required:** The fact that a world-class expert needed to make only minor adjustments suggests our dimensional approach captured the real variation in how users interact with marine radioactivity data.

**Relevance across expertise levels:** Questions designed for general public, professionals, and domain experts all passed the expert's review, indicating we successfully modeled the different audience needs.

**Coverage of real use cases:** The expert's comment that questions "have relevance" confirms we weren't just generating syntactically correct but meaningless queries—these reflected actual information needs.

This expert validation gave us confidence that our systematic approach produces higher-quality test cases than ad-hoc question generation, setting us up for meaningful evaluation of our RAG system.

## What's Next: From Questions to Systematic Evaluation

Having validated our question set, we now have a solid foundation for systematic RAG evaluation. But generating good questions is just the beginning—the real work lies in understanding how and why our system fails.

The next phase follows a rigorous methodology adapted from [**Grounded Theory**](https://www.wikiwand.com/en/articles/Grounded_theory) in qualitative research:

**1. Trace Collection**
We'll run our RAG system on all 100 questions and collect complete "traces"—the full sequence of retrieval, reasoning, and response generation for each query. This gives us the raw material to understand system behavior.

**2. Open Coding**
Rather than starting with predefined error categories, we'll read through traces and make detailed notes about anything that seems problematic—hallucinations, irrelevant retrievals, inappropriate tone, missing context. This "open coding" process from grounded theory captures the full spectrum of how our system actually fails.

**3. Axial Coding** 
We'll then cluster similar failure observations into coherent, non-overlapping failure modes through "axial coding"—another grounded theory technique. This moves us from scattered observations to a structured taxonomy of what goes wrong and why.

**4. Quantification and Prioritization**
With clear failure modes defined, we can measure their prevalence across our test set and prioritize which issues to tackle first based on frequency and impact.

**5. Automated Evaluation**
Finally, we can train LLM-as-judge evaluators to detect these specific failure modes at scale, enabling continuous monitoring as we iterate on our system.

This systematic approach ensures we're not just measuring generic "helpfulness" but understanding the specific ways our marine radioactivity RAG system falls short of user expectations.