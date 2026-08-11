# PRD — Visual HTML Document Editing Engine

**Product Name:** Visual HTML Editor Engine  
**Version:** 1.0  
**Status:** MVP Specification  
**Primary Stack:** Next.js + React + TypeScript

---

## 1. Product Overview

Build a browser-based **visual HTML document editing engine** that allows users to create and edit structured HTML documents visually.

The editor should behave similarly to a lightweight combination of:

- Figma
- Canva
- a document/template designer
- an HTML page builder

Users should be able to drag elements onto a page, position them precisely, resize them, edit their properties, and save the resulting document as a structured JSON representation that can be rendered into HTML.

The system must **not use raw HTML as the primary source of truth**.

Instead:

```text
User Interaction
       ↓
Document Model
       ↓
React Renderer
       ↓
HTML/CSS
```

The document model is the canonical representation of the document.

---

# 2. Primary Objective

Create a reusable visual editing engine capable of:

1. Creating document pages.
2. Adding elements to pages.
3. Dragging elements.
4. Resizing elements.
5. Selecting elements.
6. Editing element properties.
7. Editing text.
8. Positioning elements precisely.
9. Layering elements.
10. Duplicating/deleting elements.
11. Undoing/redoing changes.
12. Saving documents as JSON.
13. Loading documents from JSON.
14. Rendering documents consistently.
15. Exporting the document as HTML/CSS.

The architecture must be extensible enough to later support:

- OCR-generated layouts
- document templates
- schema-based data extraction
- PDF generation
- collaborative editing
- AI-assisted document generation

These features are **not required for MVP** unless explicitly listed below.

---

# 3. Target User

The initial user is a technical/non-technical user who needs to visually create structured documents without manually writing HTML/CSS.

Example use cases:

### Template creation

```text
Create a certificate template
        ↓
Drag text fields
        ↓
Position fields
        ↓
Style fields
        ↓
Save template
```

### Document recreation

```text
Reference document
        ↓
Create page
        ↓
Place text/image/fields
        ↓
Adjust layout
        ↓
Export HTML
```

### Future OCR workflow

```text
Upload document
        ↓
OCR + layout detection
        ↓
Automatically generate elements
        ↓
User visually corrects layout
        ↓
Save structured template
```

---

# 4. Core Design Principle

## The JSON document model is the source of truth.

Do **not** use the DOM as the application's state.

Bad architecture:

```text
DOM
 ↓
Modify DOM directly
 ↓
Save DOM
```

Required architecture:

```text
User Action
     ↓
Editor Command
     ↓
Document State
     ↓
React
     ↓
DOM
```

Example:

```typescript
moveElement("element-123", {
  x: 250,
  y: 120
});
```

The state changes:

```json
{
  "x": 250,
  "y": 120
}
```

React then renders the updated element.

---

# 5. Technology Requirements

## Frontend

Use:

- Next.js
- React
- TypeScript
- Tailwind CSS
- Zustand

Use the Next.js App Router.

The editor itself should be a client-side application.

---

## Dragging and interaction

Use either:

- `dnd-kit`
- custom pointer/mouse interaction
- another mature React-compatible interaction library

The implementation should support precise positioning rather than only list-style drag-and-drop.

---

## Rich text

Use:

- Tiptap / ProseMirror

if rich-text editing is required.

For MVP, basic text editing is sufficient.

---

## State management

Use Zustand.

Recommended state separation:

```text
EditorStore
DocumentStore
HistoryStore
SelectionStore
UIStore
```

Avoid placing the entire editor implementation inside a single giant Zustand store.

---

# 6. Application Structure

Recommended routes:

```text
/
├── projects
│
├── projects/[projectId]
│
├── editor/[documentId]
│
├── templates
│
└── settings
```

MVP may initially only implement:

```text
/editor/[documentId]
```

---

# 7. Editor UI

The editor should use a three-panel layout.

```text
┌───────────────────────────────────────────────────────────┐
│                         Toolbar                            │
├──────────────┬──────────────────────────────┬─────────────┤
│              │                              │             │
│   Elements   │                              │ Properties  │
│   Sidebar    │            Canvas            │   Panel     │
│              │                              │             │
│              │                              │             │
│              │                              │             │
│              │                              │             │
└──────────────┴──────────────────────────────┴─────────────┘
```

