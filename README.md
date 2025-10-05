# Obfuscation Detector

A tool that detects deliberate attempts to disguise writing style in text. Uses Meta Llama for natural language analysis, in conjunction with statistical stylometric techniques.

**Live Demo:**
https://obfuscationdetector.netlify.app/

## Technologies
- **Groq API**: access to Meta Llama 3.1 8B model
- **React + Tailwind:** frontend
- **NLTK + scikit-learn:** NLP and statistical analysis
- **Docker:** containerization
- **Netlify + Render:** deployment

## Workflow
1. Input text is divided into segments using NLTK tokenization
2. Each segment is analyzed for:
- lexical features (average word length, Type-Token Ratio, Hapax Legomena Ratio)
- syntactic features (average sentence length, sentence length variance, punctuation patterns)
- part-of-speech patterns (noun ratio, function word ratio)
- readability metrics (Flesch Reading Ease syllable-based scoring)
3. Statistical variance calculated across all segments for each feature (high variance in lexical sophistication, abrupt changes in formality levels, etc.)
4. Four component scores are calculated: lexical inconsistency, syntactic inconsistency, stylistic shift, and unnatural variation. These are combinde into an overall obfuscation score
5. Llama 3.1 8B analyzes the statistical results and generates human-readable insights about detected patterns

Based on the overall score: 
- 0-30%: Minimal Risk
- 30-60%: Moderate Risk
- 60-100%: High Risk
