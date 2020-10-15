import sublime_plugin
import sublime
import sys

if int(sublime.version()) >= 3114:
    # Clear module cache to force reloading all modules of this package.
    # See https://github.com/emmetio/sublime-text-plugin/issues/35
    prefix = __package__ + "."  # don't clear the base package
    for module_name in [
        module_name
        for module_name in sys.modules
        if (module_name.startswith(prefix) and module_name != __name__) or ('json' == module_name)
    ]:
        del sys.modules[module_name]
    prefix = None

from .lib.tab_nine_process import tabnine_proc
from .lib.settings  import is_native_auto_complete

capabilities = tabnine_proc.get_capabilities()
is_v2 = False

if is_native_auto_complete() or (capabilities["enabled_features"] and "sublime.new-experience" in capabilities["enabled_features"]): 
    is_v2 = True
    from .completions.completions_v2 import *
else: 
    from .completions.completions_v1 import *

class DisableViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.settings().set("tabnine-disabled", True)

    def is_visible(self, *args):
        return is_v2 and not self.view.settings().get("tabnine-disabled", False)

class EnableViewCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.view.settings().set("tabnine-disabled", False)
    def is_visible(self, *args):
        return is_v2 and self.view.settings().get("tabnine-disabled", False)

class EnableNativeAutoCompleteCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        sublime.load_settings('TabNine.sublime-settings').set("native_auto_complete", True)
        sublime.save_settings('TabNine.sublime-settings')
        sublime_plugin.unload_plugin(__name__)
        sublime_plugin.reload_plugin(__name__)
    def is_visible(self, *args):
        return not is_v2
