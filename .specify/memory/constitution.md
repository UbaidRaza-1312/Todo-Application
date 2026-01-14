<!-- SYNC IMPACT REPORT
Version change: 1.0 → 2.0.0
Modified principles: None (completely new constitution based on project requirements)
Added sections: All sections (new constitution)
Removed sections: None (this is a new constitution)
Templates requiring updates: ✅ updated - .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
Follow-up TODOs: None
-->
# Todo App Qwen Constitution

## Core Principles

### Accuracy
Every technical and conceptual claim must be verifiable through primary sources. System behavior must match documented specifications exactly.

### Clarity
Writing must target an academic computer science audience. Code, specs, and documentation must use precise, unambiguous language.

### Reproducibility
Any result must be independently reproducible using: Specs, Prompts, Versioned configurations. No undocumented manual intervention is allowed.

### Rigor
Claims must prioritize peer-reviewed literature. Engineering decisions must be justified by standards or research.

### Academic Integrity
Zero-tolerance for plagiarism. All sources must be cited in APA style. AI-generated content must be reviewed, edited, verified, and properly referenced.

### Responsible AI Use
AI tools (QWEN CLI, Spec-Kit Plus) are engineering collaborators, not authorities. All outputs require human validation, spec conformance, and security review.

## Security Constitution
Authentication Law: Every API request must include Authorization: Bearer <JWT>. Tokens must be signed with BETTER_AUTH_SECRET, time-limited, and verifiable by backend. Data Sovereignty: Users may only view, modify, delete their own tasks. Zero-Trust API: No endpoint is public. No implicit trust between frontend and backend. Identity is proven only by cryptographic verification.

## Development Workflow
All development must follow: Write Spec → Generate Plan → Break into Tasks → Implement via QWEN CLI. Manual coding is constitutionally prohibited. Toolchain: Specs (GitHub Spec-Kit Plus), Implementation (QWEN), Frontend (Next.js App Router), Backend (FastAPI), ORM (SQLModel), Database (Neon Serverless PostgreSQL), Auth (Better Auth + JWT).

## Governance
All work must follow the governance model: Architecture (Spec documents), Implementation (QWEN CLI under spec control), Security (JWT + Better Auth policies), Data (Database schema specs), Research Claims (Peer-reviewed sources). Any change must follow: Spec update, Review, AI regeneration, Validation. No direct code edits outside the Agentic Dev Stack workflow.

**Version**: 2.0.0 | **Ratified**: 2026-01-11 | **Last Amended**: 2026-01-11