# Documentation overview

## 1. Purpose

This folder contains all technical and client-facing documentation for the
project. The goal is to keep the documentation consistent and easy to
navigate across all subteams.

## 2. Structure

| File / Folder              | Description |
|----------------------------|-------------|
| **index.md**               | Landing page for the documentation site. |
| **overview.md**            | You are here – global index of all documentation files. |
| **architecture.md**        | System design, data flow, and integration between extraction, backend, and UI. |
| **ui_visualization.md**    | Overall dashboard / visualization concept and UX decisions. |
| **backend/**               | Backend documentation: API endpoints, service layer, and DB connection. |
| **backend/index.md**       | High-level description of the backend and how components fit together. |
| **backend/api.md**         | API reference for the FastAPI endpoints (generated with mkdocstrings). |
| **backend/services.md**    | Reference for the database / aggregation functions (generated with mkdocstrings). |
| **extraction/**            | Documentation for data extraction and preprocessing. |
| **extraction/data_analysis.md** | Detailed description of the current extraction and analysis pipeline. |
| **frontend/ui.md**         | Description of the frontend dashboard, main screens and components. |
| **client/user_manual.md**  | Client-facing user manual and demo instructions. |
| **sprint-summaries/**      | Sprint-by-sprint summaries and notes. |

## 3. Documentation guidelines

To keep documentation consistent and easy to navigate, every subteam should:

1. **Update documentation alongside code changes.**  
   When you finish a new feature, update the relevant `.md` file in this folder.

2. **Follow consistent formatting.**  
   Use clear section headers (`##`), bullet points, and short paragraphs.

3. **Avoid duplication.**  
   Link to other files instead of rewriting the same content. Example:  
   See [architecture.md](architecture.md) for overall system design.