---

# 8. Toolbar

The toolbar should contain:

### Document controls

- Save
- Undo
- Redo
- Preview
- Export

### Canvas controls

- Zoom in
- Zoom out
- Fit to screen
- Zoom percentage

### Editing controls

- Delete
- Duplicate
- Bring forward
- Send backward
- Bring to front
- Send to back

---

# 9. Element Sidebar

The sidebar should contain draggable elements.

MVP:

```text
Elements

Text
Image
Rectangle
Line
Field
```

Future:

```text
Table
Checkbox
Radio
Signature
QR Code
Barcode
Container
Group
Repeater
Dynamic List
```

---

# 10. Canvas

The canvas represents the document/page.

Example:

```text
                 Canvas
       ┌──────────────────────────┐
       │                          │
       │       Hello World        │
       │                          │
       │   Name: [____________]   │
       │                          │
       │                          │
       │                          │
       └──────────────────────────┘
```

The canvas must support:

- zoom
- pan
- selection
- dragging
- resizing
- snapping
- rulers/guides
- grid
- multi-selection

Some advanced features may be deferred.

---

# 11. Page Model

A document can contain one or more pages.

Example:

```json
{
  "id": "doc-001",
  "name": "Certificate",
  "pages": [
    {
      "id": "page-001",
      "width": 794,
      "height": 1123,
      "unit": "px",
      "elements": []
    }
  ]
}
```

Default MVP page:

```text
Width: 794px
Height: 1123px
```

This approximately represents A4 at 96 DPI.

---

# 12. Element Model

Every element must have a unique ID.

Base structure:

```typescript
interface BaseElement {
  id: string;
  type: ElementType;

  x: number;
  y: number;

  width: number;
  height: number;

  rotation: number;

  zIndex: number;

  locked: boolean;
  hidden: boolean;
}
```

---

# 13. Text Element

Example:

```json
{
  "id": "text-001",
  "type": "text",
  "x": 100,
  "y": 100,
  "width": 300,
  "height": 50,
  "rotation": 0,
  "zIndex": 1,
  "content": "Hello World",
  "style": {
    "fontFamily": "Arial",
    "fontSize": 24,
    "fontWeight": 400,
    "fontStyle": "normal",
    "textAlign": "left",
    "color": "#000000",
    "lineHeight": 1.2
  }
}
```

---

# 14. Image Element

```json
{
  "id": "image-001",
  "type": "image",
  "x": 100,
  "y": 200,
  "width": 300,
  "height": 200,
  "rotation": 0,
  "zIndex": 2,
  "src": "/images/example.png",
  "objectFit": "contain"
}
```

---

# 15. Shape Element

MVP should support:

```text
rectangle
line
```

Example:

```json
{
  "id": "shape-001",
  "type": "rectangle",
  "x": 100,
  "y": 300,
  "width": 400,
  "height": 100,
  "rotation": 0,
  "zIndex": 1,
  "style": {
    "backgroundColor": "#ffffff",
    "borderColor": "#000000",
    "borderWidth": 1,
    "borderRadius": 0
  }
}
```

---

# 16. Dynamic Field Element

This is important for future document-generation functionality.

A field should be different from ordinary text.

Example:

```json
{
  "id": "field-001",
  "type": "field",
  "x": 300,
  "y": 200,
  "width": 250,
  "height": 40,

  "field": {
    "name": "owner_name",
    "dataType": "string",
    "required": true
  },

  "style": {
    "fontSize": 16
  }
}
```

The visual editor may display:

```text
[ owner_name ]
```

but HTML rendering should eventually support:

```html
<span data-field="owner_name">
    {{owner_name}}
</span>
```

---

# 17. Selection System

When an element is selected:

```text
┌─────────────────────────┐
│                         │
│     Selected Element    │
│                         │
└─────────────────────────┘
 ↑                       ↑
resize handles
```

The selection overlay must provide:

- bounding box
- corner resize handles
- edge resize handles
- rotation handle
- selection indicator

---

# 18. Multi-Selection

Users should be able to select multiple elements.

Support:

```text
Shift + Click
```

and/or drag selection rectangle.

Selected elements can be:

