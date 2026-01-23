# MASTER STRATEGIC PLAN: IA FACTORY NEXUS

## 1. Executive Vision
**Mission:** Democratize AI in Algeria with a "Sovereign, Key-in-Hand" ecosystem.
**Problem:** International payment blocks (No CB), Data Sovereignty laws (Law 18.xxx), Low hardware literacy.
**Solution:** A Hybrid SaaS/Hardware platform where users buy "Access" (Credits) or "Physical sovereign units" (Box/USB) paid in DZD.

---

## 2. Phase 1: Cleaning the "Bordel" (Foundation)
*Current Status: In Progress*
Before manufacturing hardware, software must be bulletproof.
*   **Unified Backend:** Consolidate `rag-dz` into a single `services/api` folder (FastAPI). Remove 15+ loose scripts.
*   **Unified Frontend:** "Bolt Nexus" (`localhost:5173`) as the single dashboard for Chat, Code, and Apps.
*   **Orchestration:** One script (`start-nexus.bat`) to rule them all.

## 3. Phase 2: The Software Ecosystem (Nexus)
The "Product" is not just a chatbot. It is a suite:
1.  **Nexus Core (Bolt):** The daily driver. Chat with generic models (Llama 3, GPT-4 via Router).
2.  **Satellites (The Value Add):**
    *   **School (PHP):** For Education clients.
    *   **Academy (Node):** For Training.
    *   **Video (Python):** For Creators.
    *   *Strategy:* Linked via the "Nexus Dock". Launched on-demand to save RAM.

## 4. Phase 3: Hardware Packaging ( The "Physical" Assets)
To bypass the "Cloud Dependency" and "Device Anarchy":

### A. The "IA Factory Box" (B2B / Enterprise)
*Target: Companies needing Law 18.xxx compliance.*
*   **Concept:** "Plug & Play AI Server".
*   **Hardware Rec:**
    *   **Low Cost:** Orange Pi 5 Plus (32GB RAM). Powerful NPU for local LLM. Cost: ~$150.
    *   **Pro:** Refurbished HP/Dell Tiny PC (i5/i7, 64GB RAM). Cost: ~$300.
*   **Software:** Linux (Ubuntu Server) + Docker Compose + Local Ollama (Llama-3-8B).
*   **Value:** "Zero Data leaves your office."

### B. The "IA Student Stick" (B2C / Mass Market)
*Target: 2M Students without reliable internet.*
*   **Concept:** "AI on a Key".
*   **Hardware Rec:** High-Speed USB 3.2 Gen 2 (128GB/256GB). Speed is critical for loading models.
*   **Software:** "Portable Nexus".
    *   Portable Python (WinPython).
    *   Single-file Executable (Electron/Tauri).
    *   Quantized Models (GGUF format, 4-bit) for CPU inference on crappy laptops.

---

## 5. The "Brain" Strategy (AI Providers)
We use a **Hybrid Router** system managed by the Backend.

### Tier 1: Local & Sovereign (The "Law 18.xxx" Mode)
*   **Provider:** **Ollama** (running inside the Box/USB).
*   **Models:** Llama 3 (8B), Mistral (7B), Gemma 2 (9B).
*   **Cost:** 0 DZD/token (Electricity only).
*   **Privacy:** 100%.

### Tier 2: Low-Cost Cloud (The "Performance" Mode)
*   **Provider:** **Groq** (LPU Inference).
*   **Performance:** 500 tokens/sec (Instant).
*   **Cost:** Extremely low (~$0.10 / 1M tokens).
*   **Use Case:** Fast chat, coding, translation.

### Tier 3: The "Swiss Quality" (R&D)
*   **Provider:** **PublicAI / Apertus** (EPFL/ETH Zurich initiative).
*   **Use Case:** Fine-tuning a specific "Algerian Legal/Education" model.
*   **Strategy:** Use your Swiss presence to access these compute resources -> Train model -> Distill into GGUF -> Deploy on Algerian Boxes.

---

## 6. Action Roadmap
1.  **TODAY:** Validate `start-nexus.bat` (Software Core).
2.  **TOMORROW:** Clean up files (Standardize `requirements.txt`).
3.  **NEXT WEEK:** Build the "Portable USB" prototype (I can script the build process).
