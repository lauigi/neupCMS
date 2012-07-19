#-*- coding:utf-8 -*-
from django import forms
from django.utils.safestring import mark_safe

class UEditor(forms.Textarea):
    def render(self, name, value, attrs=None):
        html = super(UEditor, self).render(name, value, attrs)
        js = u"""
        <script type="text/javascript">
        var editor_a = new baidu.editor.ui.Editor();
        editor_a.render({textarea});
        </script>
        """
        js = js.format(textarea=attrs['id'])
        return mark_safe("\n".join([html, js]))

    class Media:
        base_url = "/media/editor/ueditor/"
        css = {"all": (base_url+"themes/default/ueditor.css",)}
        js = (base_url+"editor_config.js",base_url+"editor_all_min.js",)