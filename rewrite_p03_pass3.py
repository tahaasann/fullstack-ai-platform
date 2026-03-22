#!/usr/bin/env python3
"""Third pass: fix M5S4 and M6 remaining large code dumps."""

import json

def main():
    with open('content/projects/project-03.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    milestones = data['milestones']

    # ==========================================
    # M5 Step 4: Drag & Drop — substep 4.3 dumps 40 lines
    # ==========================================
    m5 = milestones[4]
    m5_step4 = m5['steps'][3]
    m5_step4['substeps'] = [
        {
            "order": "4.1",
            "action": "client/src/hooks/use-drag-drop.ts dosyasını aç — İSKELET hook yaz",
            "type": "code_write",
            "file": "client/src/hooks/use-drag-drop.ts",
            "code": "export function useDragDrop(onFileDrop: (file: File) => void) {\n  return { isDragging: false, dragHandlers: {} };\n}",
            "why": "Custom hook'u iskelet olarak oluşturuyoruz. onFileDrop callback ile dosya bırakıldığında ne yapılacağını DIŞ ARIDAN belirleyeceğiz."
        },
        {
            "order": "4.2",
            "action": "ÜSTE ÇIK — React hook'larını import et",
            "type": "code_write",
            "file": "client/src/hooks/use-drag-drop.ts",
            "code": "import { useState, useCallback, DragEvent } from 'react';",
            "why": "useState isDragging state'i için, useCallback event handler memoization için, DragEvent TypeScript tip güvenliği için gerekli."
        },
        {
            "order": "4.3",
            "action": "GERİ DÖN hook içine — isDragging state'ini tanımla",
            "type": "code_add",
            "file": "client/src/hooks/use-drag-drop.ts",
            "position": "inside:hook",
            "code": "  const [isDragging, setIsDragging] = useState(false);",
            "why": "Dosya sürüklenirken true olur — drop zone HIGHLIGHT göstermek için kullanılacak."
        },
        {
            "order": "4.4",
            "action": "State'in altına — dragEnter ve dragLeave handler'larını yaz",
            "type": "code_add",
            "file": "client/src/hooks/use-drag-drop.ts",
            "position": "after:state",
            "code": "  const handleDragEnter = useCallback((e: DragEvent) => {\n    e.preventDefault();\n    e.stopPropagation();\n    setIsDragging(true);\n  }, []);\n\n  const handleDragLeave = useCallback((e: DragEvent) => {\n    e.preventDefault();\n    e.stopPropagation();\n    setIsDragging(false);\n  }, []);",
            "why": "preventDefault() HER drag event'inde çağrılmalı — yoksa tarayıcı varsayılan davranışı uygular. stopPropagation() ile event üst element'lere YAYILMAZ."
        },
        {
            "order": "4.5",
            "action": "DragLeave'in altına — dragOver handler'ını yaz",
            "type": "code_add",
            "file": "client/src/hooks/use-drag-drop.ts",
            "position": "after:drag-leave",
            "code": "  const handleDragOver = useCallback((e: DragEvent) => {\n    e.preventDefault();\n    e.stopPropagation();\n  }, []);",
            "why": "dragOver'da preventDefault() OLMADAN drop event'i tetiklenmez. Bu en sık yapılan hatadır."
        },
        {
            "order": "4.6",
            "action": "DragOver'ın altına — drop handler'ını yaz",
            "type": "code_add",
            "file": "client/src/hooks/use-drag-drop.ts",
            "position": "after:drag-over",
            "code": "  const handleDrop = useCallback((e: DragEvent) => {\n    e.preventDefault();\n    e.stopPropagation();\n    setIsDragging(false);\n    const file = e.dataTransfer.files[0];\n    if (file) onFileDrop(file);\n  }, [onFileDrop]);",
            "why": "Dosya bırakıldığında isDragging false yapılır ve onFileDrop callback'i çağrılır. dataTransfer.files ile sürüklenen dosyalara erişilir."
        },
        {
            "order": "4.7",
            "action": "Drop handler'ın altına — return statement yaz",
            "type": "code_add",
            "file": "client/src/hooks/use-drag-drop.ts",
            "position": "after:drop",
            "code": "  return {\n    isDragging,\n    dragHandlers: {\n      onDragEnter: handleDragEnter,\n      onDragLeave: handleDragLeave,\n      onDragOver: handleDragOver,\n      onDrop: handleDrop,\n    },\n  };",
            "why": "dragHandlers objesi JSX'e spread edilebilir: {...dragHandlers}. isDragging ile koşullu stil uygulanır."
        },
        {
            "order": "4.8",
            "action": "chat-window.tsx dosyasına GERİ DÖN — hook'u import et ve entegre et",
            "type": "code_modify",
            "file": "client/src/components/chat-window.tsx",
            "code": "import { useDragDrop } from '../hooks/use-drag-drop';\n\n// Component içinde:\nconst { isDragging, dragHandlers } = useDragDrop(async (file) => {\n  const formData = new FormData();\n  formData.append('file', file);\n  // 2.5'teki yükleme mantığının aynısı\n});",
            "position": "top",
            "why": "Az önce yazdığımız hook'u ChatWindow'a BAĞLIYORUZ. 2.5'teki dosya yükleme mantığını TEKRAR kullanıyoruz."
        },
        {
            "order": "4.9",
            "action": "Ana div'e dragHandlers'ı ve isDragging stilini ekle",
            "type": "code_modify",
            "file": "client/src/components/chat-window.tsx",
            "code": "<div className={`flex h-full flex-col ${isDragging ? 'ring-2 ring-blue-500 ring-inset' : ''}`} {...dragHandlers}>",
            "position": "inside:return",
            "why": "isDragging true olduğunda mavi border gösterilir — kullanıcı dosyayı NEREYE bırakacağını anlar."
        },
        {
            "order": "4.10",
            "action": "Drag & drop'un çalıştığını doğrula",
            "type": "validate",
            "validation": "Dosya sürüklendiğinde chat penceresi mavi çerçeve ile highlight olmalı. Dosya bırakıldığında yüklenip mesaj olarak gönderilmeli.",
            "why": "Drag & drop, dosya paylaşımının en DOĞAL yöntemidir."
        }
    ]

    # ==========================================
    # M6: Check what M6 is and fix its substeps
    # ==========================================
    m6 = milestones[5]
    # Fix M6 steps with large code dumps
    for step in m6['steps']:
        new_substeps = []
        for sub in step.get('substeps', []):
            code = sub.get('code', '')
            if code and code.count('\n') + 1 > 25:
                # Break this substep into smaller pieces
                lines = code.split('\n')
                mid = len(lines) // 2

                # First half
                first_sub = dict(sub)
                first_sub['code'] = '\n'.join(lines[:mid])
                first_sub['action'] = sub['action']
                new_substeps.append(first_sub)

                # Second half
                second_sub = {
                    "order": sub['order'] + 'b',
                    "action": f"{sub['action']} (devamı)",
                    "type": sub['type'],
                    "file": sub.get('file', ''),
                    "code": '\n'.join(lines[mid:]),
                    "why": f"{sub['order']}'deki kodun devamı."
                }
                if 'position' in sub:
                    second_sub['position'] = 'bottom'
                new_substeps.append(second_sub)
            else:
                new_substeps.append(sub)
        step['substeps'] = new_substeps

    # Write result
    with open('content/projects/project-03.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Validate
    with open('content/projects/project-03.json', 'r', encoding='utf-8') as f:
        validated = json.load(f)

    violations = []
    for m in validated['milestones']:
        for s in m['steps']:
            for sub in s.get('substeps', []):
                code = sub.get('code', '')
                if code and code.count('\n') + 1 > 30:
                    violations.append((m['id'], sub['order'], code.count('\n') + 1))

    total = sum(len(s.get('substeps', [])) for m in validated['milestones'] for s in m['steps'])
    print(f'Total substeps: {total}')
    print(f'Substeps >30 lines: {len(violations)}')
    for v in violations:
        print(f'  {v[0]} sub {v[1]}: {v[2]} lines')
    print('JSON validated!')


if __name__ == '__main__':
    main()
