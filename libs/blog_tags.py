# -*- coding: utf-8 -*-
# @Author  : SamSa
"""
markdown 代码格式化
1. pip install mistune
    mistune 快速将markdown代码转化为html代码
2. pip install pygments
    pygments进行对html中的code进行美化
    支持的css样式
    default emacs   friendly    colorful    autumn  murphy  manni   monokai
    perldoc pastie  borland trac    native  fruity  bw  vim vs  tango   rrt
    xcode   igor    paraiso-light   paraiso-dark    lovelace    algol   algol_nu
    arduino rainbow_dash    abap
"""
import mistune
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter


def block_code(text, lang, inlinestyles=False, linenos=False):
    if not lang:
        text = text.strip()
        return u'<pre><code>%s</code></pre>\n' % mistune.escape(text)

    try:
        lexer = get_lexer_by_name(lang, stripall=True)
        formatter = HtmlFormatter(
            noclasses=inlinestyles, linenos=linenos
        )
        code = highlight(text, lexer, formatter)
        if linenos:
            return '<div class="highlight">%s</div>\n' % code
        return code
    except:
        return '<pre class="%s"><code>%s</code></pre>\n' % (
            lang, mistune.escape(text)
        )


class HighlightMixin(object):
    def block_code(self, text, lang):
        # renderer has an options
        inlinestyles = self.options.get('inlinestyles')
        linenos = self.options.get('linenos')
        return block_code(text, lang, inlinestyles, linenos)


class TocRenderer(HighlightMixin, mistune.Renderer):
    pass


# 自定义模板标签
# from django import template
# register = template.Library()
# @register.filter
def markdown_detail(value):
    renderer = TocRenderer(linenos=True, inlinestyles=False)
    mdp = mistune.Markdown(escape=True, renderer=renderer)
    return mdp(value)