- moved together
- deleted together
- duplicated together
- aligned
- distributed

---

# 19. Alignment

Provide:

```text
Align left
Align center
Align right

Align top
Align middle
Align bottom
```

For multiple elements:

```text
Distribute horizontally
Distribute vertically
```

---

# 20. Snapping

MVP should support basic snapping.

Snap to:

- page edges
- page center
- nearby element edges
- nearby element centers

---

# 21. Grid

Optional grid overlay.

Users should be able to:

- enable/disable grid
- change grid size

Default:

```text
Grid: 10px
```

---

# 22. Properties Panel

When no element is selected:

```text
Page Properties
```

When an element is selected:

```text
Element Properties
```

## Position

```text
X:       120
Y:       240

Width:   300
Height:  80

Rotation: 0°
```

## Text

For text elements:

```text
Font
Font Size
Weight
Style
Color
Alignment
Line Height
Letter Spacing
```

## Appearance

```text
Opacity
Background
Border
Border Radius
```

## Advanced

```text
Z-index
Locked
Hidden
```

---

# 23. Keyboard Shortcuts

Required:

```text
Delete       Delete selected
Backspace    Delete selected

Ctrl/Cmd + Z       Undo
Ctrl/Cmd + Shift Z Redo

Ctrl/Cmd + C       Copy
Ctrl/Cmd + V       Paste
Ctrl/Cmd + D       Duplicate

Arrow keys         Move 1px
Shift + Arrow      Move 10px

Escape             Deselect
```

---

# 24. Undo / Redo

Every document mutation should be represented as an editor operation.

Examples:

```text
CREATE_ELEMENT
DELETE_ELEMENT
MOVE_ELEMENT
RESIZE_ELEMENT
UPDATE_STYLE
UPDATE_CONTENT
CHANGE_Z_INDEX
```

History:

```text
Initial
 ↓
Add Text
 ↓
Move Text
 ↓
Resize Text
 ↓
Change Font
```

Undo should reverse operations rather than attempting to reconstruct the DOM.

---

# 25. Copy / Paste

Copying an element should serialize its document-model representation.

Pasting should generate a new ID.

Example:

```text
field-001
```

copied to:

```text
field-002
```

---

# 26. Layer Management

Elements must have deterministic stacking.

Support:

```text
Bring Forward
Send Backward
Bring To Front
Send To Back
```

Layer ordering should be stored in the document model.

---

# 27. Rendering Architecture

Create a renderer abstraction:

```typescript
renderElement(element)
```

Example:

```typescript
switch (element.type) {
  case "text":
    return <TextElement {...element} />;

  case "image":
    return <ImageElement {...element} />;

  case "rectangle":
    return <RectangleElement {...element} />;

  case "field":
    return <FieldElement {...element} />;
}
```

Do not create one giant component containing all element types.

---

# 28. HTML Export

The document model should be convertible into standalone HTML.

Example:

```typescript
generateHTML(document): string
```

Output:

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        .page {
            position: relative;
            width: 794px;
            height: 1123px;
        }

        .element {
            position: absolute;
        }
    </style>
</head>

<body>

<div class="page">

    <div
        class="element"
        style="
            left:100px;
            top:100px;
            width:300px;
            height:50px;
        "
    >
        Hello World
    </div>

</div>

</body>
</html>
```

The exported HTML must **not depend on React or Next.js**.

---

# 29. Import

The MVP does not need to support arbitrary HTML → editor conversion.

However, architecture should allow:

```text
HTML
 ↓
Parser
 ↓
Document Model
 ↓
Editor
```

Do not build the parser unless explicitly required for MVP.

---

# 30. Persistence

Documents must be serializable.

```typescript
JSON.stringify(document)
```

and later:

```typescript
JSON.parse(data)
```

The editor must be completely reconstructable from the saved JSON.

---

# 31. Autosave

MVP should support basic autosave.

Suggested behavior:

```text
User changes document
        ↓
Debounce 1–2 seconds
        ↓
