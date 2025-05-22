import importlib.resources
import os
from pathlib import Path
import shutil
import backstage_templater  # <--- explicitly import the package

class Templater:

    def __init__(self):
        self.template_definition = self._load_template_definition()
        self.catalog_info = self._load_catalog_info()

    def generate_template(self):
        current_directory = Path(os.getcwd())
        template_project_name = f"backstage-{current_directory.name}"
        template_project_path = current_directory.parent / template_project_name
        template_project_path.mkdir(exist_ok=True)

        with open(template_project_path / 'template.yml', 'w') as f:
            f.write(self.template_definition)

        content_dir = template_project_path / "content"
        def ignore_patterns(dir, files):
            ignore = {'.git', '__pycache__'}
            return [f for f in files if f in ignore]
        shutil.copytree(current_directory, content_dir, dirs_exist_ok=True, ignore=ignore_patterns)

        with open(content_dir / 'catalog-info.yml', 'w') as f:
            f.write(self.catalog_info)

    def _load_template_definition(self):
        resource = importlib.resources.files(backstage_templater).joinpath('template_definition.yml')
        with resource.open('r', encoding='utf-8') as f:
            return f.read()

    def _load_catalog_info(self):
        resource = importlib.resources.files(backstage_templater).joinpath('catalog-info.yml')
        with resource.open('r', encoding='utf-8') as f:
            return f.read()

def main():
    templater = Templater()
    templater.generate_template()

if __name__ == "__main__":
    main()
