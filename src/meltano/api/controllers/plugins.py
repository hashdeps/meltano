from meltano.core.compiler.project_compiler import ProjectCompiler
from meltano.core.plugin_discovery_service import PluginDiscoveryService, PluginNotFoundError
from meltano.core.plugin import PluginType
from meltano.core.project import Project
from meltano.core.project_add_service import ProjectAddService
from meltano.core.config_service import ConfigService
from meltano.core.plugin_install_service import PluginInstallService
from meltano.core.tracking import GoogleAnalyticsTracker

from flask import Blueprint, request, jsonify

pluginsBP = Blueprint("plugins", __name__, url_prefix="/api/v1/plugins")


@pluginsBP.route("/all", methods=["GET"])
def all():
    new_project = Project()
    new_plugin_discovery_service = PluginDiscoveryService(new_project)
    result = new_plugin_discovery_service.discover(PluginType.ALL)
    return jsonify(result)


@pluginsBP.route("/installed", methods=["GET"])
def installed():
    project = Project.find()
    config = ConfigService(project)
    plugins = []
    installedPlugins = {}
    meltano_manifest = project.meltano

    for plugin in config.plugins():
        discovery = PluginDiscoveryService(project)
        try:
            definition = discovery.find_plugin(plugin.type, plugin.name)
        except PluginNotFoundError:
            definition = {}
        merged = {**definition.canonical(),**plugin.canonical() }
        plugins.append(merged)

    meltano_plugins = project.meltano['plugins']

    for type in meltano_plugins:
        installedPlugins[type] = []
        for type_plugin in meltano_plugins[type]:
            for complete_plugin in plugins:
                if type_plugin['name'] == complete_plugin['name']:
                    this_plugin = complete_plugin
            
                    if 'settings' in this_plugin:
                        del this_plugin['settings']
                    
                    if 'select' in this_plugin:
                        del this_plugin['select']

                    installedPlugins[type].append(this_plugin)

    meltano_manifest['plugins'] = installedPlugins

    return jsonify(meltano_manifest)


@pluginsBP.route("/add", methods=["POST"])
def add():
    payload = request.get_json()
    plugin_type = PluginType(payload["plugin_type"])
    plugin_name = payload["name"]

    project = Project.find()
    add_service = ProjectAddService(project)
    plugin = add_service.add(plugin_type, plugin_name)

    return jsonify(plugin.canonical())


@pluginsBP.route("/install", methods=["POST"])
def install():
    payload = request.get_json()
    plugin_type = PluginType(payload["plugin_type"])
    plugin_name = payload["name"]

    project = Project.find()
    compiler = ProjectCompiler(project)
    install_service = PluginInstallService(project)
    config_service = ConfigService(project)

    plugin = config_service.find_plugin(plugin_name, plugin_type=plugin_type)
    run_venv = install_service.create_venv(plugin)
    run_install_plugin = install_service.install_plugin(plugin)

    if plugin_type is PluginType.MODELS:
        try:
            compiler.compile()
        except Exception as e:
            pass

    tracker = GoogleAnalyticsTracker(project)
    tracker.track_meltano_add(plugin_type=plugin_type, plugin_name=plugin_name)

    return jsonify(plugin.canonical())
