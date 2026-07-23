  source PNG + OCR JSON + base layout(generate a new one if it doesn't exist from the source PNG)
                │
                ▼
          render candidate PNG
                │
                ▼
     compare source ↔ candidate
         │                 │
         │ acceptable      │ mismatch
         ▼                 ▼
      approve       diagnose discrepancy
                           │
                           ▼
            create a constrained layout patch
                           │
                           ▼
                    validate + render
                           │
                           └── repeat, with a retry limit
                                        │
                                        ▼
                               human review if unresolved

  key design choice: don’t let an AI freely generate a new HTML layout. Have it produce a constrained change to your existing layout mode
