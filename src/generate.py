from pathlib import Path

from convert import markdown_to_html_node


def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    try:
        title_line = next(line for line in lines if line.startswith("# "))
    except StopIteration:
        raise ValueError("Title not found")
    return title_line[2:].strip()


def generate_page(src_path: Path, template_path: Path, dest_path: Path, base_path: str = "/") -> None:
    print(f"Generating page from {src_path!s} to {dest_path!s} using {template_path!s}")
    markdown = src_path.read_text()
    title = extract_title(markdown)
    content = markdown_to_html_node(markdown).to_html()
    template = template_path.read_text()
    html = (
        template
        .replace("{{ Title }}", title)
        .replace("{{ Content }}", content)
        .replace('href=/"', 'href="' + base_path)
        .replace('src=/"', 'src="' + base_path)
    )
    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True)
    dest_path.write_text(html)
