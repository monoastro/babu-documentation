
● Context for new session

  Immediate task: citizenship_back NoneType fix (Option 2 — central)

  Bug: Build failed: can only concatenate str (not 'NoneType') to str

  Root cause: Extractor returns explicit null for some fields. extracted.get(key, "") only defaults when key is
  missing, not when value is None. The None passes through d.update() in layouts, overwrites the "" default, then
  crashes at string concatenation sites like "Date: " + d["copy_issue_date_bs"] (citizenship_back/layout.py:491).

  Fix — two edits:

  1. information_extraction/extractor.py line 23:
  # FROM:
  return { key: extracted.get(key, "") for key in schema["required"] }
  # TO:
  return { key: extracted.get(key, "") or "" for key in schema["required"] }

  2. main.py line 78 (inside resolve_data, the data_path branch — add line after data = json.loads(...)):
  data = json.loads(data_path.read_text(encoding="utf-8"))
  data = {k: (v if v is not None else "") for k, v in data.items()}  # NEW

  Verify:
  python -c "
  import json, pathlib
  pathlib.Path('/tmp/cb_null.json').write_text(json.dumps({
      'copy_issue_date_bs': None, 'full_name': 'test',
      'citizenship_no': '', 'sex': '', 'dob_year': '', 'dob_month': '',
      'dob_day': '', 'birth_district': '', 'birth_rm_mn': '',
      'birth_ward_no': '', 'perm_district': '', 'perm_municipality': '',
      'perm_ward_no': '', 'nepal_citizenship_act_sentence': '',
      'citizenship_type': '', 'right_thumb_impression': '',
      'left_thumb_impression': '', 'copy_officer_signature': '',
      'copy_officer_name': '', 'copy_officer_designation': '',
      'issuing_officer_signature': '', 'issuing_officer_name': '',
      'issuing_officer_designation': '', 'issue_date_bs': '', 'remarks': ''
  }))"
  .venv/bin/python main.py --type citizenship_back --data /tmp/cb_null.json -o /tmp/cb_test.html

  Other concatenation crash sites: document_builder/letter/layout.py lines 171-172 (d["email_address"],
  d["website_url"]). Central fix covers these too.

  ---
  Standing constraints

  - Never print API key values — length/prefix checks only
  - Monochrome output only (#000000 on #ffffff, enforced in html_engine/monochrome.py)
  - Prefer graphify query/path/explain over grep when graphify-out/graph.json exists
  - Caveman mode active (full)
  - Do not run graphify label unasked (LLM token cost)
  - After code changes: run graphify update .

  ---
  Pending after this fix

  - PAN layout rewrite — document_builder/pan/layout.py needs full rewrite to match source scan (608x857 portrait, A4
  portrait output). Complete rewrite code was composed in prior session but never written to disk. Source scan
  aspect ratio and block positions must be preserved.
  - Autolayout overhaul plan at /home/moon/.claude/plans/sunny-painting-pnueli.md — separate larger task, geometry
  from Datalab /convert bboxes.