Save document
```

Display:

```text
Saved
Saving...
Unsaved changes
```

---

# 32. Backend API

The frontend should communicate through a clean API abstraction.

Suggested endpoints:

```text
GET    /documents/:id
POST   /documents
PUT    /documents/:id
DELETE /documents/:id
```

Potential future:

```text
POST /documents/:id/export
POST /documents/:id/render
POST /documents/import
```

The frontend should not tightly couple the editor to the backend implementation.

---

# 33. Database Model

Basic document table:

```text
documents
---------
id
name
project_id
content_json
created_at
updated_at
```

Do not normalize every individual element into separate database rows for MVP.

Store the document model as JSON/JSONB.

PostgreSQL `JSONB` is preferred.

---

# 34. Project Structure

Recommended frontend structure:

```text
src/
├── app/
│
├── components/
│   ├── editor/
│   │   ├── Editor.tsx
│   │   ├── Canvas.tsx
│   │   ├── Toolbar.tsx
│   │   ├── Sidebar.tsx
│   │   ├── PropertiesPanel.tsx
│   │   ├── SelectionOverlay.tsx
│   │   └── Ruler.tsx
│   │
│   ├── elements/
│   │   ├── TextElement.tsx
│   │   ├── ImageElement.tsx
│   │   ├── RectangleElement.tsx
│   │   └── FieldElement.tsx
│   │
│   └── ui/
│
├── store/
│   ├── editorStore.ts
│   ├── documentStore.ts
│   ├── historyStore.ts
│   └── uiStore.ts
│
├── models/
│   ├── document.ts
│   ├── element.ts
│   └── page.ts
│
├── renderer/
│   ├── reactRenderer.tsx
│   └── htmlRenderer.ts
│
├── commands/
│   ├── elementCommands.ts
│   ├── historyCommands.ts
│   └── alignmentCommands.ts
│
├── utils/
│
└── types/
```

---

# 35. Non-Functional Requirements

## Performance

The editor should remain responsive with at least:

```text
500 elements/page
```

The architecture should eventually allow:

```text
1000+ elements/page
```

without major architectural changes.

## Browser

Support current:

- Chrome
- Firefox
- Edge
- Safari

Desktop-first.

Mobile editing is **out of scope for MVP**.

---

# 36. Security

Do not blindly render arbitrary user-provided HTML.

If HTML import is added later:

- sanitize HTML
- prevent script execution
- prevent event-handler injection
- sanitize URLs
- restrict dangerous CSS

Exported HTML must not allow arbitrary JavaScript injection through document content.

---

# 37. MVP Scope

The first implementation **must include only**:

### Canvas

- page
- zoom
- pan
- grid

### Elements

- Text
- Image
- Rectangle
- Field

### Interaction

- select
- drag
- resize
- delete
- duplicate
- multi-select

### Properties

- position
- size
- rotation
- text styling
- colors
- borders
- z-index

### Editor

- undo
- redo
- keyboard shortcuts
- snapping
- alignment

### Persistence

- JSON document model
- load
- save
- autosave

### Export

- standalone HTML/CSS

---

# 38. Explicitly Out of Scope for MVP

Do **not** implement:

- real-time collaboration
- multiplayer editing
- arbitrary HTML importing
- AI generation
- OCR
- PDF parsing
- PDF generation
- database normalization of individual elements
- mobile editor
- complex animations
- responsive website builder
- JavaScript execution inside documents
- plugin system

The architecture should permit these features later.

---

# 39. Future Architecture

The eventual platform should support:

```text
                    Document Engine
                          │
       ┌──────────────────┼──────────────────┐
       │                  │                  │
       ▼                  ▼                  ▼
   Visual Editor       OCR Engine        AI Engine
       │                  │                  │
       └──────────────────┼──────────────────┘
                          ▼
                  Document Model
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
             HTML        PDF       JSON Schema
              │                       │
              ▼                       ▼
          Rendering               Extraction
