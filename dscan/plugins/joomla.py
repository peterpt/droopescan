from cement.core import handler, controller
from dscan.common.update_api import GitRepo
from dscan.plugins import BasePlugin
import dscan.common.update_api as ua
import dscan.common.versions

class Joomla(BasePlugin):
    can_enumerate_plugins = False
    can_enumerate_themes = False

    forbidden_url = "media/"
    regular_file_url = "media/system/js/validate.js"
    module_common_file = ""

    update_majors = ['1','2','3']

    interesting_urls = [("joomla.xml", "This CMS' default changelog.")]

    interesting_module_urls = [
    ]

    class Meta:
        # The label is important, choose the CMS name in lowercase.
        label = 'joomla'

    # This function is the entry point for the CMS.
    @controller.expose(help='joomla related scanning tools')
    def joomla(self):
        self.plugin_init()

    def update_version_check(self):
        """
        @return: True if new tags have been made in the github repository.
        """
        return ua.github_tags_newer('joomla/joomla-cms/', self.versions_file,
                update_majors=self.update_majors)

    def update_version(self):
        """
        @return: updated VersionsFile
        """
        gr, versions_file, new_tags = ua.github_repo_new('joomla/joomla-cms/',
                'joomla/joomla-cms/', self.versions_file, self.update_majors)

        hashes = {}
        for version in new_tags:
            gr.tag_checkout(version)
            hashes[version] = gr.hashes_get(versions_file, self.update_majors)

        versions_file.update(hashes)
        return versions_file

    def update_plugins_check(self):
        return False

    def update_plugins(self):
        pass

def load(app=None):
    handler.register(Joomla)

