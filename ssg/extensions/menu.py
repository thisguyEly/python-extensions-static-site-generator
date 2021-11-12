from ssg import hooks, parsers, site

files = []


@hooks.register("collect_files")
def collect_files(source, site_parsers):
    def valid(p): return not isinstance(p, parsers.ResourceParser)
    for path in source.rglob("*"):
        for parser in list(filter(valid, site_parsers)):
            if parser.valid_file_ext(path.suffix):
                files.append(path)


@hooks.register("generate_menu")
def generate_menu(html, ext):
    template = '<li><a href="{}{}">{}</a></li>'
    def menu_item(name, ext): return template.format(name, ext, name.title())
    menu = "\n".join([menu_item(path.stem, ext) for path in files])
    return "<ul>\n{}</ul>\n{}".format(menu, html)