```

---

# 40. Future Semantic Elements

The document model should eventually support:

```text
Text
Image
Field
Table
Checkbox
Signature
Barcode
QR Code
Container
Group
Repeater
Conditional
```

Example:

```json
{
  "type": "field",
  "field": {
    "name": "citizenship_number",
    "dataType": "string"
  }
}
```

This is intentionally different from ordinary text.

---

# 41. Future OCR Integration

The editor should eventually accept:

```text
OCR result
+
Bounding boxes
+
Detected text
+
Document dimensions
```

and automatically create elements.

Example OCR:

```json
{
  "text": "Certificate No.",
  "bbox": [120, 100, 280, 130]
}
```

becomes:

```json
{
  "type": "text",
  "content": "Certificate No.",
  "x": 120,
  "y": 100,
  "width": 160,
  "height": 30
}
```

The editor then allows the user to correct the automatically detected layout.

---

# 42. Future AI Integration

The document model should be AI-friendly.

An AI system should eventually be able to produce structured elements:

```json
{
  "type": "field",
  "field": {
    "name": "full_name"
  }
}
```

instead of generating arbitrary HTML.

This allows AI to modify the document safely through structured commands.

Example:

```text
"Move the owner's name field below the address."

        ↓

AI command

        ↓

MOVE_ELEMENT
```

rather than:

```text
AI generates entire HTML document
```

---

# 43. Acceptance Criteria

The MVP is considered complete when a user can:

### AC-01
Open the editor and see an A4-sized page.

### AC-02
Drag a Text element onto the page.

### AC-03
Move the Text element freely.

### AC-04
Resize the Text element.

### AC-05
Edit its content.

### AC-06
Change font size, font weight, alignment and color.

### AC-07
Add an image.

### AC-08
Resize and reposition the image.

### AC-09
Add a dynamic field.

### AC-10
Select multiple elements.

### AC-11
Move multiple elements together.

### AC-12
Align selected elements.

### AC-13
Duplicate an element.

### AC-14
Delete an element.

### AC-15
Change element stacking order.

### AC-16
Undo and redo changes.

### AC-17
Save the document.

### AC-18
Reload the page and recover the document exactly.

### AC-19
Export the document to standalone HTML/CSS.

### AC-20
The exported HTML visually matches the editor canvas.

---

# 44. Engineering Rules for the Agent

The implementation agent **must follow these rules**:

### Rule 1 — Document model first

Do not start by manipulating DOM elements.

Define the document schema first.

### Rule 2 — Single source of truth

The document state is authoritative.

### Rule 3 — Components are renderers

React components render document state; they should not own persistent document state.

### Rule 4 — Commands modify state

Mutations should go through reusable commands/actions.

### Rule 5 — History is operation-based

Every mutation should be undoable.

### Rule 6 — No premature complexity

Do not implement OCR, AI, collaboration, PDF, or arbitrary HTML parsing during MVP.

### Rule 7 — Extensibility

New elements should be addable without rewriting the editor core.

The desired pattern is:

```typescript
ElementRegistry.register({
  type: "text",
  renderer: TextElement,
  inspector: TextInspector,
  serializer: serializeText
});
```

rather than large `if/else` or `switch` statements spread throughout the application.

---

# 45. Definition of Done

The implementation is complete when:

```text
┌──────────────────────────────────────┐
│             Visual Editor            │
├──────────┬─────────────────┬────────┤
│ Elements │     Canvas      │ Props  │
│          │                 │        │
│ Text     │    ┌───────┐    │ X: 120 │
│ Image    │    │ Hello │    │ Y: 200 │
│ Field    │    └───────┘    │ W: 300 │
│ Shape    │                 │ H: 50  │
│          │                 │        │
└──────────┴─────────────────┴────────┘
```

supports the complete edit → save → reload → export cycle:

```text
Create
  ↓
Edit
  ↓
Document JSON
  ↓
Save
  ↓
Reload
  ↓
Render
  ↓
Export HTML
```

with no loss of document structure or visual positioning.

---

# 46. Agent Implementation Priority

The coding agent should implement in this order:

```text
PHASE 1
Document schema
        ↓
PHASE 2
Zustand state
        ↓
PHASE 3
Canvas + page
        ↓
PHASE 4
Element rendering
        ↓
PHASE 5
Selection + dragging
        ↓
PHASE 6
Resize + rotation
        ↓
PHASE 7
Properties panel
        ↓
PHASE 8
Undo / redo
        ↓
PHASE 9
Alignment + snapping
        ↓
PHASE 10
Persistence
        ↓
PHASE 11
HTML renderer/exporter
        ↓
PHASE 12
Testing + performance
```

**Important:** The agent should not attempt to build the entire system in one pass. Each phase should produce a working state before proceeding to the next phase.
