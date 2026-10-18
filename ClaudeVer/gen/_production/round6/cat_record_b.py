import json
from pathlib import Path
p=Path(r"F:\Project\world.execute-Ralmia-\ClaudeVer\gen\_production\round6\cat_generation.json")
m=json.loads(p.read_text(encoding="utf-8"))
m["assets"].append({"filename":"cat_ralmia_v2b.png","step":"B face-only local edit","prompt":"Use case: precise-object-edit. Image 1 is the EDIT TARGET, a finished waist-up cat-girl Ralmia cutout. Image 2 is her canonical identity reference only.\nEdit ONLY the exposed facial skin features inside image 1, to create matching alternate expression L15b. Keep the same exact face angle, outline, scale and position. Change the one open cyan eye into a content closed eye, and make BOTH closed eyes happy upward-curving \"^ ^\" arcs. Give her a slightly wider, upward happy omega smile, calm satisfaction and blush as if purring while being petted. No hand actually petting her; no added object.\nEverything outside the face must be pixel-identical: especially all hair and bangs, cat ears, ahoge, temple gem, mechanical paw fists and fingers, forearms, shoulders, torso, red bow, armor, alpha outline and transparent canvas. Do not recompose or resize the subject. Keep exact 1672x941 canvas and original transparent background. No text, symbols, watermark, tail or legs.","references":["cat_ralmia_v2.png","ref_sheet.png"],"source":"C:\\Users\\zaofenMachine\\.codex\\generated_images\\01a14edb-d956-7ae2-b8c5-5d4d3f241d21\\exec-022e09aa-6a9d-4bab-b045-b97373fc6fb2.png"})
m["status"]="complete"
m["validation"]="_qa/round6/cat_validation.json"
m["edit_mask"]="_qa/round6/cat_face_edit_mask.png"
m["final_files"]=["cat_ralmia_v2.png","cat_ralmia_v2b.png"]
p.write_text(json.dumps(m,ensure_ascii=False,indent=2),encoding="utf-8")
