#!/usr/bin/env python3
"""
Script para corregir links internos en docs/ para que funcionen en GitHub Wiki.

Convierte links de formato repositorio a formato Wiki:
- [texto](./user/getting-started.md) → [texto](user/Getting-Started)
- [texto](../developer/architecture/tracking.md) → [texto](developer/architecture/Tracking)
"""

import re
import os
from pathlib import Path


def to_wiki_title(filename):
    """
    Convierte un nombre de archivo a formato Wiki title.
    Ejemplos:
    - getting-started.md → Getting-Started
    - implement-us.md → Implement-Us
    - user-guide.md → User-Guide
    """
    # Remover extensión .md
    name = filename.replace('.md', '')

    # Convertir a Title Case manteniendo guiones
    # getting-started → Getting-Started
    parts = name.split('-')
    return '-'.join(word.capitalize() for word in parts)


def convert_link_to_wiki_format(match, current_file_path):
    """
    Convierte un link de formato repo a formato Wiki.

    Args:
        match: Match object del regex
        current_file_path: Path del archivo actual (para resolver rutas relativas)

    Returns:
        str: Link en formato Wiki
    """
    link_text = match.group(1)
    link_path = match.group(2)
    anchor = match.group(3) if match.lastindex >= 3 else ""

    # Resolver ruta relativa desde current_file_path
    current_dir = Path(current_file_path).parent
    docs_dir = Path('/Users/victor/PycharmProjects/claude-dev-kitc/docs')

    # Convertir link a path absoluto
    if link_path.startswith('/'):
        # Path absoluto desde raíz del proyecto
        absolute_path = Path('/Users/victor/PycharmProjects/claude-dev-kitc') / link_path.lstrip('/')
    else:
        # Path relativo desde current_file
        absolute_path = (current_dir / link_path).resolve()

    # Si el link apunta fuera de docs/, dejarlo sin modificar
    try:
        relative_to_docs = absolute_path.relative_to(docs_dir)
    except ValueError:
        # Está fuera de docs/ (como ../README.md, ../PROJECT_PLAN.md)
        return match.group(0)

    # Convertir relative_to_docs a string
    link_path_normalized = str(relative_to_docs)

    # Separar directorio y archivo
    path_parts = link_path_normalized.split('/')

    # Casos especiales para archivos mapeados por el workflow
    if link_path_normalized in ['README.md', 'index.md']:
        wiki_path = 'Home'
    elif link_path_normalized == 'user/index.md':
        wiki_path = 'Documentation-Index'
    else:
        # Convertir cada parte de la ruta
        converted_parts = []
        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:
                # Última parte es el archivo - convertir a Wiki title
                if part.endswith('.md'):
                    converted_parts.append(to_wiki_title(part))
                else:
                    converted_parts.append(part)
            else:
                # Directorio - mantener tal cual
                converted_parts.append(part)

        wiki_path = '/'.join(converted_parts)

    # Agregar anchor si existe
    if anchor:
        wiki_path += anchor

    return f'[{link_text}]({wiki_path})'


def fix_links_in_file(file_path):
    """
    Corrige todos los links internos a .md en un archivo.

    Args:
        file_path: Path del archivo a corregir

    Returns:
        bool: True si se hicieron cambios
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Regex para capturar links markdown: [texto](ruta.md) o [texto](ruta.md#anchor)
    # Captura: [texto](cualquier-cosa.md) o [texto](./cualquier-cosa.md) o [texto](../cualquier-cosa.md)
    pattern = r'\[([^\]]+)\]\(([^\)]+\.md)(#[^\)]+)?\)'

    # Convertir todos los links
    content = re.sub(
        pattern,
        lambda m: convert_link_to_wiki_format(m, file_path),
        content
    )

    # Si hubo cambios, escribir de vuelta
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True

    return False


def main():
    """Main function."""
    docs_dir = Path('/Users/victor/PycharmProjects/claude-dev-kitc/docs')

    print("🔍 Buscando archivos .md con links a corregir...")

    changed_files = []
    unchanged_files = []

    # Buscar todos los archivos .md en docs/
    for md_file in docs_dir.rglob('*.md'):
        relative_path = md_file.relative_to(docs_dir)

        # Corregir links
        if fix_links_in_file(md_file):
            changed_files.append(relative_path)
            print(f"  ✅ {relative_path}")
        else:
            unchanged_files.append(relative_path)
            print(f"  ⏭️  {relative_path} (sin cambios)")

    print(f"\n📊 Resumen:")
    print(f"  ✅ Archivos modificados: {len(changed_files)}")
    print(f"  ⏭️  Archivos sin cambios: {len(unchanged_files)}")

    if changed_files:
        print(f"\n📝 Archivos modificados:")
        for file in changed_files:
            print(f"  - {file}")


if __name__ == '__main__':
    main()
